# Converter Recipe case029

## Goal
Prepare PNG image slices for case029 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case029.nii.gz \
  -o workspace/images/case029 \
  --axis y \
  --rotate 0 \
  --normalize per-slice \
  --prefix case029 \
  --index-width 3 \
  --manifest-json workspace/images/case029-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case029` and masks under `workspace/masks/case029`.
