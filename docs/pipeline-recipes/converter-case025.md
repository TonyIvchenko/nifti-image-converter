# Converter Recipe case025

## Goal
Prepare PNG image slices for case025 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case025.nii.gz \
  -o workspace/images/case025 \
  --axis x \
  --rotate 0 \
  --normalize per-slice \
  --prefix case025 \
  --index-width 3 \
  --manifest-json workspace/images/case025-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case025` and masks under `workspace/masks/case025`.
