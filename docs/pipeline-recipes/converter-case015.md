# Converter Recipe case015

## Goal
Prepare PNG image slices for case015 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case015.nii.gz \
  -o workspace/images/case015 \
  --axis z \
  --rotate 180 \
  --normalize per-slice \
  --prefix case015 \
  --index-width 3 \
  --manifest-json workspace/images/case015-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case015` and masks under `workspace/masks/case015`.
