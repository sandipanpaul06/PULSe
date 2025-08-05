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
    parser.add_argument('-pref', type=str, help='File prefix for image_gen_ms and image_generation_vcf')
    parser.add_argument('-out', type=str, help='Output file name for image_gen_ms')
    parser.add_argument('-nHap', type=int, help='Number of haplotypes for image_gen_ms and image_generation_vcf')
    parser.add_argument('-subFolder', type=str, help='Subfolder name for image_gen_ms')
    parser.add_argument('-n', type=int, help='Number of files for image_gen_ms and image_generation_vcf')
    parser.add_argument('-start', type=int, help='Start number of files for image_gen_ms and image_generation_vcf')
    parser.add_argument('-stop', type=int, help='Stop number of files for image_generation_vcf')
    parser.add_argument('-imgDim', type=int, help='Image dimension for image_gen_ms and image_generation_vcf')
    parser.add_argument('-fileName', type=str, help='File name for preprocess_vcf and prediction')
    parser.add_argument('-outFolder', type=str, help='Output folder for preprocess_vcf')
    parser.add_argument('-split', type=float, help='Train/test split for train mode')
    parser.add_argument('-modelName', type=str, help='Name of model for train and prediction')
    parser.add_argument('-Sw', type=str, help='Sweep file for train mode')
    parser.add_argument('-Ne', type=str, help='Neutral file for train mode')
    parser.add_argument('-subfolder', type=str, help='Subfolder for image_generation_vcf')
    parser.add_argument('-outDat', type=str, help='Output dataset name for image_generation_vcf')

    args = parser.parse_args()
    mode = args.mode

    # A dictionary to hold the arguments we will pass to the child script.
    script_args = {}

    # Validate arguments for each mode
    if mode == 'image_gen_ms':
        required_args = ['pref', 'out', 'nHap', 'subFolder', 'n', 'start']
        invalid_args = ['fileName', 'outFolder', 'split', 'modelName', 'Sw', 'Ne', 'stop', 'outDat', 'subfolder', 'imgDim']
    elif mode == 'train':
        required_args = ['Sw', 'Ne', 'split', 'modelName']
        invalid_args = ['pref', 'out', 'nHap', 'subFolder', 'n', 'start', 'imgDim', 'stop', 'outDat', 'subfolder']
    elif mode == 'preprocess_vcf':
        required_args = ['fileName', 'outFolder']
        invalid_args = ['pref', 'out', 'nHap', 'subFolder', 'n', 'start', 'imgDim', 'split', 'modelName', 'Sw', 'Ne', 'stop', 'outDat', 'subfolder']
    elif mode == 'image_generation_vcf':
        required_args = ['subfolder', 'nHap', 'pref', 'start', 'stop', 'imgDim', 'outDat']
        invalid_args = ['fileName', 'outFolder', 'split', 'modelName', 'Sw', 'Ne']
    elif mode == 'prediction':
        required_args = ['fileName', 'modelName']
        invalid_args = ['pref', 'out', 'nHap', 'subFolder', 'n', 'start', 'imgDim', 'split', 'Sw', 'Ne', 'stop', 'outDat', 'subfolder']
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
        'image_generation_vcf': 'image_generation_vcf.py',
        'prediction': 'prediction.py'
    }

    if mode in script_mapping:
        script_name = script_mapping[mode]
        run_script(script_name, script_args)
    else:
        print(f"Error: Mode '{mode}' is invalid")
        sys.exit(1)

if __name__ == '__main__':
    main()
