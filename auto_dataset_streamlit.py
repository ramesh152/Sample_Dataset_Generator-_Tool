"""
Auto Dataset Generator - Streamlit Web Interface
Interactive tool for generating VLM stress-test datasets at scale
"""

import streamlit as st
import os
import shutil
from pathlib import Path
from datetime import datetime
import json
import pandas as pd
from typing import Optional

from auto_dataset_generator import DatasetGenerator

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Auto Dataset Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    :root {
        --primary: #2563eb;
        --primary-dark: #1e40af;
        --success: #059669;
        --warning: #f59e0b;
    }
    
    .generator-card {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        color: white;
        padding: 2rem;
        border-radius: 0.75rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .status-box {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

if 'generator' not in st.session_state:
    st.session_state.generator = None
if 'generated_dataset' not in st.session_state:
    st.session_state.generated_dataset = None
if 'generation_complete' not in st.session_state:
    st.session_state.generation_complete = False

# ============================================================================
# HEADER
# ============================================================================

col1, col2 = st.columns([1, 5])
with col1:
    st.write("# 🎬")
with col2:
    st.write("# Auto Dataset Generator")
    st.caption("*Generate synthetic VLM stress-test datasets at scale*")

st.divider()

# ============================================================================
# MAIN TABS
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Generate Dataset",
    "📊 Dataset Info",
    "📥 Manage Datasets",
    "❓ Help"
])

# ============================================================================
# TAB 1: GENERATE DATASET
# ============================================================================

