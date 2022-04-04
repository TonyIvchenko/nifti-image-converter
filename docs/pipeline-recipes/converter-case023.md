# Converter Recipe case023

## Goal
Prepare PNG image slices for case023 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case023.nii.gz \
  -o workspace/images/case023 \
  --axis y \
  --rotate 180 \
  --normalize per-slice \
  --prefix case023 \
  --index-width 3 \
  --manifest-json workspace/images/case023-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case023` and masks under `workspace/masks/case023`.
