# Converter Recipe case024

## Goal
Prepare PNG image slices for case024 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case024.nii.gz \
  -o workspace/images/case024 \
  --axis z \
  --rotate 270 \
  --normalize global \
  --prefix case024 \
  --index-width 3 \
  --manifest-json workspace/images/case024-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case024` and masks under `workspace/masks/case024`.