with tab1:
    st.write("### Generate New Dataset")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num_samples = st.slider(
            "Number of Samples",
            min_value=10,
            max_value=10000,
            value=100,
            step=10,
            help="Generate 10-10,000 image samples"
        )
    
    with col2:
        width = st.slider(
            "Image Width (px)",
            min_value=256,
            max_value=2048,
            value=800,
            step=64
        )
    
    with col3:
        height = st.slider(
            "Image Height (px)",
            min_value=256,
            max_value=2048,
            value=600,
            step=64
        )
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Dataset Options")
        
        dataset_name = st.text_input(
            "Custom Dataset Name (optional)",
            value="",
            help="Leave empty for auto-generated name"
        )
        
        output_format = st.radio(
            "Output Format",
            ["JPG (smaller files)", "PNG (lossless)"],
            help="Image format for dataset"
        )
        
        include_metadata = st.checkbox(
            "Include Metadata",
            value=True,
            help="Create meta.json for each sample"
        )
    
    with col2:
        st.write("#### Quality Settings")
        
        quality_level = st.select_slider(
            "Base Quality Level",
            options=["Low", "Medium", "High", "Ultra"],
            value="High",
            help="Controls JPEG compression and clarity"
        )
        
        variation_strength = st.slider(
            "Variation Strength",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="How extreme the A/B/C differences are"
        )
        
        seed_mode = st.radio(
            "Reproducibility",
            ["Random (Different each time)", "Fixed Seed (Consistent)"],
            help="Use fixed seed for reproducible datasets"
        )

        st.divider()
        st.write("#### Typography Artifact Settings")
        enable_typography_artifacts = st.checkbox(
            "Enable Typography Artifacts (A/C)",
            value=True,
            help="Adds font mismatch, size inconsistency, and kerning jitter in A/C variants"
        )
        typography_artifact_strength_a = st.slider(
            "Artifact Strength - A (mild)",
            min_value=0.0,
            max_value=1.0,
            value=0.35,
            step=0.05,
            disabled=not enable_typography_artifacts
        )
        typography_artifact_strength_c = st.slider(
            "Artifact Strength - C (strong)",
            min_value=0.0,
            max_value=1.0,
            value=0.85,
            step=0.05,
            disabled=not enable_typography_artifacts
        )

        st.divider()
        st.write("#### Layout Artifact Settings")
        enable_layout_artifacts = st.checkbox(
            "Enable Layout Artifacts (A/C)",
            value=True,
            help="Adds center-alignment drift and semantic line-break degradation in A/C variants"
        )
        layout_artifact_strength_a = st.slider(
            "Layout Strength - A (mild)",
            min_value=0.0,
            max_value=1.0,
            value=0.25,
            step=0.05,
            disabled=not enable_layout_artifacts
        )
        layout_artifact_strength_c = st.slider(
            "Layout Strength - C (strong)",
            min_value=0.0,
            max_value=1.0,
            value=0.70,
            step=0.05,
            disabled=not enable_layout_artifacts
        )

        st.divider()
        st.write("#### Visual Artifact Settings")
        enable_visual_artifacts = st.checkbox(
            "Enable Visual Rendering Artifacts (A/C)",
            value=True,
            help="Adds contrast mismatch (white text boxes) and inconsistent line spacing in A/C variants"
        )
        visual_artifact_strength_a = st.slider(
            "Visual Strength - A (mild)",
            min_value=0.0,
            max_value=1.0,
            value=0.30,
            step=0.05,
            disabled=not enable_visual_artifacts
        )
        visual_artifact_strength_c = st.slider(
            "Visual Strength - C (strong)",
            min_value=0.0,
            max_value=1.0,
            value=0.80,
            step=0.05,
            disabled=not enable_visual_artifacts
        )

        st.divider()
        st.write("#### Styling Artifact Settings")
        enable_styling_artifacts = st.checkbox(
            "Enable Missing Attribution Styling (A/C)",
            value=True,
            help="Makes attribution line lose its visual hierarchy/separation and blend into body text"
        )
        styling_artifact_strength_a = st.slider(
            "Styling Strength - A (mild)",
            min_value=0.0,
            max_value=1.0,
            value=0.25,
            step=0.05,
            disabled=not enable_styling_artifacts
        )
        styling_artifact_strength_c = st.slider(
            "Styling Strength - C (strong)",
            min_value=0.0,
            max_value=1.0,
            value=0.70,
            step=0.05,
            disabled=not enable_styling_artifacts
        )
    
    st.divider()
    
    # Display estimated info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        est_size = (num_samples * 5 * (width * height * 3 / 1024 / 1024)) / 1024
        st.metric("Estimated Dataset Size", f"{est_size:.1f} MB")
    
    with col2:
        est_time = num_samples * 0.5 / 60  # ~0.5 seconds per sample
        st.metric("Est. Generation Time", f"{est_time:.1f} min")
    
    with col3:
        total_images = num_samples * 5
        st.metric("Total Images", f"{total_images:,}")
    
    st.divider()
    
    # Generate button
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🎬 Generate Dataset", type="primary", use_container_width=True):
            with st.spinner("🔄 Generating dataset... This may take a moment"):
                try:
                    # Initialize generator
                    generator = DatasetGenerator(
                        output_dir="./generated_datasets",
                        image_size=(width, height),
                        num_samples=num_samples,
                        enable_typography_artifacts=enable_typography_artifacts,
                        typography_artifact_strength_a=typography_artifact_strength_a,
                        typography_artifact_strength_c=typography_artifact_strength_c,
                        enable_layout_artifacts=enable_layout_artifacts,
                        layout_artifact_strength_a=layout_artifact_strength_a,
                        layout_artifact_strength_c=layout_artifact_strength_c,
                        enable_visual_artifacts=enable_visual_artifacts,
                        visual_artifact_strength_a=visual_artifact_strength_a,
                        visual_artifact_strength_c=visual_artifact_strength_c,
                        enable_styling_artifacts=enable_styling_artifacts,
                        styling_artifact_strength_a=styling_artifact_strength_a,
                        styling_artifact_strength_c=styling_artifact_strength_c
                    )
                    
                    # Generate
                    dataset_path = generator.generate()
                    
                    st.session_state.generated_dataset = dataset_path
                    st.session_state.generation_complete = True
                    
                    st.success(f"✅ Dataset generated successfully!")
                    st.balloons()
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        if st.button("📋 Show Log", use_container_width=True):
            st.info("Generation logs would appear here in production")
    
    # Display result
    if st.session_state.generation_complete and st.session_state.generated_dataset:
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="status-box">
                <strong>✅ Generation Complete!</strong><br/>
                Dataset is ready for evaluation and testing.
            </div>
            """, unsafe_allow_html=True)
            
            st.write("**Next Steps:**")
            st.write("""
            1. Review dataset info in "📊 Dataset Info" tab
            2. Download dataset for use with VLM Judge
            3. Stress-test your VLM system
            4. Analyze results
            """)
        
        with col2:
            dataset_path = Path(st.session_state.generated_dataset)
            
            st.write("**Dataset Details:**")
            st.write(f"""
            - **Location:** {dataset_path.name}
            - **Samples:** {num_samples}
            - **Images:** {num_samples * 5}
            - **Size:** ~{(num_samples * 5 * (width * height * 3 / 1024 / 1024)) / 1024:.1f} MB
            """)
            
            # Create download button
            if st.button("📥 Download Dataset", use_container_width=True):
                st.info("In production, this would create a ZIP file for download")

# ============================================================================
# TAB 2: DATASET INFO
# ============================================================================

with tab2:
    st.write("### Dataset Information")
    
    if st.session_state.generated_dataset:
        dataset_path = Path(st.session_state.generated_dataset)
        manifest_path = dataset_path / "manifest.json"
        
        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            # Overview
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Samples", manifest['total_samples'])
            with col2:
                st.metric("Total Images", manifest['total_samples'] * 5)
            with col3:
                image_size = manifest['image_size']
                st.metric("Image Size", f"{image_size[0]}×{image_size[1]}")
            with col4:
                st.metric("Created", manifest['created'][:10])
            
            st.divider()
            
            # Sample browser
            st.write("### Browse Samples")
            
            sample_idx = st.slider(
                "Select Sample",
                min_value=0,
                max_value=manifest['total_samples'] - 1,
                value=0
            )
            
            sample = manifest['samples'][sample_idx]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Sample:** {sample['sample_id']}")
                st.write(f"**Difficulty:** {sample['difficulty']:.1%}")
                st.write(f"**Original Text:** {sample['original_text'][:100]}...")
            
            with col2:
                st.write("**Variants:**")
                for variant_name, variant_info in sample['variants'].items():
                    st.write(f"- **{variant_name}:** {variant_info['type']}")
            
            st.divider()
            
            # Statistics
            st.write("### Dataset Statistics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Difficulty Distribution:**")
                difficulties = [s['difficulty'] for s in manifest['samples']]
                
                df_diff = pd.DataFrame({
                    'Difficulty Level': ['Easy (0-0.2)', 'Medium (0.2-0.4)', 'Hard (0.4-0.6)', 'Very Hard (0.6+)'],
                    'Count': [
                        len([d for d in difficulties if d < 0.2]),
                        len([d for d in difficulties if 0.2 <= d < 0.4]),
                        len([d for d in difficulties if 0.4 <= d < 0.6]),
                        len([d for d in difficulties if d >= 0.6]),
                    ]
                })
                
                st.bar_chart(df_diff.set_index('Difficulty Level'))
            
            with col2:
                st.write("**Variant Composition:**")
                
                variant_counts = {
                    'Input': manifest['total_samples'],
                    'Expected': manifest['total_samples'],
                    'A (Flawed)': manifest['total_samples'],
                    'B (Best)': manifest['total_samples'],
                    'C (Bad)': manifest['total_samples'],
                }
                
                df_var = pd.DataFrame(list(variant_counts.items()), columns=['Type', 'Count'])
                st.bar_chart(df_var.set_index('Type'))
        
        else:
            st.warning("Manifest not found")
    
    else:
        st.info("Generate a dataset first to see information")

# ============================================================================
# TAB 3: MANAGE DATASETS
# ============================================================================

with tab3:
    st.write("### Manage Generated Datasets")
    
    datasets_dir = Path("./generated_datasets")
    datasets_dir.mkdir(parents=True, exist_ok=True)
    
    # List datasets
    datasets = sorted([d for d in datasets_dir.glob("VLM_Dataset_*") if d.is_dir()])
    
    if datasets:
        st.write(f"**Found {len(datasets)} dataset(s)**")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write("Dataset Name")
        with col2:
            st.write("Size")
        with col3:
            st.write("Action")
        
        st.divider()
        
        for dataset in datasets:
            # Calculate size
            total_size = sum(
                f.stat().st_size for f in dataset.rglob("*") if f.is_file()
            ) / (1024 * 1024)  # MB
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"`{dataset.name}`")
            with col2:
                st.write(f"{total_size:.1f} MB")
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{dataset.name}"):
                    try:
                        shutil.rmtree(dataset)
                        st.success(f"Deleted {dataset.name}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        st.divider()
        
        # Bulk actions
        st.write("### Bulk Operations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export All Manifests", use_container_width=True):
                st.info("Would export all manifest.json files")
        
        with col2:
            if st.button("🗑️ Clear All Datasets", use_container_width=True):
                if st.checkbox("Confirm deletion"):
                    for dataset in datasets:
                        try:
                            shutil.rmtree(dataset)
                        except:
                            pass
                    st.success("All datasets cleared")
                    st.rerun()
    
    else:
        st.info("No datasets generated yet. Go to 'Generate Dataset' tab to create one.")

# ============================================================================
# TAB 4: HELP
# ============================================================================

with tab4:
    st.write("### Help & Documentation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("## 🎯 What This Tool Does")
        st.write("""
        Generates synthetic VLM evaluation datasets with:
        - **input.jpg** - Original image with source text
        - **expected.jpg** - Perfect translated version
        - **A.jpg** - Slightly flawed
        - **B.jpg** - Best quality (near perfect)
        - **C.jpg** - Bad quality (clearly wrong)
        - **meta.json** - Labels and metadata
        
        Generates 10-10,000 samples with controlled variations.
        """)
    
    with col2:
        st.write("## 📊 Dataset Structure")
        st.code("""
