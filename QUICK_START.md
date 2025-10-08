# 🚀 Quick Start Guide

Get up and running with the GWAS Intelligence Pipeline in **5 minutes**.

## Prerequisites Checklist

Before you start, make sure you have:
- [ ] Snowflake account with Cortex AI enabled
- [ ] Python 3.8+ installed
- [ ] Jupyter Notebook installed
- [ ] A GWAS research paper PDF to test

## Step-by-Step Setup

### 1. Install Python Dependencies (2 minutes)

```bash
# Clone the repo (if not done already)
cd gwas_intelligence

# Create conda environment (recommended)
conda create -n gwas_intelligence python=3.11
conda activate gwas_intelligence

# Install dependencies
pip install -r requirements.txt

# Register Jupyter kernel
python -m ipykernel install --user --name gwas_intelligence
```

**Alternative with venv**:
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Snowflake Credentials (1 minute)

Create a `.env` file in the project root:

```bash
# Copy the template
cat > .env << 'EOF'
SNOWFLAKE_ACCOUNT=your_account.region
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=DEMO_JGH
EOF
```

Replace:
- `your_account.region` with your Snowflake account (e.g., `abc12345.us-east-1`)
- `your_username` with your Snowflake username
- `your_password` with your Snowflake password

**Need help?** See `docs/ENV_TEMPLATE.md` for detailed instructions.

### 3. Launch Jupyter (30 seconds)

```bash
# Make sure your environment is activated
conda activate gwas_intelligence

# Start Jupyter
jupyter notebook
```

Your browser should open automatically to `http://localhost:8888`

### 4. Open the Notebook (30 seconds)

1. Click on `gwas_extraction_demo.ipynb`
2. Select kernel: **Kernel → Change kernel → Python (gwas_intelligence)**
3. You should see "Python (gwas_intelligence)" in the top-right corner

### 5. Run Setup Cells (1 minute)

Run cells **1-18** in order (Shift+Enter or Cell → Run All Above):

```
Cell 1:  ✅ Imports
Cell 2:  ✅ Configuration
Cell 3:  ✅ Create Database
Cell 4:  ✅ Create Schemas
Cell 5:  ✅ Create Stage
Cells 6-17: ✅ Create Tables
Cell 18: ✅ Connect to Snowflake
```

**Expected output**:
```
✅ Imports successful!
✅ Configuration set!
✅ Connected to Snowflake!
   User: YOUR_USER
   Warehouse: DEMO_JGH
   Database: GWAS
✅ Database GWAS created
✅ Schema PDF_RAW created
✅ Schema PDF_PROCESSING created
✅ Stage PDF_STAGE created
✅ All tables created successfully
```

**If you see errors**, check:
- Your `.env` file has correct credentials
- You have `CREATE DATABASE` privilege (or use `ACCOUNTADMIN`)
- Your warehouse is running

## First PDF Processing (5-10 minutes)

### 1. Prepare a Test PDF

Download a GWAS paper or use your own. Example:
- https://www.frontiersin.org/articles/10.3389/fpls.2024.1373081/full
- Save as `~/Downloads/gwas_paper.pdf`

### 2. Upload PDF to Snowflake (Cell 19)

Update the cell with your PDF path:

```python
# Cell 19 - Update this line
local_pdf_path = "/Users/yourusername/Downloads/gwas_paper.pdf"
```

Run the cell. Expected output:
```
📤 Uploading PDF to Snowflake stage...
   Local file: /Users/yourusername/Downloads/gwas_paper.pdf
   Stage: @GWAS.PDF_RAW.PDF_STAGE
✅ Upload complete!
   File: gwas_paper.pdf (1.2 MB)
```

### 3. Run the Pipeline (Cells 20-43)

**Option A: Run All at Once**
```
Cell → Run All Below
```

**Option B: Run Step-by-Step** (recommended for first time)
1. Cell 20-21: Parse PDF (1-5 min) ⏳
2. Cell 22: Create images (1-2 min)
3. Cell 23-27: Generate embeddings (2-3 min)
4. Cell 28-33: Create search service (1 min)
5. Cell 34-41: Extract traits (2-5 min)
6. Cell 42-43: Merge results (30 sec)

**Total time**: 5-15 minutes depending on PDF size

### 4. View Results (Cell 44)

Run the final cell to see extracted traits:

```python
# Cell 44 - View Results
results_df = session.sql(f"""
    SELECT 
        trait,
        chromosome,
        start_position,
        end_position,
        gene_name,
        marker_name,
        p_value,
        extraction_confidence
    FROM {DATABASE_NAME}.{SCHEMA_PROCESSING}.GWAS_TRAIT_ANALYTICS
    WHERE document_id = '{DOCUMENT_ID}'
    ORDER BY extraction_confidence DESC
""").to_pandas()

print(f"\n📊 Extracted {len(results_df)} traits from {DOCUMENT_ID}\n")
results_df
```

## Success! 🎉

You should now see a table with extracted GWAS traits including:
- Trait name
- Chromosome
- Genomic positions
- Gene names
- Markers (SNPs/QTLs)
- P-values
- Confidence levels

## Next Steps

### Process More PDFs

To process additional papers, just update and re-run:
- Cell 19: Upload new PDF
- Cells 20-44: Process and extract

### Query Your Data

```sql
-- View all extracted traits
SELECT * FROM GWAS.PDF_PROCESSING.GWAS_TRAIT_ANALYTICS;

-- Count traits by chromosome
SELECT chromosome, COUNT(*) as trait_count
FROM GWAS.PDF_PROCESSING.GWAS_TRAIT_ANALYTICS
GROUP BY chromosome
ORDER BY chromosome;

-- Find high-confidence extractions
SELECT trait, gene_name, p_value
FROM GWAS.PDF_PROCESSING.GWAS_TRAIT_ANALYTICS
WHERE extraction_confidence = 'HIGH'
ORDER BY p_value;
```

### Clean Up (For Re-testing)

If you want to start fresh:

```sql
-- Option 1: Drop and recreate tables
DROP TABLE IF EXISTS GWAS.PDF_PROCESSING.GWAS_TRAIT_ANALYTICS CASCADE;
DROP TABLE IF EXISTS GWAS.PDF_PROCESSING.MULTIMODAL_PAGES CASCADE;
-- etc...

-- Option 2: Drop entire database
DROP DATABASE IF EXISTS GWAS;
-- Then re-run cells 1-18
```

## Troubleshooting Quick Tips

### "Authentication failed"
→ Check your `.env` file, verify account format: `account.region`

### "Insufficient privileges"
→ Use a role with `CREATE DATABASE` or ask admin to grant privileges

### "Cortex function not found"
→ Verify Cortex AI is enabled in your Snowflake account

### Cell hangs at "Parsing PDF..."
→ This is normal! `AI_PARSE_DOCUMENT` takes 1-5 minutes. Be patient.

### "Cannot convert Column to bool"
→ Missing `.collect()` - should be fixed in latest notebook

### PDF upload fails
→ Check file path, use absolute path, verify file exists

## Need More Help?

- **Full documentation**: See `README.md`
- **Environment setup**: See `docs/ENV_TEMPLATE.md`
- **Troubleshooting**: See `README.md` Troubleshooting section
- **Development notes**: See `docs/development/`

---

**That's it! You're now extracting GWAS traits from research papers!** 🧬✨

For questions or issues, open a GitHub issue or check the documentation.
