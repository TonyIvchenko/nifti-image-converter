#!/usr/bin/env python3
"""Convert 3D/4D NIfTI images into PNG slices."""

import argparse
import json
import sys
from pathlib import Path

import numpy

import imageio


def strip_nii_extension(path):
    filename = Path(path).name
    if filename.endswith(".nii.gz"):
        return filename[:-7]
    if filename.endswith(".nii"):
        return filename[:-4]
    return Path(path).stem


def build_image_name(base_name, slice_index, volume_index=None, index_width=3, axis="z"):
    if axis not in {"x", "y", "z"}:
        raise ValueError(f"Unsupported axis '{axis}'. Expected one of: x, y, z.")
    if volume_index is None:
        return f"{base_name}_{axis}{slice_index:0{index_width}d}.png"
    return (
        f"{base_name}_t{volume_index:0{index_width}d}_{axis}{slice_index:0{index_width}d}.png"
    )


def rotate_slice(data, degrees):
    if degrees == 0:
        return data
    return numpy.rot90(data, k=degrees // 90)


def normalize_to_uint8(data, min_value=None, max_value=None):
    finite = numpy.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
    if min_value is None or max_value is None:
        min_value = float(finite.min())
        max_value = float(finite.max())
    if max_value == min_value:
        return numpy.zeros(finite.shape, dtype=numpy.uint8)
    scaled = (finite - min_value) / (max_value - min_value)
    return (scaled * 255).astype(numpy.uint8)


def compute_global_normalization_bounds(image_array):
    finite = numpy.nan_to_num(image_array, nan=0.0, posinf=0.0, neginf=0.0)
    return float(finite.min()), float(finite.max())


def iter_slices(image_array, axis="z"):
    axis_to_index = {"x": 0, "y": 1, "z": 2}
    if axis not in axis_to_index:
        raise ValueError(f"Unsupported axis '{axis}'. Expected one of: x, y, z.")
    axis_index = axis_to_index[axis]

    dims = len(image_array.shape)
    if dims == 4:
        total_volumes = image_array.shape[3]
        total_slices = image_array.shape[axis_index]
        for current_volume in range(total_volumes):
            volume_data = image_array[:, :, :, current_volume]
            for current_slice in range(total_slices):
                yield (
                    current_volume + 1,
                    current_slice + 1,
                    numpy.take(volume_data, current_slice, axis=axis_index),
                )
        return

    if dims == 3:
        total_slices = image_array.shape[axis_index]
        for current_slice in range(total_slices):
            yield None, current_slice + 1, numpy.take(image_array, current_slice, axis=axis_index)
        return

    raise ValueError(f"Not a 3D or 4D image. Got shape {image_array.shape}.")


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
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Reduce informational output.",
    )
    parser.add_argument(
        "--axis",
        choices=["x", "y", "z"],
        default="z",
        help="Spatial axis to slice along.",
    )
    parser.add_argument(
        "--manifest-json",
        help="Optional path to write a JSON manifest describing produced slice files.",
    )
    parser.add_argument(
        "--normalize",
        choices=["per-slice", "global"],
        default="per-slice",
        help="Normalization strategy for intensity scaling to uint8.",
    )
    return parser.parse_args(argv)


def build_manifest(
    input_path,
    output_dir,
    image_shape,
    axis,
    rotate,
    dry_run,
    normalize,
    records,
):
    return {
        "input_path": str(input_path),
        "output_dir": str(output_dir),
        "image_shape": list(image_shape),
        "axis": axis,
        "rotate": rotate,
        "dry_run": dry_run,
        "normalize": normalize,
        "records": records,
    }


def main(argv):
    args = parse_args(argv)
    inputfile = args.input
    output_dir = Path(args.output)

    def log(message):
        if not args.quiet:
            print(message)

    if not Path(inputfile).is_file():
        print(f"Input file does not exist: {inputfile}")
        sys.exit(2)

    basename = strip_nii_extension(inputfile)

    log(f"Input file is {inputfile}")
    log(f"Output folder is {str(output_dir)}")

    # set fn as your 3D/4D nifti file
    try:
        import nibabel

        image_array = nibabel.load(inputfile).get_fdata()
    except Exception as exc:
        print(f"Unable to load NIfTI file '{inputfile}': {exc}")
        sys.exit(2)
    log(str(len(image_array.shape)))

    rotation_degrees = 0
    if args.rotate is not None:
        rotation_degrees = args.rotate
        if rotation_degrees == 0:
            log("Rotation disabled via --rotate 0.")
        else:
            log(f"Rotation set to {rotation_degrees} degrees via --rotate.")
    elif args.yes:
        log("Running non-interactively with no rotation.")
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
            log('OK, Your images will be converted it as it is.')
        else:
            print('You must choose either y or n. Quitting...')
            sys.exit()

    if not output_dir.exists():
        output_dir.mkdir(parents=True)
        log("Created ouput directory: " + str(output_dir))

    log('Reading NIfTI file...')

    global_min = None
    global_max = None
    if args.normalize == "global":
        global_min, global_max = compute_global_normalization_bounds(image_array)
        log(
            "Using global normalization bounds: "
            f"min={global_min:.6f}, max={global_max:.6f}"
        )

    written_count = 0
    skipped_count = 0
    preview_count = 0
    records = []

    try:
        slices = iter_slices(image_array, axis=args.axis)
        for volume_index, slice_index, slice_data in slices:
            if rotation_degrees in (90, 180, 270):
                log('Rotating image...')
                slice_data = rotate_slice(slice_data, rotation_degrees)

            log('Saving image...')
            image_name = build_image_name(
                base_name=basename,
                slice_index=slice_index,
                volume_index=volume_index,
                axis=args.axis,
            )
            image_path = output_dir / image_name
            if image_path.exists() and not args.overwrite:
                log(f"Skipping existing file: {image_path}")
                skipped_count += 1
                records.append(
                    {
                        "volume_index": volume_index,
                        "slice_index": slice_index,
                        "path": str(image_path),
                        "status": "skipped_existing",
                    }
                )
                continue
            if args.dry_run:
                log(f"Would write: {image_path}")
                preview_count += 1
                records.append(
                    {
                        "volume_index": volume_index,
                        "slice_index": slice_index,
                        "path": str(image_path),
                        "status": "dry_run",
                    }
                )
                continue
            imageio.imwrite(
                image_path,
                normalize_to_uint8(slice_data, min_value=global_min, max_value=global_max),
            )
            written_count += 1
            records.append(
                {
                    "volume_index": volume_index,
                    "slice_index": slice_index,
                    "path": str(image_path),
                    "status": "written",
                }
            )
            log('Saved.')
    except ValueError as exc:
        print(str(exc))
        sys.exit(2)

    if args.manifest_json:
        manifest_path = Path(args.manifest_json)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest = build_manifest(
            input_path=inputfile,
            output_dir=output_dir,
            image_shape=image_array.shape,
            axis=args.axis,
            rotate=rotation_degrees,
            dry_run=args.dry_run,
            normalize=args.normalize,
            records=records,
        )
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        log(f"Wrote manifest JSON to {manifest_path}")

    if args.dry_run:
        print(f"Dry run complete. {preview_count} files would be written ({skipped_count} skipped).")
    else:
        print(f"Finished converting images. {written_count} files written ({skipped_count} skipped).")

# call the function to start the program
if __name__ == "__main__":
   main(sys.argv[1:])