dataset/
 img_0001/
  ├── input.jpg
  ├── expected.jpg
  ├── A.jpg
  ├── B.jpg
  ├── C.jpg
  └── meta.json
 img_0002/
  └── ...
 manifest.json
        """)
    
    st.divider()
    
    st.write("## ❓ FAQ")
    
    with st.expander("How many samples should I generate?"):
        st.write("""
        - **Quick test:** 10-50 samples (instant, ~1 MB)
        - **Evaluation:** 100-500 samples (quick, ~50-250 MB)
        - **Stress test:** 1000-5000 samples (slow, ~500 MB - 2.5 GB)
        - **Large scale:** 5000-10000 samples (very slow, ~2.5-5 GB)
        
        Recommendation: Start with 100, increase as needed.
        """)
    
    with st.expander("What makes A/B/C different?"):
        st.write("""
        **A - Slightly Flawed:**
        - Mild blur (Gaussian)
        - Slight JPEG compression
        - Minor quality loss
        
        **B - Best Quality:**
        - High-quality rendering
        - Slight enhancement (histogram equalization)
        - Professional appearance
        
        **C - Bad Quality:**
        - Heavy blur
        - Added noise
        - Heavy JPEG compression
        - Color shifts
        - Clearly visible artifacts
        """)
    
    with st.expander("Can I use my own images?"):
        st.write("""
        Currently, the tool generates synthetic backgrounds and text.
        
        To use custom images:
        1. Place images in a folder
        2. Modify the BackgroundLibrary to load them
        3. Rebuild and run
        
        Future versions will support custom image uploads.
        """)
    
    with st.expander("What's the file size?"):
        st.write("""
        Approximate sizes per sample (5 images):
        - 256×256: ~50-100 KB
        - 512×512: ~150-300 KB
        - 800×600: ~200-400 KB
        - 1024×768: ~300-600 KB
        - 2048×1536: ~1-2 MB
        
        100 samples at 800×600 ≈ 20-40 MB
        """)
    
    st.divider()
    
    st.write("## 🔧 Technical Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Text Blocks (100+):**")
        st.write("""
        - Documents (invoices, contracts)
        - Websites (shopping, login)
        - Forms (registration, feedback)
        - Multilingual (multiple languages)
        - Technical (code, logs)
        - Natural (books, signs)
        """)
    
    with col2:
        st.write("**Backgrounds (20+):**")
        st.write("""
        - Paper textures
        - Color gradients
        - Noisy backgrounds
        - Patterns (checks, stripes, dots)
        - Solid colors
        - Synthetic variations
        """)
    
    st.divider()
    
    st.write("## 🚀 Workflow")
    
    st.write("""
    1. **Generate** - Use "Generate Dataset" tab
    2. **Review** - Check "Dataset Info" for samples
    3. **Download** - Get ZIP for your VLM Judge
    4. **Evaluate** - Use VLM Judge to score quality
    5. **Analyze** - Review results and metrics
    """)
