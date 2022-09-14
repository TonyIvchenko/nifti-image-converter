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
