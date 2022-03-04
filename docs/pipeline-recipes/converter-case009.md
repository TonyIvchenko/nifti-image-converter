# Converter Recipe case009

## Goal
Prepare PNG image slices for case009 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case009.nii.gz \
  -o workspace/images/case009 \
  --axis z \
  --rotate 0 \
  --normalize per-slice \
  --prefix case009 \
  --index-width 3 \
  --manifest-json workspace/images/case009-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case009` and masks under `workspace/masks/case009`.
