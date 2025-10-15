"""
🧬 GWAS Trait Extraction Viewer
A beautiful Streamlit app for exploring genomic data extracted from research papers
using Snowflake Cortex AI and multimodal RAG.

Now with page-based navigation to prevent unwanted navigation during chat!
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
from snowflake.snowpark.context import get_active_session

# =============================
# 🎨 PAGE CONFIG & STYLING
# =============================
st.set_page_config(
    page_title="GWAS Trait Extraction Viewer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #2ca02c;
        --accent-color: #ff7f0e;
        --background-color: #f8f9fa;
        --success-color: #28a745;
        --warning-color: #ffc107;
        --danger-color: #dc3545;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid var(--primary-color);
        margin-bottom: 1rem;
    }
    
    .metric-card h3 {
        margin: 0 0 0.5rem 0;
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-card p {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
        color: #333;
    }
    
    /* Beautiful trait cards */
    .trait-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .trait-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .trait-card.found {
        border-left: 4px solid var(--success-color);
    }
    
    .trait-card.not-found {
        border-left: 4px solid #dee2e6;
        opacity: 0.85;
    }
    
    .trait-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
    }
    
    .trait-icon {
        font-size: 1.5rem;
        opacity: 0.8;
    }
    
    .trait-name {
        font-size: 0.9rem;
        font-weight: 600;
        color: #495057;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0;
    }
    
    .trait-value {
        font-size: 1.1rem;
        font-weight: 600;
        color: #212529;
        margin: 0;
        line-height: 1.4;
        word-break: break-word;
    }
    
    .trait-not-found {
        font-size: 0.95rem;
        color: #6c757d;
        font-style: italic;
        margin: 0;
    }
    
    .trait-status {
        position: absolute;
        top: 0.75rem;
        right: 0.75rem;
        font-size: 0.75rem;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .trait-status.found {
        background-color: #d4edda;
        color: #155724;
    }
    
    .trait-status.not-found {
        background-color: #f8f9fa;
        color: #6c757d;
    }
    
    /* Stats section */
    .stats-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
    }
    
    .stat-item {
        text-align: center;
        padding: 1rem;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #5a6c7d;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .section-header::after {
        content: '';
        flex: 1;
        height: 2px;
        background: linear-gradient(to right, #e9ecef, transparent);
        margin-left: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================
# 🔌 SNOWFLAKE CONNECTION
# =============================
@st.cache_resource
def get_snowflake_connection():
    """Initialize Snowflake connection"""
    return st.connection("snowflake")

conn = get_snowflake_connection()

# =============================
# 📊 DATA LOADING FUNCTIONS
# =============================
@st.cache_data(ttl=600)
def load_documents():
    """Load all available documents"""
    query = """
    SELECT 
        DOCUMENT_ID as document_id,
        FILE_NAME as pdf_filename,
        TOTAL_PAGES as page_count,
        CREATED_AT as extraction_timestamp,
        FILE_PATH as file_url
    FROM GWAS.PDF_RAW.PARSED_DOCUMENTS
    ORDER BY CREATED_AT DESC
    """
    return conn.query(query)

@st.cache_data(ttl=600)
def load_gwas_traits(document_id):
    """Load GWAS traits for a specific document"""
    query = f"""
    SELECT 
        trait,
        germplasm_name,
        genome_version,
        chromosome,
        physical_position,
        gene,
        snp_name,
        variant_id,
        variant_type,
        effect_size,
        gwas_model,
        evidence_type,
        allele,
        annotation,
        candidate_region,
        extraction_source,
        field_citations,
        traits_extracted,
        traits_not_reported,
        extraction_accuracy_pct
    FROM GWAS.PDF_PROCESSING.GWAS_TRAIT_ANALYTICS
    WHERE document_id = '{document_id}'
    """
    return conn.query(query)

@st.cache_data(ttl=600)
def load_document_pages(document_id):
    """Load multimodal pages for a document"""
    query = f"""
    SELECT 
        page_number,
        page_text,
        image_path,
        has_text,
        has_image
    FROM GWAS.PDF_PROCESSING.MULTIMODAL_PAGES
    WHERE document_id = '{document_id}'
    ORDER BY page_number
    """
    return conn.query(query)

@st.cache_data(ttl=600)
def load_text_pages(document_id):
    """Load text pages for analytics"""
    query = f"""
    SELECT 
        page_number,
        LENGTH(page_text) as text_length
    FROM GWAS.PDF_PROCESSING.TEXT_PAGES
    WHERE document_id = '{document_id}'
    ORDER BY page_number
    """
    return conn.query(query)

@st.cache_data(ttl=600)
def load_image_pages(document_id):
    """Load image pages for analytics"""
    query = f"""
    SELECT 
        page_number,
        image_file_path as image_path
    FROM GWAS.PDF_PROCESSING.IMAGE_PAGES
    WHERE document_id = '{document_id}'
    ORDER BY page_number
    """
    return conn.query(query)

# =============================
# 🗂️ DOCUMENT SELECTOR (SHARED)
# =============================
def render_document_selector():
    """Render document selector in sidebar - shared across all pages"""
    with st.sidebar:
        st.markdown("### 📁 Document Selection")
        
        # Load documents
        documents = load_documents()
        
        if documents.empty:
            st.warning("⚠️ No documents found in the database.")
            st.info("💡 Please run the GWAS extraction pipeline first.")
            st.stop()
        
        # Initialize session state for selected document
        if "selected_doc_id" not in st.session_state:
            st.session_state.selected_doc_id = documents.iloc[0]['DOCUMENT_ID']
        
        # Document selector
        doc_options = {
            f"{row['PDF_FILENAME']} ({row['DOCUMENT_ID'][:8]}...)": row['DOCUMENT_ID'] 
            for _, row in documents.iterrows()
        }
        
        # Find current selection index
        current_doc_labels = [label for label, doc_id in doc_options.items() 
                             if doc_id == st.session_state.selected_doc_id]
        current_index = list(doc_options.keys()).index(current_doc_labels[0]) if current_doc_labels else 0
        
        selected_doc_label = st.selectbox(
            "Choose a document:",
            options=list(doc_options.keys()),
            index=current_index,
            key="doc_selector"
        )
        
        # Update session state when selection changes
        st.session_state.selected_doc_id = doc_options[selected_doc_label]
        
        # Document info card
        doc_info = documents[documents['DOCUMENT_ID'] == st.session_state.selected_doc_id].iloc[0]
        
        st.markdown("---")
        st.markdown("### 📄 Document Info")
        st.markdown(f"""
        <div class="metric-card">
            <h3>Filename</h3>
            <p style="font-size: 1rem;">{doc_info['PDF_FILENAME']}</p>
        </div>
        <div class="metric-card">
            <h3>Pages</h3>
            <p>{doc_info['PAGE_COUNT']}</p>
        </div>
        <div class="metric-card">
            <h3>Extracted</h3>
            <p style="font-size: 1rem;">{doc_info['EXTRACTION_TIMESTAMP'].strftime('%Y-%m-%d')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🔍 Quick Stats")
        
        # Load stats
        traits_df = load_gwas_traits(st.session_state.selected_doc_id)
        
        if not traits_df.empty:
            traits_row = traits_df.iloc[0]
            
            # Recalculate accurate count (excluding NOT_FOUND)
            trait_field_names = [
                'TRAIT', 'GERMPLASM_NAME', 'GENOME_VERSION', 'CHROMOSOME', 'PHYSICAL_POSITION',
                'GENE', 'SNP_NAME', 'VARIANT_ID', 'VARIANT_TYPE', 'EFFECT_SIZE',
                'GWAS_MODEL', 'EVIDENCE_TYPE', 'ALLELE', 'ANNOTATION', 'CANDIDATE_REGION'
            ]
            
            actual_found = 0
            for field in trait_field_names:
                value = traits_row.get(field)
                if value:
                    value_str = str(value).strip('"').strip("'")
                    if value_str and "NOT_FOUND" not in value_str.upper():
                        actual_found += 1
            
            total_traits = len(trait_field_names)
            actual_accuracy = (actual_found / total_traits) * 100
            
            st.metric("Traits Extracted", f"{actual_found}/{total_traits}")
            st.metric("Accuracy", f"{actual_accuracy:.1f}%")
            st.metric("Source", traits_row['EXTRACTION_SOURCE'].replace('_', ' ').title())
        
        # Download PDF button
        st.markdown("---")
        st.markdown("### 📥 Download")
        
        if st.button("📄 Download PDF", use_container_width=True):
            pdf_url = doc_info['FILE_URL']
            st.info(f"📁 PDF Location:\n`{pdf_url}`")
            st.caption("To download: Use GET command in Snowsight or download from stage")
            st.code(f"GET {pdf_url} file:///local/path/", language="sql")
    
    return doc_info

# =============================
# 📄 PAGE FUNCTIONS
# =============================

def page_extracted_traits():
    """Page 1: Extracted Traits"""
    traits_df = load_gwas_traits(st.session_state.selected_doc_id)
    
    if traits_df.empty:
        st.warning("⚠️ No trait data found for this document.")
        return
    
    traits_row = traits_df.iloc[0]
    
    # Recalculate actual traits found (excluding NOT_FOUND values)
    trait_field_names = [
        'TRAIT', 'GERMPLASM_NAME', 'GENOME_VERSION', 'CHROMOSOME', 'PHYSICAL_POSITION',
        'GENE', 'SNP_NAME', 'VARIANT_ID', 'VARIANT_TYPE', 'EFFECT_SIZE',
        'GWAS_MODEL', 'EVIDENCE_TYPE', 'ALLELE', 'ANNOTATION', 'CANDIDATE_REGION'
    ]
    
    actual_found = 0
    for field in trait_field_names:
        value = traits_row.get(field)
        if value:
            value_str = str(value).strip('"').strip("'")
            is_valid = value_str and "NOT_FOUND" not in value_str.upper() and "NOT FOUND" not in value_str.upper()
            if is_valid:
                actual_found += 1
    
    total_traits = len(trait_field_names)
    actual_accuracy = (actual_found / total_traits) * 100 if total_traits > 0 else 0
    
    # Beautiful stats section
    st.markdown("""
    <div class="stats-container">
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
            <div class="stat-item">
                <p class="stat-value">{}/{}</p>
                <p class="stat-label">Traits Found</p>
            </div>
            <div class="stat-item">
                <p class="stat-value">{:.1f}%</p>
                <p class="stat-label">Accuracy</p>
            </div>
            <div class="stat-item">
                <p class="stat-value">{}</p>
                <p class="stat-label">Not Reported</p>
            </div>
            <div class="stat-item">
                <p class="stat-value">{}</p>
                <p class="stat-label">Evidence Type</p>
            </div>
        </div>
    </div>
    """.format(
        actual_found, total_traits,
        actual_accuracy,
        total_traits - actual_found,
        traits_row['EVIDENCE_TYPE'] or "GWAS"
    ), unsafe_allow_html=True)
    
    # Section header
    st.markdown('<h3 class="section-header">🧬 Extracted Genomic Data</h3>', unsafe_allow_html=True)
    
    # Define trait display order and labels
    trait_fields = [
        ("Trait", "trait", "🎯"),
        ("Germplasm Name", "germplasm_name", "🌱"),
        ("Genome Version", "genome_version", "🧬"),
        ("Chromosome", "chromosome", "📍"),
        ("Physical Position", "physical_position", "📏"),
        ("Gene", "gene", "🧪"),
        ("SNP Name", "snp_name", "🔬"),
        ("Variant ID", "variant_id", "🆔"),
        ("Variant Type", "variant_type", "🔀"),
        ("Effect Size", "effect_size", "📈"),
        ("GWAS Model", "gwas_model", "🧮"),
        ("Allele", "allele", "🔤"),
        ("Annotation", "annotation", "📝"),
        ("Candidate Region", "candidate_region", "🗺️")
    ]
    
    # Parse citations
    try:
        citations = json.loads(traits_row['FIELD_CITATIONS']) if traits_row['FIELD_CITATIONS'] else {}
    except:
        citations = {}
    
    # Display traits in a beautiful 2-column grid with HTML
    col1, col2 = st.columns(2)
    
    for idx, (label, field, icon) in enumerate(trait_fields):
        col = col1 if idx % 2 == 0 else col2
        
        value = traits_row[field.upper()]
        
        # Clean up value - strip quotes and check for NOT_FOUND
        if value:
            value = str(value).strip('"').strip("'")
        
        # Check if value is actually missing
        is_missing = (
            not value or 
            value == "Not in paper" or
            "NOT_FOUND" in value.upper() or
            "NOT FOUND" in value.upper() or
            value == "None" or
            value == "NULL"
        )
        
        # Create beautiful trait card
        with col:
            if is_missing:
                st.markdown(f"""
                <div class="trait-card not-found">
                    <div class="trait-status not-found">Not Found</div>
                    <div class="trait-header">
                        <span class="trait-icon">{icon}</span>
                        <h4 class="trait-name">{label}</h4>
                    </div>
                    <p class="trait-not-found">Not reported in paper</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="trait-card found">
                    <div class="trait-status found">Found</div>
                    <div class="trait-header">
                        <span class="trait-icon">{icon}</span>
                        <h4 class="trait-name">{label}</h4>
                    </div>
                    <p class="trait-value">{value}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Additional info section
    st.markdown('<h3 class="section-header">📊 Extraction Metadata</h3>', unsafe_allow_html=True)
    
    metadata_cols = st.columns(3)
    
    with metadata_cols[0]:
        source = "Multimodal Pipeline" if traits_row['EXTRACTION_SOURCE'] == 'multimodal_pipeline' else "Text-Only Pipeline"
        st.markdown(f"""
        <div class="metric-card">
            <h3>Extraction Source</h3>
            <p style="font-size: 1.1rem;">{source}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metadata_cols[1]:
        confidence_text = traits_row.get('FIELD_CITATIONS', 'N/A')
        if confidence_text and confidence_text != 'N/A':
            # Try to extract confidence summary
            if 'HIGH' in confidence_text:
                conf_parts = confidence_text.split()
                conf_summary = ' '.join(conf_parts[:3]) if len(conf_parts) > 3 else confidence_text[:20]
            else:
                conf_summary = confidence_text[:30]
        else:
            conf_summary = 'Not available'
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>Confidence Summary</h3>
            <p style="font-size: 1.1rem;">{conf_summary}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metadata_cols[2]:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Traits Extracted</h3>
            <p style="font-size: 1.1rem;">{traits_row['TRAITS_EXTRACTED']}/{total_traits}</p>
        </div>
        """, unsafe_allow_html=True)


def page_browser():
    """Page 2: Page Browser"""
    st.markdown("## 📄 Page Browser")
    st.markdown("*Explore individual pages with text and images*")
    
    pages_df = load_document_pages(st.session_state.selected_doc_id)
    
    if pages_df.empty:
        st.warning("⚠️ No page data found for this document.")
        return
    
    # Page selector
    page_numbers = sorted(pages_df['PAGE_NUMBER'].unique())
    selected_page = st.selectbox(
        "Select page:",
        options=page_numbers,
        format_func=lambda x: f"Page {x}",
        key="page_selector"
    )
    
    page_data = pages_df[pages_df['PAGE_NUMBER'] == selected_page].iloc[0]
    
    # Display page content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Page Text")
        if page_data['HAS_TEXT'] and page_data['PAGE_TEXT']:
            with st.expander("View full text", expanded=True):
                st.text_area(
                    "Text content:",
                    value=page_data['PAGE_TEXT'][:2000] + "..." if len(page_data['PAGE_TEXT']) > 2000 else page_data['PAGE_TEXT'],
                    height=400,
                    key=f"text_{selected_page}",
                    label_visibility="collapsed"
                )
        else:
            st.info("No text content for this page")
    
    with col2:
        st.markdown("### 🖼️ Page Image")
        if page_data['HAS_IMAGE'] and page_data['IMAGE_PATH']:
            try:
                from snowflake.snowpark.files import SnowflakeFile
                import io
                
                # Get Snowpark session
                session = get_active_session()
                
                # Clean up image path (remove any @ prefix if present)
                image_path = page_data['IMAGE_PATH'].lstrip('@')
                
                # Build scoped file URL for SnowflakeFile
                scoped_url_query = f"""
                SELECT BUILD_SCOPED_FILE_URL(@GWAS.PDF_RAW.PDF_STAGE, '{image_path}') as scoped_url
                """
                
                result = session.sql(scoped_url_query).collect()
                
                if result and result[0]['SCOPED_URL']:
                    scoped_url = result[0]['SCOPED_URL']
                    
                    # Read image file as bytes using SnowflakeFile
                    with SnowflakeFile.open(scoped_url, 'rb') as f:
                        image_bytes = f.read()
                    
                    # Display the image using bytes
                    st.image(image_bytes, use_container_width=True, caption=f"Page {selected_page}")
                    
                    with st.expander("📁 Image Details"):
                        st.caption(f"**Stage Path:** `{page_data['IMAGE_PATH']}`")
                        st.caption(f"**Full Path:** `@GWAS.PDF_RAW.PDF_STAGE/{image_path}`")
                        st.caption(f"**File Size:** {len(image_bytes):,} bytes")
                else:
                    st.warning("Could not generate scoped URL")
                    st.caption(f"📁 Path: {page_data['IMAGE_PATH']}")
                    
            except Exception as e:
                st.error(f"Error loading image: {str(e)}")
                st.caption(f"📁 Path: {page_data['IMAGE_PATH']}")
                st.info("💡 Tip: Try regenerating images or check stage permissions")
        else:
            st.warning("No image available for this page")
    
    # Page statistics
    st.markdown("---")
    st.markdown("### 📊 Page Statistics")
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.metric("Page Number", selected_page)
    
    with stat_col2:
        text_len = len(page_data['PAGE_TEXT']) if page_data['PAGE_TEXT'] else 0
        st.metric("Text Length", f"{text_len:,} chars")
    
    with stat_col3:
        status = "✓ Complete" if page_data['HAS_TEXT'] and page_data['HAS_IMAGE'] else "⚠ Partial"
        st.metric("Status", status)


def page_analytics():
    """Page 3: Analytics Dashboard"""
    st.markdown("## 📊 Analytics Dashboard")
    
    traits_df = load_gwas_traits(st.session_state.selected_doc_id)
    
    if traits_df.empty:
        st.warning("⚠️ No analytics data available.")
        return
    
    traits_row = traits_df.iloc[0]
    documents = load_documents()
    doc_info = documents[documents['DOCUMENT_ID'] == st.session_state.selected_doc_id].iloc[0]
    
    # Extraction summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Extraction Summary")
        
        # Recalculate accurate counts (excluding NOT_FOUND)
        trait_field_names = [
            'TRAIT', 'GERMPLASM_NAME', 'GENOME_VERSION', 'CHROMOSOME', 'PHYSICAL_POSITION',
            'GENE', 'SNP_NAME', 'VARIANT_ID', 'VARIANT_TYPE', 'EFFECT_SIZE',
            'GWAS_MODEL', 'EVIDENCE_TYPE', 'ALLELE', 'ANNOTATION', 'CANDIDATE_REGION'
        ]
        
        extracted = 0
        for field in trait_field_names:
            value = traits_row.get(field)
            if value:
                value_str = str(value).strip('"').strip("'")
                if value_str and "NOT_FOUND" not in value_str.upper():
                    extracted += 1
        
        not_reported = len(trait_field_names) - extracted
        
        summary_df = pd.DataFrame({
            'Status': ['Extracted', 'Not Reported'],
            'Count': [extracted, not_reported]
        })
        
        st.bar_chart(summary_df.set_index('Status'))
        st.metric("Extraction Accuracy", f"{traits_row['EXTRACTION_ACCURACY_PCT']:.1f}%")
    
    with col2:
        st.markdown("### 📈 Extraction Sources")
        
        # Parse citations to count sources
        try:
            citations = json.loads(traits_row['FIELD_CITATIONS']) if traits_row['FIELD_CITATIONS'] else {}
            
            phase1_count = sum(1 for v in citations.values() if 'Phase1' in str(v))
            phase2_count = sum(1 for v in citations.values() if 'Phase2' in str(v))
            llm_count = sum(1 for v in citations.values() if 'LLM' in str(v))
            
            sources_df = pd.DataFrame({
                'Source': ['Phase 1 (Text)', 'Phase 2 (Multimodal)', 'LLM Tie-Breaker'],
                'Count': [phase1_count, phase2_count, llm_count]
            })
            
            st.bar_chart(sources_df.set_index('Source'))
            
        except Exception as e:
            st.warning("Could not parse citation data")
    
    # Page statistics
    st.markdown("---")
    st.markdown("### 📄 Document Processing Stats")
    
    text_pages_df = load_text_pages(st.session_state.selected_doc_id)
    image_pages_df = load_image_pages(st.session_state.selected_doc_id)
    pages_df = load_document_pages(st.session_state.selected_doc_id)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pages", doc_info['PAGE_COUNT'])
    
    with col2:
        st.metric("Text Pages", len(text_pages_df))
    
    with col3:
        st.metric("Image Pages", len(image_pages_df))
    
    with col4:
        st.metric("Multimodal Pages", len(pages_df))
    
    # Text length distribution
    if not text_pages_df.empty:
        st.markdown("### 📏 Text Length Distribution by Page")
        st.line_chart(text_pages_df.set_index('PAGE_NUMBER')['TEXT_LENGTH'])


def page_raw_data():
    """Page 4: Raw Data Explorer"""
    st.markdown("## 🔍 Raw Data Explorer")
    st.markdown("*View raw data from database tables*")
    
    traits_df = load_gwas_traits(st.session_state.selected_doc_id)
    pages_df = load_document_pages(st.session_state.selected_doc_id)
    documents = load_documents()
    doc_info = documents[documents['DOCUMENT_ID'] == st.session_state.selected_doc_id].iloc[0]
    
    # GWAS Traits Table
    with st.expander("🧬 GWAS Traits Analytics", expanded=True):
        if not traits_df.empty:
            st.dataframe(traits_df, use_container_width=True)
            
            # Download button
            csv = traits_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Traits CSV",
                data=csv,
                file_name=f"gwas_traits_{st.session_state.selected_doc_id[:8]}.csv",
                mime="text/csv"
            )
        else:
            st.info("No trait data available")
    
    # Multimodal Pages Table
    with st.expander("📄 Multimodal Pages"):
        if not pages_df.empty:
            st.dataframe(pages_df, use_container_width=True)
            
            # Download button
            csv = pages_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Pages CSV",
                data=csv,
                file_name=f"pages_{st.session_state.selected_doc_id[:8]}.csv",
                mime="text/csv"
            )
        else:
            st.info("No page data available")
    
    # Document Metadata
    with st.expander("📋 Document Metadata"):
        st.json({
            "document_id": doc_info['DOCUMENT_ID'],
            "pdf_filename": doc_info['PDF_FILENAME'],
            "page_count": int(doc_info['PAGE_COUNT']),
            "file_url": doc_info['FILE_URL'],
            "extraction_timestamp": doc_info['EXTRACTION_TIMESTAMP'].isoformat()
        })


def page_chatbot():
    """Page 5: Ask Questions (Chatbot)"""
    st.markdown("## 🤖 Ask Questions About This Document")
    st.markdown("*Use AI to ask questions about the research paper and get answers with source citations*")
    
    # Initialize session state for chat
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    if "chat_model" not in st.session_state:
        st.session_state.chat_model = "mistral-large2"
    
    # Chat configuration
    with st.expander("⚙️ Chat Settings", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            model = st.selectbox(
                "Select AI Model",
                ["mistral-large2", "llama3.1-70b", "llama3.1-8b"],
                key="chat_model_select"
            )
            st.session_state.chat_model = model
        
        with col2:
            num_chunks = st.slider(
                "Context Pages",
                min_value=1,
                max_value=10,
                value=5,
                key="num_chunks"
            )
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_messages = []
            st.rerun()
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
            st.markdown(message["content"])
    
    # Chat input
    if question := st.chat_input("Ask a question about this GWAS paper...", key="chat_input"):
        # Add user message to chat history
        st.session_state.chat_messages.append({"role": "user", "content": question})
        
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(question)
        
        # Display assistant response
        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            
            with st.spinner("Searching document and generating answer..."):
                try:
                    # Get Snowpark session
                    session = get_active_session()
                    
                    # Step 1: Generate embeddings for the question using AI_EMBED
                    question_clean = question.replace("'", "''")  # Escape for SQL
                    
                    embed_query = f"""
                    SELECT 
                        AI_EMBED('voyage-multimodal-3', '{question_clean}') as text_vector,
                        AI_EMBED('voyage-multimodal-3', '{question_clean}') as image_vector
                    """
                    
                    embedding_results = session.sql(embed_query).collect()
                    
                    # Convert embeddings to lists
                    text_vector = embedding_results[0]['TEXT_VECTOR']
                    image_vector = embedding_results[0]['IMAGE_VECTOR']
                    
                    # Convert to Python lists if needed
                    if hasattr(text_vector, 'tolist'):
                        text_vector = text_vector.tolist()
                    elif not isinstance(text_vector, list):
                        text_vector = list(text_vector)
                    
                    if hasattr(image_vector, 'tolist'):
                        image_vector = image_vector.tolist()
                    elif not isinstance(image_vector, list):
                        image_vector = list(image_vector)
                    
                    # Step 2: Build multi_index_query (escape question for JSON)
                    question_json = question.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
                    
                    # Convert vectors to JSON string
                    text_vector_str = str(text_vector).replace("'", '"')
                    image_vector_str = str(image_vector).replace("'", '"')
                    
                    # Build the search query with multi_index_query
                    search_query = f"""
                    SELECT 
                        result.value:page_text::STRING AS page_text,
                        result.value:page_number::INT AS page_number
                    FROM TABLE(
                        FLATTEN(
                            PARSE_JSON(
                                SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                                    'GWAS.PDF_PROCESSING.MULTIMODAL_SEARCH_SERVICE',
                                    '{{
                                        "multi_index_query": {{
                                            "page_text": {{"text": "{question_json}"}},
                                            "text_embedding": {{"vector": {text_vector_str}}},
                                            "image_embedding": {{"vector": {image_vector_str}}}
                                        }},
                                        "columns": ["page_text", "page_number"],
                                        "limit": {num_chunks},
                                        "filter": {{"@eq": {{"document_id": "{st.session_state.selected_doc_id}"}}}}
                                    }}'
                                )
                            )['results']
                        )
                    ) AS result
                    """
                    
                    search_results = session.sql(search_query).collect()
                    
                    # Build context from search results
                    context_str = ""
                    page_refs = []
                    for result in search_results:
                        page_num = result['PAGE_NUMBER'] if result['PAGE_NUMBER'] else 'Unknown'
                        page_text = result['PAGE_TEXT'] if result['PAGE_TEXT'] else ''
                        context_str += f"[Page {page_num}]: {page_text}\n\n"
                        if page_num not in page_refs and page_num != 'Unknown':
                            page_refs.append(page_num)
                    
                    # Create prompt for LLM
                    prompt = f"""[INST]
