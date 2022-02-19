# Converter Recipe case002

## Goal
Prepare PNG image slices for case002 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case002.nii.gz \
  -o workspace/images/case002 \
  --axis y \
  --rotate 90 \
  --normalize global \
  --prefix case002 \
  --index-width 3 \
  --manifest-json workspace/images/case002-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case002` and masks under `workspace/masks/case002`.
