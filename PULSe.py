import argparse
import os
import sys

# We import the functionality from image_gen_ms directly.
# This assumes image_gen_ms.py is in the same directory.
try:
    import image_gen_ms
except ImportError:
    print("Error: Could not import 'image_gen_ms.py'. Please ensure it exists.", file=sys.stderr)
    sys.exit(1)


def main():
    # Create the main parser for the wrapper script
    parser = argparse.ArgumentParser(description='Wrapper script for different modes.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    
    # We will use subparsers to handle the different modes.
    # The 'dest' argument will store the name of the subparser chosen.
    subparsers = parser.add_subparsers(dest='mode', required=True,
                                        help='Available modes:\n'
                                        '  image_gen_ms  Run the image generation script.')
    
    # Create a subparser for the 'image_gen_ms' mode.
    # The 'add_parser' call is where we add all the arguments for the child script.
    image_gen_ms_parser = subparsers.add_parser('image_gen_ms',
                                                help=image_gen_ms.get_parser().format_help())
    
    # Add the arguments from the image_gen_ms script to this subparser
    image_gen_ms.add_args_to_parser(image_gen_ms_parser)

    # Parse the arguments.
    args = parser.parse_args()
    
    # Based on the subparser chosen, call the main function of the corresponding script.
    if args.mode == 'image_gen_ms':
        image_gen_ms.main(args)


if __name__ == '__main__':
    main()

