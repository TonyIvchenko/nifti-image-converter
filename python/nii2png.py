#!/usr/bin/env python3
"""Convert 3D/4D NIfTI images into PNG slices."""

import argparse
import sys
from pathlib import Path

import nibabel
import numpy

import imageio


def strip_nii_extension(path):
    filename = Path(path).name
    if filename.endswith(".nii.gz"):
        return filename[:-7]
    if filename.endswith(".nii"):
        return filename[:-4]
    return Path(path).stem


def rotate_slice(data, degrees):
    if degrees == 0:
        return data
    return numpy.rot90(data, k=degrees // 90)


def normalize_to_uint8(data):
    finite = numpy.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
    min_value = float(finite.min())
    max_value = float(finite.max())
    if max_value == min_value:
        return numpy.zeros(finite.shape, dtype=numpy.uint8)
    scaled = (finite - min_value) / (max_value - min_value)
    return (scaled * 255).astype(numpy.uint8)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="nii2png.py",
        description="Convert 3D/4D NIfTI images into PNG slices.",
    )
    parser.add_argument("-i", "--input", required=True, help="Path to input .nii/.nii.gz file.")
    parser.add_argument("-o", "--output", required=True, help="Path to output directory for PNG files.")
    parser.add_argument(
        "-r",
        "--rotate",
        type=int,
        choices=[0, 90, 180, 270],
        help="Rotate output slices by this degree value.",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Run non-interactively with default answers.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite PNG files if they already exist.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print intended output files without writing them.",
    )
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    inputfile = args.input
    output_dir = Path(args.output)

    if not Path(inputfile).is_file():
        print(f"Input file does not exist: {inputfile}")
        sys.exit(2)

    basename = strip_nii_extension(inputfile)

    print('Input file is ', inputfile)
    print('Output folder is ', str(output_dir))

    # set fn as your 3D/4D nifti file
    try:
        image_array = nibabel.load(inputfile).get_fdata()
    except Exception as exc:
        print(f"Unable to load NIfTI file '{inputfile}': {exc}")
        sys.exit(2)
    print(len(image_array.shape))

    rotation_degrees = 0
    if args.rotate is not None:
        rotation_degrees = args.rotate
        if rotation_degrees == 0:
            print("Rotation disabled via --rotate 0.")
        else:
            print(f"Rotation set to {rotation_degrees} degrees via --rotate.")
    elif args.yes:
        print("Running non-interactively with no rotation.")
    else:
        ask_rotate = input('Would you like to rotate the orientation? (y/n) ')

        if ask_rotate.lower() == 'y':
            ask_rotate_num = int(input('OK. By 90° 180° or 270°? '))
            if ask_rotate_num == 90 or ask_rotate_num == 180 or ask_rotate_num == 270:
                rotation_degrees = ask_rotate_num
                print('Got it. Your images will be rotated by {} degrees.'.format(ask_rotate_num))
            else:
                print('You must enter a value that is either 90, 180, or 270. Quitting...')
                sys.exit()
        elif ask_rotate.lower() == 'n':
            print('OK, Your images will be converted it as it is.')
        else:
            print('You must choose either y or n. Quitting...')
            sys.exit()

    # if 4D image inputted
    if len(image_array.shape) == 4:
        # set 4d array dimension values
        nx, ny, nz, nw = image_array.shape

        # set destination folder
        if not output_dir.exists():
            output_dir.mkdir(parents=True)
            print("Created ouput directory: " + str(output_dir))

        print('Reading NIfTI file...')

        total_volumes = image_array.shape[3]
        total_slices = image_array.shape[2]

        # iterate through volumes
        for current_volume in range(0, total_volumes):
            slice_counter = 0
            # iterate through slices
            for current_slice in range(0, total_slices):
                if (slice_counter % 1) == 0:
                    # rotate or no rotate
                    if rotation_degrees in (90, 180, 270):
                        print('Rotating image...')
                        data = rotate_slice(
                            image_array[:, :, current_slice, current_volume],
                            rotation_degrees,
                        )
                    else:
                        data = image_array[:, :, current_slice, current_volume]
                            
                    #alternate slices and save as png
                    print('Saving image...')
                    image_name = basename + "_t" + "{:0>3}".format(str(current_volume+1)) + "_z" + "{:0>3}".format(str(current_slice+1))+ ".png"
                    image_path = output_dir / image_name
                    if image_path.exists() and not args.overwrite:
                        print(f"Skipping existing file: {image_path}")
                        continue
                    if args.dry_run:
                        print(f"Would write: {image_path}")
                        continue
                    imageio.imwrite(image_path, normalize_to_uint8(data))
                    print('Saved.')
                    slice_counter += 1

        print('Finished converting images')

    # else if 3D image inputted
    elif len(image_array.shape) == 3:
        # set 4d array dimension values
        nx, ny, nz = image_array.shape

        # set destination folder
        if not output_dir.exists():
            output_dir.mkdir(parents=True)
            print("Created ouput directory: " + str(output_dir))

        print('Reading NIfTI file...')

        total_slices = image_array.shape[2]

        slice_counter = 0
        # iterate through slices
        for current_slice in range(0, total_slices):
            # alternate slices
            if (slice_counter % 1) == 0:
                # rotate or no rotate
                if rotation_degrees in (90, 180, 270):
                    data = rotate_slice(image_array[:, :, current_slice], rotation_degrees)
                else:
                    data = image_array[:, :, current_slice]

                #alternate slices and save as png
                if (slice_counter % 1) == 0:
                    print('Saving image...')
                    image_name = basename + "_z" + "{:0>3}".format(str(current_slice+1))+ ".png"
                    image_path = output_dir / image_name
                    if image_path.exists() and not args.overwrite:
                        print(f"Skipping existing file: {image_path}")
                        continue
                    if args.dry_run:
                        print(f"Would write: {image_path}")
                        continue
                    imageio.imwrite(image_path, normalize_to_uint8(data))
                    print('Saved.')
                    slice_counter += 1

        print('Finished converting images')
    else:
        print(f"Not a 3D or 4D image. Got shape {image_array.shape}.")
        sys.exit(2)

# call the function to start the program
if __name__ == "__main__":
   main(sys.argv[1:])
