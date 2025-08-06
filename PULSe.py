import argparse
import subprocess
import sys
import os

def run_script(script_name, args_dict):
    """
    Executes a script with a list of arguments.
    This helper function correctly formats the arguments with their flags.
    """
    # Start with the python executable and the script name
    command = [sys.executable, script_name]
    
    # Iterate through the dictionary and add flags and values to the command list
    for key, value in args_dict.items():
        if value is not None:
            command.append(f'-{key}')
            command.append(str(value))
    
    # Run the command and handle potential errors
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print(f"Error: The script '{script_name}' was not found. Please ensure it is in the same directory.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error: The script '{script_name}' exited with code {e.returncode}.", file=sys.stderr)
        sys.exit(e.returncode)


def main():
    """Main function to parse arguments and dispatch to the correct script."""
    parser = argparse.ArgumentParser(description='Wrapper for different modes')
    
    # Define all possible arguments for all modes
    parser.add_argument('-mode', type=str, required=True, help='Mode of operation')
    parser.add_argument('-pref', type=str, help='File prefix for image_gen_ms and image_gen_vcf (modes: image_gen_ms, image_gen_vcf)')
    parser.add_argument('-nHap', type=int, help='Number of haplotypes for image_gen_ms and image_gen_vcf (modes: image_gen_ms, image_gen_vcf)')
    parser.add_argument('-subFolder', type=str, help='Subfolder name for (modes: image_gen_ms, image_gen_vcf)')
    parser.add_argument('-n', type=int, help='Number of files to use (modes: image_gen_ms, image_gen_vcf)')
    parser.add_argument('-start', type=int, help='Start number of files (modes: image_gen_ms, image_gen_vcf)')
    parser.add_argument('-out', type=str, help='Output file name (modes: image_gen_ms, image_gen_vcf)')
    
    parser.add_argument('-fileName', type=str, help= 'Image filename prefix (modes: HOG)')
    parser.add_argument('-pipeline', type=str, choices=['P1', 'P2'], help='P1 or P2 (modes: HOG, train, calibrate)')   
    
    
    parser.add_argument('-u', type=int, help='Number of samples on the unlabeled set (mode: train)')
    parser.add_argument('-l', type=int, help='Number of samples on the labeled set (mode: train)')
    parser.add_argument('-lp', type=str, help='Labeled positive filename prefix (mode: train)')
    parser.add_argument('-testcase', type=int, choices=[0, 1], help='0: simulated unlabeled set, 1: empirical unlabeled set (mode: train, calibrate)')
    parser.add_argument('-testname', type=str, help='Test name (mode: train, calibrate)')
    parser.add_argument('--p', type=int, help='Percentage of positives in the unlabeled set (mode: train)(testcase 0 only)')
    parser.add_argument('--up', type=str, help='Unlabeled positive filename prefix (mode: train)(testcase 0 only)')
    parser.add_argument('--un', type=str, help='Unlabeled negative filename prefix (mode: train)(testcase 0 only)')
    parser.add_argument('--emp', type=str, help='Empirical filename (mode: train)(testcase 1 only)')
    parser.add_argument('--C', type=float, help='C parameter (mode: train)(testcase 1 only)')
    parser.add_argument('--L1', type=float, help='L1 parameter (mode: train)(testcase 1 only)')

    parser.add_argument('-T', type=float, help='Calibration threshold (mode: calibrate)')

    parser.add_argument('-fileNameVCF', type=str, help= 'VCF file name (mode: preprocess_vcf)')
    parser.add_argument('-outFolder', type=str, help= 'Output subfolder name to be created inside VCF_datasets (mode: preprocess_vcf)')

    args = parser.parse_args()
    mode = args.mode

    # A dictionary to hold the arguments we will pass to the child script.
    script_args = {}

    # Validate arguments for each mode
    if mode == 'image_gen_ms':
        required_args = ['pref', 'nHap', 'subFolder', 'n', 'start', 'out']
        invalid_args = ['fileName', 'pipeline', 'u', 'l', 'lp', 'testcase', 'testname', 'p', 'up', 'un', 'emp', 'C', 'L1', 'T', 'fileNameVCF', 'outFolder']
    elif mode == 'HOG':
        required_args = ['fileName', 'pipeline']
        invalid_args = ['pref', 'nHap', 'subFolder', 'n', 'start', 'out', 'u', 'l', 'lp', 'testcase', 'testname', 'p', 'up', 'un', 'emp', 'C', 'L1', 'T', 'fileNameVCF', 'outFolder']
    elif mode == 'train':
        required_args = ['u', 'l', 'lp', 'pipeline', 'testcase', 'testname']
        invalid_args = ['pref', 'nHap', 'subFolder', 'n', 'start', 'out', 'fileName', 'T', 'fileNameVCF', 'outFolder']

        if args.testcase == 0:
            if args.p is None or args.up is None or args.un is None:
                print(f"Error: Missing required arguments for 'train' mode with testcase 0: --p, --up and --un are required.")
                sys.exit(1)
            required_args.extend(['p', 'up', 'un'])
            invalid_args.extend(['emp', 'C', 'L1'])
        elif args.testcase == 1:
            if args.emp is None or args.C is None or args.L1 is None:
                print(f"Error: Missing required arguments for 'train' mode with testcase 1: --emp, --C, and --L1 are required.")
                sys.exit(1)
            required_args.extend(['emp', 'C', 'L1'])
            invalid_args.extend(['p', 'up', 'un'])
        else:
            print(f"Error: Invalid value for -testcase. Must be 0 or 1.")
            sys.exit(1)
    elif mode == 'calibrate':
        required_args = ['testname', 'pipeline', 'testcase', 'T']
        invalid_args = ['pref', 'nHap', 'subFolder', 'n', 'start', 'out', 'fileName', 'u', 'l', 'lp', 'p', 'up', 'un', 'emp', 'C', 'L1', 'fileNameVCF', 'outFolder']
    elif mode == 'preprocess_vcf':
        required_args = ['fileNameVCF', 'outFolder']
        invalid_args = ['pref', 'nHap', 'subFolder', 'n', 'start', 'out', 'fileName', 'pipeline', 'u', 'l', 'lp', 'testcase', 'testname', 'p', 'up', 'un', 'emp', 'C', 'L1', 'T']
    elif mode == 'image_gen_vcf':
        required_args = ['pref', 'nHap', 'subFolder', 'n', 'start', 'out']
        invalid_args = ['fileName', 'pipeline', 'u', 'l', 'lp', 'testcase', 'testname', 'p', 'up', 'un', 'emp', 'C', 'L1', 'T', 'fileNameVCF', 'outFolder']
    elif mode == 'HOG':
        required_args = ['fileName', 'pipeline']
        invalid_args = ['pref', 'nHap', 'subFolder', 'n', 'start', 'out', 'u', 'l', 'lp', 'testcase', 'testname', 'p', 'up', 'un', 'emp', 'C', 'L1', 'T', 'fileNameVCF', 'outFolder']
    else:
        print(f"Error: Mode '{mode}' is invalid")
        sys.exit(1)

    # Check for missing required arguments
    missing_args = [arg for arg in required_args if getattr(args, arg) is None]
    if missing_args:
        print(f"Error: Missing required arguments for '{mode}' mode: {', '.join(missing_args)}")
        sys.exit(1)

    # Check for invalid arguments
    invalid_args_provided = [arg for arg in invalid_args if getattr(args, arg) is not None]
    if invalid_args_provided:
        print(f"Error: {' '.join(invalid_args_provided)} is/are invalid for '{mode}' mode")
        sys.exit(1)

    # Populate the script_args dictionary with only the required arguments
    for arg in required_args:
        script_args[arg] = getattr(args, arg)

    # Map modes to their respective scripts
    script_mapping = {
        'image_gen_ms': 'image_gen_ms.py',
        'train': 'train.py',
        'preprocess_vcf': 'preprocess_vcf.py',
        'image_gen_vcf': 'image_gen_vcf.py',
        'HOG': 'HOG.py',
        'calibrate': 'calibrate.py'
    }

    if mode in script_mapping:
        script_name = script_mapping[mode]
        run_script(script_name, script_args)
    else:
        print(f"Error: Mode '{mode}' is invalid")
        sys.exit(1)

if __name__ == '__main__':
    main()