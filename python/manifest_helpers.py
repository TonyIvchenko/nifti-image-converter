"""Helpers for querying converter manifest payloads."""


def _records(manifest):
    return list(manifest.get("records", []))


def _status_counts(records):
    counts = {}
    for record in records:
        status = record.get("status", "unknown")
        counts[status] = counts.get(status, 0) + 1
    return counts


def converter_input_path(manifest):
    return manifest.get("input_path")


def converter_output_dir(manifest):
    return manifest.get("output_dir")


def converter_axis(manifest):
    return manifest.get("axis")


def converter_rotation(manifest):
    return manifest.get("rotate")


def converter_normalization(manifest):
    return manifest.get("normalize")


def converter_is_dry_run(manifest):
    return bool(manifest.get("dry_run"))


def converter_image_shape(manifest):
    return manifest.get("image_shape")


def converter_records(manifest):
    return _records(manifest)


def converter_record_count(manifest):
    return len(_records(manifest))


def converter_written_count(manifest):
    return sum(1 for record in _records(manifest) if record.get("status") == "written")


def converter_skipped_count(manifest):
    return sum(1 for record in _records(manifest) if record.get("status") == "skipped_existing")


def converter_dry_run_count(manifest):
    return sum(1 for record in _records(manifest) if record.get("status") == "dry_run")


def converter_error_count(manifest):
    return sum(1 for record in _records(manifest) if record.get("status") == "error")


def converter_all_paths(manifest):
    return [record.get("path") for record in _records(manifest) if record.get("path")]


def converter_written_paths(manifest):
    return [record.get("path") for record in _records(manifest) if record.get("status") == "written" and record.get("path")]


def converter_skipped_paths(manifest):
    return [record.get("path") for record in _records(manifest) if record.get("status") == "skipped_existing" and record.get("path")]


def converter_dry_run_paths(manifest):
    return [record.get("path") for record in _records(manifest) if record.get("status") == "dry_run" and record.get("path")]


def converter_error_paths(manifest):
    return [record.get("path") for record in _records(manifest) if record.get("status") == "error" and record.get("path")]


def converter_has_records(manifest):
    return bool(_records(manifest))


def converter_is_empty(manifest):
    return not _records(manifest)


def converter_wrote_anything(manifest):
    return converter_written_count(manifest) > 0


def converter_is_dry_run_only(manifest):
    records = _records(manifest)
    return bool(records) and all(record.get("status") == "dry_run" for record in records)


def converter_has_duplicate_paths(manifest):
    paths = converter_all_paths(manifest)
    return len(paths) != len(set(paths))


def converter_duplicate_paths(manifest):
    counts = {}
    for path in converter_all_paths(manifest):
        counts[path] = counts.get(path, 0) + 1
    return sorted([path for path, count in counts.items() if count > 1])


def converter_unique_path_count(manifest):
    return len(set(converter_all_paths(manifest)))
