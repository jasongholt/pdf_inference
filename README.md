# 🧬 GWAS Intelligence Pipeline

A complete pipeline for extracting genomic trait data from research papers using **Snowflake Cortex AI** and **multimodal RAG** (Retrieval Augmented Generation).

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project parses PDF research papers containing complex charts, graphs, and scientific terms, extracts GWAS (Genome-Wide Association Studies) trait information, and makes it searchable within Snowflake using vector embeddings and multimodal search.

### What This Pipeline Does

1. **PDF Processing**: Parses PDFs using Snowflake Cortex `AI_PARSE_DOCUMENT`
2. **Image Extraction**: Converts PDF pages to PNG for visual analysis
3. **Embedding Generation**: Creates text and image embeddings using `AI_EMBED`
4. **Multimodal Search**: Combines text and visual information for accurate extraction
5. **Trait Extraction**: Uses LLMs to extract structured GWAS trait data
6. **Analytics**: Provides queryable trait analytics in Snowflake tables

## ✨ Features

- 📄 **Multimodal PDF Processing**: Extracts both text and images
- 🔍 **Hybrid Search**: Combines text and image embeddings
- 🤖 **LLM-Powered Extraction**: Uses Claude/Mistral for trait extraction
- 📊 **Structured Output**: Stores results in queryable Snowflake tables
- 🚀 **Standalone Notebook**: No external Python files required
- ⚡ **Snowflake Native**: Leverages Cortex AI (no external APIs)

## 📦 Prerequisites

### 1. **Snowflake Account**
- Snowflake account with **Cortex AI** enabled
- Role with `CREATE DATABASE` privileges (or `ACCOUNTADMIN`)
- Warehouse for compute (recommend `LARGE` or bigger)

### 2. **Python Environment**
- Python 3.8 or higher
- Jupyter Notebook or JupyterLab

### 3. **Required Python Packages**
See `requirements.txt` for full list:
- `snowflake-snowpark-python` (≥1.11.1)
- `pandas`, `numpy`
- `PyMuPDF` (for PDF processing)
- `python-dotenv` (for credentials)
- `jupyter`, `notebook`

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd gwas_intelligence
```

### Step 2: Create Python Environment

**Option A: Using Conda (Recommended)**
```bash
conda create -n gwas_intelligence python=3.11
conda activate gwas_intelligence
pip install -r requirements.txt
```

**Option B: Using venv**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Install Jupyter Kernel (if using conda)

```bash
conda activate gwas_intelligence
python -m ipykernel install --user --name gwas_intelligence --display-name "Python (gwas_intelligence)"
```

## ⚙️ Configuration

### 1. Create `.env` File

Create a `.env` file in the project root with your Snowflake credentials:

```bash
# Snowflake Connection
SNOWFLAKE_ACCOUNT=your_account.region
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password

# Optional: Override defaults
SNOWFLAKE_WAREHOUSE=your_warehous
SNOWFLAKE_DATABASE=GWAS
```

**⚠️ Security Note**: Never commit the `.env` file! It's already in `.gitignore`.

### 2. Configure Notebook Settings

Open `gwas_extraction_demo.ipynb` and update **Cell 2** if needed:

```python
# Configuration
WAREHOUSE_NAME = "<warehouse>"  # Your warehouse name
DATABASE_NAME = "GWAS"        # Database to create
SCHEMA_RAW = "PDF_RAW"        # Schema for raw PDFs
SCHEMA_PROCESSING = "PDF_PROCESSING"  # Schema for processed data
```

### 3. Required Snowflake Permissions

Your Snowflake user needs:
- `CREATE DATABASE` privilege (or use `ACCOUNTADMIN` role)
- `USAGE` on your warehouse
- Access to **Cortex AI** functions:
  - `AI_PARSE_DOCUMENT`
  - `AI_EMBED`
  - `AI_COMPLETE`
  - `AI_EXTRACT`
  - `CORTEX_SEARCH`

## 🎬 Quick Start

### 1. Start Jupyter

```bash
# Activate your environment first
conda activate gwas_intelligence  # or: source venv/bin/activate

# Launch Jupyter
jupyter notebook
```

### 2. Open the Notebook

Navigate to `gwas_extraction_demo.ipynb` and select the **Python (gwas_intelligence)** kernel.

### 3. Run Setup Cells (1-18)

These cells will:
- ✅ Import dependencies
- ✅ Create database and schemas
- ✅ Create stage for PDFs
- ✅ Create all required tables
- ✅ Connect to Snowflake

**Expected output:**
```
✅ Imports successful!
✅ Configuration set!
✅ Connected to Snowflake!
✅ Database GWAS created
✅ Schema PDF_RAW created
✅ Schema PDF_PROCESSING created
✅ Stage PDF_STAGE created
✅ All tables created
```

### 4. Upload a Test PDF

**Option A: Python Upload (Cell 19)**
```python
# Update the local_pdf_path variable
local_pdf_path = "/path/to/your/paper.pdf"
# Then run the cell
```

**Option B: Snowflake Web UI**
```sql
PUT file:///path/to/paper.pdf @GWAS.PDF_RAW.PDF_STAGE AUTO_COMPRESS=FALSE;
```

**Option C: SnowSQL**
```bash
snowsql -a <account> -u <user> -q "PUT file:///path/to/paper.pdf @GWAS.PDF_RAW.PDF_STAGE AUTO_COMPRESS=FALSE;"
```

### 5. Run the Pipeline

Run cells 20-44 to:
1. Parse the PDF (Cell 20-21)
2. Create PNG images (Cell 22)
3. Generate embeddings (Cell 23-27)
4. Create search service (Cell 28-33)
5. Extract traits (Cell 34-43)
6. View results (Cell 44)

**Total runtime**: 5-15 minutes depending on PDF size

### 6. View Results

```python
# View extracted traits
results_df = session.sql(f"""
    SELECT * 
    FROM {DATABASE_NAME}.{SCHEMA_PROCESSING}.GWAS_TRAIT_ANALYTICS
    ORDER BY CREATED_AT DESC
    LIMIT 10
""").to_pandas()

