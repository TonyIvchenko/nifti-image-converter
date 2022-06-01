# Clarify how we handle four-dimensional volumes

## Why this matters
Consistent converter settings make downstream mask export and training pairing predictable.

## Quick command
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/sample.nii.gz \
  -o workspace/images \
  --axis z \
  --prefix sample \
  --index-width 3 \
  --manifest-json workspace/images/manifest.json \
  --yes
```

## What to check
- Filenames stay stable across reruns.
- Manifest and PNG outputs are generated together.
