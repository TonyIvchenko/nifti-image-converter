# Converter Recipe case030

## Goal
Prepare PNG image slices for case030 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case030.nii.gz \
  -o workspace/images/case030 \
  --axis z \
  --rotate 90 \
  --normalize global \
  --prefix case030 \
  --index-width 3 \
  --manifest-json workspace/images/case030-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case030` and masks under `workspace/masks/case030`.
