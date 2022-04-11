# Converter Recipe case027

## Goal
Prepare PNG image slices for case027 using repeatable settings.

## Commands
```bash
cd ~/git/nifti-image-converter
python3 python/nii2png.py \
  -i data/case027.nii.gz \
  -o workspace/images/case027 \
  --axis z \
  --rotate 180 \
  --normalize per-slice \
  --prefix case027 \
  --index-width 3 \
  --manifest-json workspace/images/case027-manifest.json \
  --yes
```

## Integration Notes
- Keep `--prefix`, `--axis`, and `--index-width` aligned with `lungmask` export settings.
- Keep images under `workspace/images/case027` and masks under `workspace/masks/case027`.
