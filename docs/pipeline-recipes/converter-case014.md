# Converter Recipe case014

## Goal
Prepare PNG image slices for case014 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case014.nii.gz \
  -o workspace/images/case014 \
  --axis y \
  --rotate 90 \
  --normalize global \
  --prefix case014 \
  --index-width 3 \
  --manifest-json workspace/images/case014-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case014` and masks under `workspace/masks/case014`.
