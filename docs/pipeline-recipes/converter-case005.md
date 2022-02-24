# Converter Recipe case005

## Goal
Prepare PNG image slices for case005 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case005.nii.gz \
  -o workspace/images/case005 \
  --axis y \
  --rotate 0 \
  --normalize per-slice \
  --prefix case005 \
  --index-width 3 \
  --manifest-json workspace/images/case005-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case005` and masks under `workspace/masks/case005`.
