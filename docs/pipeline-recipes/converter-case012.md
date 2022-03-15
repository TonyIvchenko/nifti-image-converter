# Converter Recipe case012

## Goal
Prepare PNG image slices for case012 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case012.nii.gz \
  -o workspace/images/case012 \
  --axis z \
  --rotate 270 \
  --normalize global \
  --prefix case012 \
  --index-width 3 \
  --manifest-json workspace/images/case012-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case012` and masks under `workspace/masks/case012`.
