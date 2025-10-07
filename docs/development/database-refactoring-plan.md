# Database Refactoring Plan: SYNGENTA → GWAS

**Created:** October 7, 2025  
**Branch:** `gwas-database-refactor`  
**Status:** Planning

## Objective

Refactor the GWAS extraction notebook to:
1. Use a new database named `GWAS` instead of `SYNGENTA`
2. Make the notebook standalone with all SQL setup included
3. Create all database objects (database, schemas, stages, tables) within the notebook
4. Be fully self-contained and runnable from scratch

## Current Database Structure

### Database & Schemas
- **Database:** `SYNGENTA`
- **Schemas:**
  - `PDF_RAW` - Raw PDF data
  - `PDF_PROCESSING` - Processed data and analytics

### Stages
- `@SYNGENTA.PDF_RAW.PDF_STAGE` - File storage for PDFs, images, text

### Tables

#### Schema: PDF_RAW
1. **PARSED_DOCUMENTS**
   - Columns: `document_id`, `file_path`, `file_name`, `parsed_content`, `total_pages`, `created_at`
   - Purpose: Stores raw parsed PDF data from AI_PARSE_DOCUMENT

#### Schema: PDF_PROCESSING
1. **TEXT_PAGES**
   - Columns: `document_id`, `file_name`, `page_number`, `page_text`, `word_count`, `text_embedding`, `embedding_model`, `created_at`
   - Purpose: Stores page text with embeddings

2. **IMAGE_PAGES**
   - Columns: `image_id`, `document_id`, `file_name`, `page_number`, `image_file_path`, `dpi`, `image_format`, `created_at`
   - Purpose: Stores page images metadata

3. **MULTIMODAL_PAGES**
   - Columns: `document_id`, `file_name`, `page_number`, `page_id`, `image_id`, `page_text`, `image_path`, `text_embedding`, `image_embedding`, `embedding_model`, `has_text`, `has_image`, `created_at`
   - Purpose: Combined text + image embeddings for multimodal RAG

4. **GWAS_TRAIT_ANALYTICS** (or **GWAS_TRAIT_ANALYTICS_V2**)
   - Columns: Complex structure with ~20 fields for genomic traits
   - Purpose: Extracted GWAS trait data

5. **GWAS_TIEBREAKER_LOG**
   - Columns: `log_id`, `document_id`, `extraction_version`, `finding_number`, `trait_name`, etc.
   - Purpose: Logs LLM tiebreaker decisions

### Search Services
- `MULTIMODAL_SEARCH_SERVICE` - Cortex Search Service for RAG queries

## Refactoring Steps

### Phase 1: Analysis & Planning ✅
- [x] Identify all database objects
- [x] Document current structure
- [x] Create refactoring plan
- [x] Create git branch

### Phase 2: Create Setup SQL Cells
Will add these SQL cells at the beginning of the notebook:

#### Cell: Database & Schema Setup
```sql
-- Create GWAS database and schemas
CREATE DATABASE IF NOT EXISTS GWAS;

USE DATABASE GWAS;

CREATE SCHEMA IF NOT EXISTS PDF_RAW
  COMMENT = 'Raw PDF data from AI_PARSE_DOCUMENT';

CREATE SCHEMA IF NOT EXISTS PDF_PROCESSING
  COMMENT = 'Processed PDF data, embeddings, and analytics';

USE SCHEMA PDF_RAW;
```

#### Cell: Create Stage
```sql
-- Create stage for PDF files and generated assets
CREATE STAGE IF NOT EXISTS GWAS.PDF_RAW.PDF_STAGE
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
  COMMENT = 'Storage for PDF files, extracted images, and text';

-- Verify stage created
SHOW STAGES LIKE 'PDF_STAGE' IN SCHEMA GWAS.PDF_RAW;
```

#### Cell: Create PDF_RAW Tables
```sql
-- PARSED_DOCUMENTS: Raw parsed PDF data
CREATE TABLE IF NOT EXISTS GWAS.PDF_RAW.PARSED_DOCUMENTS (
    document_id VARCHAR PRIMARY KEY,
    file_path VARCHAR NOT NULL,
    file_name VARCHAR NOT NULL,
    parsed_content VARIANT NOT NULL,
    total_pages INTEGER,
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    COMMENT 'Raw PDF data from Cortex AI_PARSE_DOCUMENT'
);
```

