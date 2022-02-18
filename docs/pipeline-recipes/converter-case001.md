# Converter Recipe case001

## Goal
Prepare PNG image slices for case001 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case001.nii.gz \
  -o workspace/images/case001 \
  --axis x \
  --rotate 0 \
  --normalize per-slice \
  --prefix case001 \
  --index-width 3 \
  --manifest-json workspace/images/case001-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case001` and masks under `workspace/masks/case001`.
