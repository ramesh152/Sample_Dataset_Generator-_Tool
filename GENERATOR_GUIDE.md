# Auto Dataset Generator - Guide

## What This Project Solves

This project generates synthetic image datasets to stress-test Vision-Language Models (VLMs) using controlled visual and rendering artifacts.

Each sample group includes:
- `input.jpg`: clean source rendering
- `expected.jpg`: clean reference rendering
- `A.jpg`: mildly degraded variant
- `B.jpg`: high-quality variant
- `C.jpg`: strongly degraded variant
- `meta.json`: labels, issues, and text bounding boxes

## How It Works

1. Build one realistic background for a sample.
2. Render the sample text on that background.
3. Create A/B/C variants with configurable artifact strengths.
4. Apply degradations in text bounding-box regions.
5. Save structured metadata for downstream evaluation.

## Key Guarantees

- Shared background per sample group:
  `input/expected/A/B/C` are generated from the same background source.
- Bounding-box scoped artifact pipeline:
  effect operations are applied to text regions.
- Traceable metadata:
  per-variant issue labels and `text_bboxes` are stored in `meta.json`.

## Background Families

The generator supports diverse background families:

- Paper textures: plain, ruled, aged/yellow, crumpled, photocopy shadow
- Notebook/Textbook pages: lines, columns, margin-like zones, highlights
- Newspaper: multi-column grayscale print, fold lines, scan-like noise
- Ad/Flyer layouts: promo panels, coupon-like blocks, brochure cards
- Office documents: header/table structures, form-like lines, stamp-like marks
- Screen/UI captures: card layouts, top bars, dashboard/chat-like blocks
- Signage/Outdoor: board/poster-like rectangles on textured surfaces
- Packaging/Labels: label panels and barcode-like regions
- Low-light/Photo-captured: uneven light, shadows, perspective tilt, blur
- Solid colors: subtle texture and vignette for less synthetic appearance
- Plus gradient/noisy/pattern styles

## Artifact Families

Configurable artifacts include:

- Typography artifacts:
  font mismatch, size inconsistency, kerning jitter
- Layout artifacts:
  alignment drift, line-break degradation
- Visual rendering artifacts:
  contrast mismatch (white text pills), line spacing inconsistency
- Styling artifacts:
  missing attribution styling
- Variant degradations:
  blur, noise, JPEG artifacts, color shift, local enhancement

## Variant Behavior

- Variant A (mild): moderate artifact strengths and mild local degradation
- Variant B (best): clean rendering with slight local enhancement
- Variant C (strong): high artifact strengths and strong local degradation

## Metadata Shape

Each `meta.json` includes:

- `sample_id`, `original_text`, `difficulty`
- `variants` with per-variant `type` and `issues`
- `background_consistency`:
  - `shared_source_background_across_group`
  - `artifacts_restricted_to_text_bbox`
- `text_bboxes`: bounding boxes for `input`, `expected`, `A`, `B`, `C`
- `created`

## Quick Start

```powershell
powershell -ExecutionPolicy Bypass -File .\setup_windows.ps1
.\.myenv\Scripts\streamlit run auto_dataset_streamlit.py
```

## Programmatic Usage

```python
from auto_dataset_generator import DatasetGenerator

generator = DatasetGenerator(
    output_dir="./generated_datasets",
    image_size=(800, 600),
    num_samples=100,
)

dataset_path = generator.generate()
print(dataset_path)
```

## Main Files

- `auto_dataset_generator.py`: core engine
- `auto_dataset_streamlit.py`: Streamlit interface
- `START_HERE.txt`: quick operational notes
- `WINDOWS_QUICKSTART.md`: Windows setup
- `README.md`: high-level summary