print(results_df)
```

## 📖 Usage

### Processing Multiple PDFs

To process multiple PDFs, use the provided cells in a loop:

```python
pdf_files = ["paper1.pdf", "paper2.pdf", "paper3.pdf"]

for pdf_file in pdf_files:
    STAGE_FILE_PATH = pdf_file
    DOCUMENT_ID = pdf_file
    
    # Run parsing, embedding, and extraction cells
    # (Copy the logic from cells 20-43)
```

### Querying Extracted Traits

```sql
-- Find all traits for a specific document
SELECT 
    trait,
    chromosome,
    start_position,
    end_position,
    gene_name,
    extraction_confidence
FROM GWAS.PDF_PROCESSING.GWAS_TRAIT_ANALYTICS
WHERE document_id = 'your_paper.pdf'
ORDER BY extraction_confidence DESC;

-- Search across all documents
SELECT 
    document_id,
    trait,
    chromosome,
    gene_name,
    COUNT(*) as trait_count
FROM GWAS.PDF_PROCESSING.GWAS_TRAIT_ANALYTICS
GROUP BY document_id, trait, chromosome, gene_name
ORDER BY trait_count DESC;
```

### Cleaning Up for Re-testing

Use the cleanup cells (near the end of notebook) or run:

```sql
-- Drop all tables
DROP TABLE IF EXISTS GWAS.PDF_PROCESSING.GWAS_TRAIT_ANALYTICS;
DROP TABLE IF EXISTS GWAS.PDF_PROCESSING.MULTIMODAL_PAGES;
DROP TABLE IF EXISTS GWAS.PDF_PROCESSING.IMAGE_PAGES;
DROP TABLE IF EXISTS GWAS.PDF_PROCESSING.TEXT_PAGES;
DROP TABLE IF EXISTS GWAS.PDF_RAW.PARSED_DOCUMENTS;

-- Clear stage
REMOVE @GWAS.PDF_RAW.PDF_STAGE;

-- Drop database (if needed)
DROP DATABASE IF EXISTS GWAS;
```



### Key Files

- **`gwas_extraction_demo.ipynb`**: The main notebook - run this!
- **`requirements.txt`**: Python dependencies
- **`.env`**: Your Snowflake credentials (create this)
- **`docs/`**: Detailed documentation
- **`sql/setup/`**: SQL setup scripts

## 🐛 Troubleshooting

### Common Errors

#### 1. `ModuleNotFoundError: No module named 'snowflake'`
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

#### 2. `Authentication failed` or `Invalid username/password`
**Solution**: Check your `.env` file
- Verify `SNOWFLAKE_ACCOUNT` format: `account.region` (e.g., `abc12345.us-east-1`)
- Verify username and password
- Test with: `python scratch/test_env.py` (if you have it)

#### 3. `Insufficient privileges to create database`
**Solution**: Use a role with CREATE DATABASE privilege
- Option A: Use `ACCOUNTADMIN` role
- Option B: Have your admin grant: `GRANT CREATE DATABASE ON ACCOUNT TO ROLE your_role;`

#### 4. `Cortex function not found` or `AI_PARSE_DOCUMENT` errors
**Solution**: Cortex AI not enabled
- Verify Cortex AI is enabled in your account
- Contact Snowflake support to enable Cortex AI
- Check region availability: [Cortex AI Availability](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions)

#### 5. `Cannot convert a Column object into bool`
**Solution**: Missing `.collect()` call
- This should be fixed in the latest notebook
- If you see this, add `.collect()` after `session.sql()` calls

#### 6. `PDF not found` or stage errors
**Solution**: Verify PDF upload
```python
# List files in stage
session.sql("LIST @GWAS.PDF_RAW.PDF_STAGE").show()
```

#### 7. Cell appears to hang during PDF parsing (Cell 21)
**Solution**: This is normal!
- `AI_PARSE_DOCUMENT` can take 1-5 minutes for large PDFs
- Watch for progress messages
- Check Snowflake query history to verify it's running

### Getting Help

1. **Check the notebook**: Each cell has documentation
2. **Read the error messages**: They usually point to the issue
3. **Snowflake docs**: [Cortex AI Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/overview)
4. **GitHub Issues**: Report bugs or ask questions



## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

See `docs/development/` for developer notes.

## 📄 License

See [LICENSE](LICENSE) file for details.

