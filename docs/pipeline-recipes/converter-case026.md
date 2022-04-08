# Converter Recipe case026

## Goal
Prepare PNG image slices for case026 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case026.nii.gz \
  -o workspace/images/case026 \
  --axis y \
  --rotate 90 \
  --normalize global \
  --prefix case026 \
  --index-width 3 \
  --manifest-json workspace/images/case026-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case026` and masks under `workspace/masks/case026`.