#### Cell: Create PDF_PROCESSING Tables
```sql
-- TEXT_PAGES: Page text with embeddings
CREATE TABLE IF NOT EXISTS GWAS.PDF_PROCESSING.TEXT_PAGES (
    page_id VARCHAR PRIMARY KEY DEFAULT UUID_STRING(),
    document_id VARCHAR NOT NULL,
    file_name VARCHAR NOT NULL,
    page_number INTEGER NOT NULL,
    page_text TEXT,
    word_count INTEGER,
    text_embedding VECTOR(FLOAT, 1024),
    embedding_model VARCHAR(100),
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    UNIQUE (document_id, page_number)
);

-- IMAGE_PAGES: Page images metadata
CREATE TABLE IF NOT EXISTS GWAS.PDF_PROCESSING.IMAGE_PAGES (
    image_id VARCHAR PRIMARY KEY DEFAULT UUID_STRING(),
    document_id VARCHAR NOT NULL,
    file_name VARCHAR NOT NULL,
    page_number INTEGER NOT NULL,
    image_file_path VARCHAR NOT NULL,
    dpi INTEGER DEFAULT 300,
    image_format VARCHAR(10) DEFAULT 'PNG',
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    UNIQUE (document_id, page_number)
);

-- MULTIMODAL_PAGES: Combined text + image embeddings
CREATE TABLE IF NOT EXISTS GWAS.PDF_PROCESSING.MULTIMODAL_PAGES (
    page_id VARCHAR PRIMARY KEY DEFAULT UUID_STRING(),
    document_id VARCHAR NOT NULL,
    file_name VARCHAR NOT NULL,
    page_number INTEGER NOT NULL,
    image_id VARCHAR,
    page_text TEXT,
    image_path VARCHAR,
    text_embedding VECTOR(FLOAT, 1024),
    image_embedding VECTOR(FLOAT, 1024),
    embedding_model VARCHAR(100),
    has_text BOOLEAN DEFAULT FALSE,
    has_image BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    UNIQUE (document_id, page_number)
);

-- GWAS_TRAIT_ANALYTICS: Extracted genomic trait data
CREATE TABLE IF NOT EXISTS GWAS.PDF_PROCESSING.GWAS_TRAIT_ANALYTICS (
    analytics_id VARCHAR PRIMARY KEY DEFAULT UUID_STRING(),
    document_id VARCHAR NOT NULL,
    file_name VARCHAR NOT NULL,
    extraction_version VARCHAR(50),
    finding_number INTEGER DEFAULT 1,
    
    -- Genomic traits
    trait VARCHAR(500),
    germplasm_name VARCHAR(500),
    genome_version VARCHAR(100),
    chromosome VARCHAR(50),
    physical_position VARCHAR(200),
    gene VARCHAR(500),
    snp_name VARCHAR(200),
    variant_id VARCHAR(200),
    variant_type VARCHAR(100),
    effect_size VARCHAR(200),
    gwas_model VARCHAR(200),
    evidence_type VARCHAR(100),
    allele VARCHAR(100),
    annotation TEXT,
    candidate_region VARCHAR(500),
    
    -- Metadata
    extraction_source VARCHAR(50),
    field_citations VARIANT,
    field_confidence VARIANT,
    field_raw_values VARIANT,
    traits_extracted INTEGER,
    traits_not_reported INTEGER,
    extraction_accuracy_pct FLOAT,
    
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    UNIQUE (document_id, extraction_version, finding_number)
);

-- GWAS_TIEBREAKER_LOG: LLM tiebreaker decisions
CREATE TABLE IF NOT EXISTS GWAS.PDF_PROCESSING.GWAS_TIEBREAKER_LOG (
    log_id VARCHAR PRIMARY KEY DEFAULT UUID_STRING(),
    document_id VARCHAR NOT NULL,
    extraction_version VARCHAR(50),
    finding_number INTEGER,
    trait_name VARCHAR(200),
    method_a_value VARCHAR(1000),
    method_b_value VARCHAR(1000),
    method_c_value VARCHAR(1000),
    final_decision VARCHAR(1000),
    reasoning TEXT,
    confidence_score FLOAT,
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP()
);
```

#### Cell: Create Search Service (Optional - Later)
```sql
-- Create Cortex Search Service for multimodal RAG
-- Note: Run this after loading data into MULTIMODAL_PAGES

CREATE OR REPLACE CORTEX SEARCH SERVICE GWAS.PDF_PROCESSING.MULTIMODAL_SEARCH_SERVICE
ON page_text
ATTRIBUTES page_number
WAREHOUSE = YOUR_WAREHOUSE_NAME
TARGET_LAG = '1 minute'
AS (
    SELECT
        document_id,
        page_number,
        page_text,
        text_embedding,
        image_embedding
    FROM GWAS.PDF_PROCESSING.MULTIMODAL_PAGES
);
```

### Phase 3: Find & Replace
Replace all references:
- `SYNGENTA.PDF_RAW` → `GWAS.PDF_RAW`
- `SYNGENTA.PDF_PROCESSING` → `GWAS.PDF_PROCESSING`
- `@SYNGENTA.PDF_RAW.PDF_STAGE` → `@GWAS.PDF_RAW.PDF_STAGE`

### Phase 4: Update Configuration
- Update `.env` database name
- Update `.env.example`
- Update connection code if needed

### Phase 5: Testing
1. Clear all notebook outputs
2. Run notebook from scratch
3. Verify all database objects created
4. Verify PDF processing works
5. Verify embeddings generation works
6. Verify trait extraction works

### Phase 6: Documentation
- Update README with new database name
- Update deployment docs
- Document database setup requirements

## Implementation Order

1. **Step 1:** Create new SQL cells for database/schema setup
2. **Step 2:** Create SQL cells for stage creation
3. **Step 3:** Create SQL cells for table creation
4. **Step 4:** Replace SYNGENTA with GWAS in all queries
5. **Step 5:** Test incrementally after each change
6. **Step 6:** Update environment files and documentation

## Rollback Plan

If issues occur:
```bash
git checkout main
# or
git reset --hard HEAD~1
```

Keep `main` branch untouched until testing is complete.

## Benefits of This Approach

1. **Standalone Notebook** - Everything needed to run is in the notebook
2. **Reproducible** - Anyone can run from scratch
3. **Clear Database** - Dedicated GWAS database, not mixed with other data
4. **Self-Documenting** - SQL cells show exactly what's created
5. **Idempotent** - Uses IF NOT EXISTS, safe to rerun

## Questions to Resolve

1. **Warehouse Name**: Which warehouse should be used? (Update in connection)
2. **Permissions**: Does the user have CREATE DATABASE privileges?
3. **Search Service**: Create immediately or defer until after data load?
4. **Cleanup**: Should we add cells to DROP/RECREATE for clean testing?

## Next Steps

- [ ] Review plan with user
- [ ] Proceed step-by-step with implementation
- [ ] Test each step before moving to next
- [ ] Commit changes incrementally to branch

