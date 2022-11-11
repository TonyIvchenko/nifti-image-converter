from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "python" / "manifest_helpers.py"
SPEC = spec_from_file_location("manifest_helpers", MODULE_PATH)
manifest_helpers = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(manifest_helpers)


def _sample_manifest():
    return {
        "input_path": "scan.nii.gz",
        "output_dir": "out",
        "axis": "z",
        "rotate": 90,
        "normalize": "global",
        "dry_run": False,
        "image_shape": [256, 256, 32],
        "records": [
            {"status": "written", "path": "out/a.png", "slice_index": 1, "volume_index": 1},
            {"status": "written", "path": "out/b.png", "slice_index": 2, "volume_index": 1},
            {"status": "skipped_existing", "path": "out/c.png", "slice_index": 4, "volume_index": 1},
            {"status": "dry_run", "path": "out/d.png", "slice_index": 5, "volume_index": 2},
            {"status": "error", "path": "out/e.png", "slice_index": 6, "volume_index": 2},
            {"status": "weird", "path": "out/e.png", "slice_index": 7, "volume_index": 2},
        ],
    }


def test_converter_input_path():
    assert manifest_helpers.converter_input_path(_sample_manifest()) == "scan.nii.gz"


def test_converter_output_dir():
    assert manifest_helpers.converter_output_dir(_sample_manifest()) == "out"


def test_converter_axis():
    assert manifest_helpers.converter_axis(_sample_manifest()) == "z"


def test_converter_rotation():
    assert manifest_helpers.converter_rotation(_sample_manifest()) == 90


def test_converter_normalization():
    assert manifest_helpers.converter_normalization(_sample_manifest()) == "global"


def test_converter_is_dry_run():
    assert manifest_helpers.converter_is_dry_run(_sample_manifest()) is False


def test_converter_image_shape():
    assert manifest_helpers.converter_image_shape(_sample_manifest()) == [256, 256, 32]


def test_converter_records():
    assert len(manifest_helpers.converter_records(_sample_manifest())) == 6


def test_converter_record_count():
    assert manifest_helpers.converter_record_count(_sample_manifest()) == 6


def test_converter_written_count():
    assert manifest_helpers.converter_written_count(_sample_manifest()) == 2


def test_converter_skipped_count():
    assert manifest_helpers.converter_skipped_count(_sample_manifest()) == 1


def test_converter_dry_run_count():
    assert manifest_helpers.converter_dry_run_count(_sample_manifest()) == 1


def test_converter_error_count():
    assert manifest_helpers.converter_error_count(_sample_manifest()) == 1


def test_converter_all_paths():
    assert len(manifest_helpers.converter_all_paths(_sample_manifest())) == 6


def test_converter_written_paths():
    assert manifest_helpers.converter_written_paths(_sample_manifest()) == ["out/a.png", "out/b.png"]


def test_converter_skipped_paths():
    assert manifest_helpers.converter_skipped_paths(_sample_manifest()) == ["out/c.png"]


def test_converter_dry_run_paths():
    assert manifest_helpers.converter_dry_run_paths(_sample_manifest()) == ["out/d.png"]
