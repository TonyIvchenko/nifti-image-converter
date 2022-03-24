# Converter Recipe case016

## Goal
Prepare PNG image slices for case016 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case016.nii.gz \
  -o workspace/images/case016 \
  --axis x \
  --rotate 270 \
  --normalize global \
  --prefix case016 \
  --index-width 3 \
  --manifest-json workspace/images/case016-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case016` and masks under `workspace/masks/case016`.
