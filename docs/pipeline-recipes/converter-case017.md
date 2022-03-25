# Converter Recipe case017

## Goal
Prepare PNG image slices for case017 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case017.nii.gz \
  -o workspace/images/case017 \
  --axis y \
  --rotate 0 \
  --normalize per-slice \
  --prefix case017 \
  --index-width 3 \
  --manifest-json workspace/images/case017-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case017` and masks under `workspace/masks/case017`.
