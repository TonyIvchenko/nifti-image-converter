from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import numpy as np


MODULE_PATH = Path(__file__).resolve().parents[1] / "python" / "nii2png.py"
SPEC = spec_from_file_location("nii2png", MODULE_PATH)
nii2png = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(nii2png)


def test_strip_nii_extension_handles_common_inputs():
    assert nii2png.strip_nii_extension("brain.nii") == "brain"
    assert nii2png.strip_nii_extension("brain.nii.gz") == "brain"
    assert nii2png.strip_nii_extension("/tmp/scan/brain_file.nii.gz") == "brain_file"


def test_rotate_slice_rotates_by_quadrants():
    source = np.array([[1, 2], [3, 4]])

    assert np.array_equal(nii2png.rotate_slice(source, 0), source)
    assert np.array_equal(nii2png.rotate_slice(source, 90), np.array([[2, 4], [1, 3]]))
    assert np.array_equal(nii2png.rotate_slice(source, 180), np.array([[4, 3], [2, 1]]))
    assert np.array_equal(nii2png.rotate_slice(source, 270), np.array([[3, 1], [4, 2]]))


def test_build_image_name_formats_3d_and_4d_outputs():
    assert nii2png.build_image_name("scan", slice_index=7) == "scan_z007.png"
    assert nii2png.build_image_name("scan", slice_index=7, volume_index=2) == "scan_t002_z007.png"
    assert nii2png.build_image_name("scan", slice_index=7, axis="x") == "scan_x007.png"


def test_normalize_to_uint8_scales_range():
    source = np.array([[0.0, 2.0], [1.0, 3.0]])
    scaled = nii2png.normalize_to_uint8(source)

    assert scaled.dtype == np.uint8
    assert scaled.min() == 0
    assert scaled.max() == 255


def test_normalize_to_uint8_handles_constant_values():
    source = np.full((2, 2), 4.2)
    scaled = nii2png.normalize_to_uint8(source)

    assert np.array_equal(scaled, np.zeros((2, 2), dtype=np.uint8))


def test_normalize_to_uint8_honors_explicit_bounds():
    source = np.array([[10.0, 20.0], [30.0, 40.0]])
    scaled = nii2png.normalize_to_uint8(source, min_value=10.0, max_value=40.0)

    assert scaled[0, 0] == 0
    assert scaled[1, 1] == 255


def test_compute_global_normalization_bounds():
    source = np.array([[0.0, np.nan], [5.0, np.inf], [-3.0, 2.0]])
    min_value, max_value = nii2png.compute_global_normalization_bounds(source)

    assert min_value == -3.0
    assert max_value == 5.0


def test_iter_slices_for_3d_returns_no_volume_index():
    image = np.arange(2 * 2 * 3).reshape((2, 2, 3))

    slices = list(nii2png.iter_slices(image))

    assert len(slices) == 3
    assert slices[0][0] is None
    assert slices[0][1] == 1
    assert np.array_equal(slices[0][2], image[:, :, 0])


def test_iter_slices_for_3d_supports_axis_selection():
    image = np.arange(2 * 3 * 4).reshape((2, 3, 4))
    slices_x = list(nii2png.iter_slices(image, axis="x"))
    slices_y = list(nii2png.iter_slices(image, axis="y"))

    assert len(slices_x) == 2
    assert len(slices_y) == 3
    assert np.array_equal(slices_x[1][2], image[1, :, :])
    assert np.array_equal(slices_y[2][2], image[:, 2, :])


def test_iter_slices_for_4d_returns_volume_and_slice_indices():
    image = np.arange(2 * 2 * 3 * 2).reshape((2, 2, 3, 2))

    slices = list(nii2png.iter_slices(image))

    assert len(slices) == 6
    first_volume, first_slice, first_data = slices[0]
    assert (first_volume, first_slice) == (1, 1)
    assert np.array_equal(first_data, image[:, :, 0, 0])

    last_volume, last_slice, _ = slices[-1]
    assert (last_volume, last_slice) == (2, 3)


def test_build_manifest_captures_run_metadata():
    manifest = nii2png.build_manifest(
        input_path="scan.nii.gz",
        output_dir="png",
        image_shape=(8, 9, 10),
        axis="z",
        rotate=90,
        dry_run=True,
        normalize="global",
        records=[{"slice_index": 1, "status": "dry_run", "path": "png/scan_z001.png", "volume_index": None}],
    )

    assert manifest["input_path"] == "scan.nii.gz"
    assert manifest["output_dir"] == "png"
    assert manifest["image_shape"] == [8, 9, 10]
    assert manifest["axis"] == "z"
    assert manifest["rotate"] == 90
    assert manifest["dry_run"] is True
    assert manifest["normalize"] == "global"
    assert len(manifest["records"]) == 1
