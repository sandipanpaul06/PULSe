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
    parser.add_argument('-mode', required=True, help='Mode of operation')
    parser.add_argument('-pref', type=str, help='File prefix for image_gen_ms and image_gen_vcf')
    parser.add_argument('-out', type=str, help='Output file name')
    parser.add_argument('-nHap', type=int, help='Number of haplotypes for image_gen_ms and image_gen_vcf')
    parser.add_argument('-subFolder', type=str, help='Subfolder name for image_gen_ms')
    parser.add_argument('-n', type=int, help='Number of files for image_gen_ms and image_generation_vcf')
    parser.add_argument('-start', type=int, help='Start number of files for image_gen_ms and image_generation_vcf')
    parser.add_argument('-stop', type=int, help='Stop number of files for image_gen_vcf')
    parser.add_argument('-u', type=int, help='Number of samples on the unlabeled set')
    parser.add_argument('-l', type=int, help='Number of samples on the labeled set')
    parser.add_argument('-p', type=int, help='Percentage of positives in the unlabeled set')
    parser.add_argument('-lp', type=str, help='Labeled positive filename prefix')
    parser.add_argument('-pipeline', type=str, choices=['P1', 'P2'], help='P1 or P2')
    parser.add_argument('-testcase', type=int, choices=[0, 1], help='0: simulated unlabeled set, 1: empirical unlabeled set')
    parser.add_argument('-testname', type=str, help='Test name (train mode)')
    parser.add_argument('--up', type=str, help='Unlabeled positive filename prefix (testcase 0 only, train mode)')
    parser.add_argument('--un', type=str, help='Unlabeled negative filename prefix (testcase 0 only, train mode)')
    parser.add_argument('--emp', type=str, help='Empirical filename (testcase 1 only, train mode)')
    parser.add_argument('--C', type=str, help='C parameter (testcase 1 only, train mode)')
    parser.add_argument('--L1', type=str, help='L1 parameter (testcase 1 only, train mode)')

    args = parser.parse_args()
    mode = args.mode

    # A dictionary to hold the arguments we will pass to the child script.
    script_args = {}

    # Validate arguments for each mode
    if mode == 'image_gen_ms':
        required_args = ['pref', 'out', 'nHap', 'subFolder', 'n', 'start']
        invalid_args = []
    elif mode == 'train':
        required_args = ['u', 'l', 'p', 'lp', 'pipeline', 'testcase', 'testname']
        invalid_args = []

        if args.testcase == 0:
            if args.up is None or args.un is None:
                print(f"Error: Missing required arguments for 'train' mode with testcase 0: --up and --un are required.")
                sys.exit(1)
            required_args.extend(['up', 'un'])
            invalid_args.extend(['emp', 'C', 'L1'])
        elif args.testcase == 1:
            if args.emp is None or args.C is None or args.L1 is None:
                print(f"Error: Missing required arguments for 'train' mode with testcase 1: --emp, --C, and --L1 are required.")
                sys.exit(1)
            required_args.extend(['emp', 'C', 'L1'])
            invalid_args.extend(['up', 'un'])
        else:
            print(f"Error: Invalid value for -testcase. Must be 0 or 1.")
            sys.exit(1)
    elif mode == 'preprocess_vcf':
        required_args = ['fileName', 'outFolder']
        invalid_args = []
    elif mode == 'image_gen_vcf':
        required_args = ['subfolder', 'nHap', 'pref', 'start', 'stop', 'imgDim', 'outDat']
        invalid_args = []
    elif mode == 'HOG':
        required_args = ['fileName', 'pipeline']
        invalid_args = []
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
        'HOG': 'HOG.py'
    }

    if mode in script_mapping:
        script_name = script_mapping[mode]
        run_script(script_name, script_args)
    else:
        print(f"Error: Mode '{mode}' is invalid")
        sys.exit(1)

if __name__ == '__main__':
    main()
