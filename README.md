# Auto Dataset Generator

Synthetic dataset generator for evaluating Vision-Language Models (VLMs) under controlled quality and rendering failures.

## What problem this project solves

Real VLM failures are often caused by visual artifacts (blur, compression, typography/layout mistakes), not just text content.
This project creates reproducible A/B/C comparison sets so teams can test those failure modes at scale.

For each sample, it generates:

- `input.jpg`: clean source rendering
- `expected.jpg`: reference target (clean)
- `A.jpg`: mildly degraded candidate
- `B.jpg`: high-quality candidate
- `C.jpg`: strongly degraded candidate
- `meta.json`: labels, issues, and per-image text bounding boxes

## How it solves it

1. Builds a realistic synthetic background from multiple families (paper, newspaper, office docs, UI, signage, packaging, low-light, etc.).
2. Renders text once as a baseline sample.
3. Produces A/B/C variants with configurable artifact strengths.
4. Applies degradations only inside the rendered text bounding box.
5. Keeps one shared source background across `input/expected/A/B/C` for each sample group.
6. Records metadata (`issues`, `text_bboxes`, `background_consistency`) for downstream analysis.

## Key guarantees

- Shared background per sample group: `input/expected/A/B/C` originate from the same background image.
- BBox-scoped effects: artifact operations are restricted to text regions.
- Traceable metadata: each sample contains artifact labels and per-variant text boxes.

## Quick start

```powershell
powershell -ExecutionPolicy Bypass -File .\setup_windows.ps1
.\.myenv\Scripts\streamlit run auto_dataset_streamlit.py
```

## Main files

- `auto_dataset_generator.py`: core generation engine
- `auto_dataset_streamlit.py`: web UI
- `GENERATOR_GUIDE.md`: detailed guide and examples
- `START_HERE.txt`: short operational guide
- `WINDOWS_QUICKSTART.md`: Windows environment bootstrap
