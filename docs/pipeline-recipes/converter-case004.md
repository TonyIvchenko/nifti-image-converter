# Converter Recipe case004

## Goal
Prepare PNG image slices for case004 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case004.nii.gz \
  -o workspace/images/case004 \
  --axis x \
  --rotate 270 \
  --normalize global \
  --prefix case004 \
  --index-width 3 \
  --manifest-json workspace/images/case004-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case004` and masks under `workspace/masks/case004`.
