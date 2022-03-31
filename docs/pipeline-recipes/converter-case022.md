# Converter Recipe case022

## Goal
Prepare PNG image slices for case022 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case022.nii.gz \
  -o workspace/images/case022 \
  --axis x \
  --rotate 90 \
  --normalize global \
  --prefix case022 \
  --index-width 3 \
  --manifest-json workspace/images/case022-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case022` and masks under `workspace/masks/case022`.