You are a helpful AI assistant specialized in genomic research and GWAS studies. A user is asking about a research paper.

Use the context provided from the research paper to answer the user's question accurately and concisely.

Context from the paper (with page numbers):
{context_str}

User Question: {question}

Instructions:
- Answer based on the provided context
- Be specific and cite page numbers when relevant
- If the context doesn't contain enough information to answer, say so
- Focus on GWAS-related insights, genomic findings, and research methodology
- Be concise but thorough

[/INST]
Answer:"""
                    
                    # Generate response using Cortex LLM via SQL
                    prompt_escaped = prompt.replace("'", "''")
                    llm_query = f"""
                    SELECT SNOWFLAKE.CORTEX.COMPLETE(
                        '{st.session_state.chat_model}',
                        '{prompt_escaped}'
                    ) as response
                    """
                    llm_result = session.sql(llm_query).collect()
                    response = llm_result[0]['RESPONSE'] if llm_result else "Sorry, I couldn't generate a response."
                    
                    # Format response with citations
                    if page_refs:
                        page_refs_str = ", ".join([f"Page {p}" for p in sorted(page_refs)])
                        response_with_refs = f"{response}\n\n**📄 Sources:** {page_refs_str}"
                    else:
                        response_with_refs = response
                    
                    message_placeholder.markdown(response_with_refs)
                    
                    # Add to chat history
                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": response_with_refs
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    message_placeholder.error(error_msg)
                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
    
    # Help section
    if not st.session_state.chat_messages:
        st.info("💡 **Tip**: Ask questions like:")
        st.markdown("""
        - What is the main finding of this study?
        - Which genes were identified as significant?
        - What germplasm was used in this research?
        - Explain the GWAS methodology used
        - What are the key SNPs mentioned?
        - How many traits were analyzed?
        """)


# =============================
# 🗺️ NAVIGATION & MAIN
# =============================

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧬 GWAS Trait Extraction Viewer</h1>
        <p>Explore genomic data extracted from research papers using Snowflake Cortex AI & Multimodal RAG</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Define pages
    pages = {
        "📋 Extracted Traits": page_extracted_traits,
        "📄 Page Browser": page_browser,
        "📊 Analytics Dashboard": page_analytics,
        "🔍 Raw Data": page_raw_data,
        "🤖 Ask Questions": page_chatbot,
    }
    
    # Create page navigation AT THE TOP
    st.sidebar.markdown("### 🗂️ Navigate")
    
    # Initialize current page in session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "📋 Extracted Traits"
    
    # Page selection
    selected_page = st.sidebar.radio(
        "Go to:",
        options=list(pages.keys()),
        index=list(pages.keys()).index(st.session_state.current_page),
        key="page_navigation"
    )
    
    # Update current page
    st.session_state.current_page = selected_page
    
    # Add separator before document selector
    st.sidebar.markdown("---")
    
    # Render shared document selector (now below navigation)
    doc_info = render_document_selector()
    
    # Render selected page
    pages[selected_page]()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🧬 <strong>GWAS Trait Extraction Viewer</strong></p>
        <p>Powered by Snowflake Cortex AI, Multimodal RAG & Streamlit</p>
        <p style="font-size: 0.9rem;">Built with ❤️ using snowflake-arctic-embed-l-v2.0-8k & voyage-multimodal-3</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
