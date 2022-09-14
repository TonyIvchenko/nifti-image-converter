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
