# Converter Recipe case018

## Goal
Prepare PNG image slices for case018 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case018.nii.gz \
  -o workspace/images/case018 \
  --axis z \
  --rotate 90 \
  --normalize global \
  --prefix case018 \
  --index-width 3 \
  --manifest-json workspace/images/case018-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case018` and masks under `workspace/masks/case018`.
