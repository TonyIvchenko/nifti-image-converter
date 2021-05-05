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
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    inputfile = args.input
    output_dir = Path(args.output)

    basename = strip_nii_extension(inputfile)

    print('Input file is ', inputfile)
    print('Output folder is ', str(output_dir))

    # set fn as your 3D/4D nifti file
    image_array = nibabel.load(inputfile).get_fdata()
    print(len(image_array.shape))

    # ask if rotate
    ask_rotate = input('Would you like to rotate the orientation? (y/n) ')

    if ask_rotate.lower() == 'y':
        ask_rotate_num = int(input('OK. By 90° 180° or 270°? '))
        if ask_rotate_num == 90 or ask_rotate_num == 180 or ask_rotate_num == 270:
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
                    if ask_rotate.lower() == 'y':
                        if ask_rotate_num == 90 or ask_rotate_num == 180 or ask_rotate_num == 270:
                            print('Rotating image...')
                            data = rotate_slice(
                                image_array[:, :, current_slice, current_volume],
                                ask_rotate_num,
                            )
                    elif ask_rotate.lower() == 'n':
                        data = image_array[:, :, current_slice, current_volume]
                            
                    #alternate slices and save as png
                    print('Saving image...')
                    image_name = basename + "_t" + "{:0>3}".format(str(current_volume+1)) + "_z" + "{:0>3}".format(str(current_slice+1))+ ".png"
                    image_path = output_dir / image_name
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
                if ask_rotate.lower() == 'y':
                    if ask_rotate_num == 90 or ask_rotate_num == 180 or ask_rotate_num == 270:
                        data = rotate_slice(image_array[:, :, current_slice], ask_rotate_num)
                elif ask_rotate.lower() == 'n':
                    data = image_array[:, :, current_slice]

                #alternate slices and save as png
                if (slice_counter % 1) == 0:
                    print('Saving image...')
                    image_name = basename + "_z" + "{:0>3}".format(str(current_slice+1))+ ".png"
                    image_path = output_dir / image_name
                    imageio.imwrite(image_path, normalize_to_uint8(data))
                    print('Saved.')
                    slice_counter += 1

        print('Finished converting images')
    else:
        print('Not a 3D or 4D Image. Please try again.')

# call the function to start the program
if __name__ == "__main__":
   main(sys.argv[1:])
