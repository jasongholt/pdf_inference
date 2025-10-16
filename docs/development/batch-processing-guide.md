# Batch Processing Guide - GWAS Intelligence Pipeline

## Overview

The GWAS Intelligence notebook now supports **batch processing** of multiple PDF files, enabling you to process entire research paper collections in a single run.

## Features

### ✅ Core Capabilities

1. **Automatic File Discovery**
   - Scans Snowflake stage for all PDF files
   - Shows file metadata (size, last modified)
   - Identifies already-processed files

2. **Flexible Processing Modes**
   - **Process All**: Automatically process every PDF in the stage
   - **Selective Processing**: Choose specific files to process
   - **Smart Skip**: Automatically skip already-processed files
   - **Limit Control**: Process only first N files (useful for testing)

3. **Robust Error Handling**
   - Individual file failures don't stop the batch
   - Detailed error messages per file
   - Continues processing remaining files after errors

4. **Progress Tracking**
   - Real-time progress indicator
   - Per-file timing and statistics
   - Batch-wide summary at completion

5. **Comprehensive Statistics**
   - Total processing time
   - Success/failure/skipped counts
   - Average time per file
   - Total pages processed
   - Content size metrics

## Quick Start

### 1. Upload Multiple PDFs

```bash
# Upload PDFs to Snowflake stage
PUT file:///path/to/paper1.pdf @GWAS.PDF_RAW.PDF_STAGE/
PUT file:///path/to/paper2.pdf @GWAS.PDF_RAW.PDF_STAGE/
PUT file:///path/to/paper3.pdf @GWAS.PDF_RAW.PDF_STAGE/
```

Or upload a directory:
```bash
PUT file:///path/to/papers/*.pdf @GWAS.PDF_RAW.PDF_STAGE/
```

### 2. Run Batch Processing Cells

In the notebook, navigate to **Section 4a - Batch Processing Mode** and run:

1. **Cell 1**: Discover all PDFs in stage
2. **Cell 2**: Configure batch processing settings
3. **Cell 3**: Execute batch processing
4. **Cell 4** (optional): View all processed documents

## Configuration Options

### Process All Files

```python
PROCESS_ALL = True
SKIP_EXISTING = True
MAX_FILES = None  # No limit
```

This will:
- Process every PDF in the stage
- Skip files already in the database
- No limit on number of files

### Process Specific Files

```python
PROCESS_ALL = False
SKIP_EXISTING = True
SELECTED_FILES = [
    "fpls-15-1373081.pdf",
    "nature-genetics-2024.pdf",
]
```

This will:
- Only process the specified files
- Skip if they're already processed
- Ignore other PDFs in the stage

### Testing with Limits

```python
PROCESS_ALL = True
SKIP_EXISTING = False  # Reprocess even if exists
MAX_FILES = 5  # Process only first 5 files
```

This is useful for:
- Testing the pipeline with a subset
- Re-processing existing files
- Quick validation runs

## Output Format

### During Processing

```
🚀 Starting batch processing of 5 PDF(s)
   Started at: 2025-10-16 14:23:15
================================================================================

📄 [1/5] Processing: fpls-15-1373081.pdf
--------------------------------------------------------------------------------
   🤖 Calling AI_PARSE_DOCUMENT...
   ✅ Success!
      Pages: 14
      Time: 34.2s

📄 [2/5] Processing: nature-genetics-2024.pdf
--------------------------------------------------------------------------------
   🤖 Calling AI_PARSE_DOCUMENT...
   ✅ Success!
      Pages: 22
      Time: 45.8s

📄 [3/5] Processing: already-processed.pdf
--------------------------------------------------------------------------------
   ⏭️  Already processed (skipping)
      Parsed at: 2025-10-15 10:15:32
      Total pages: 18

...
```

### Batch Summary

```
================================================================================
📊 BATCH PROCESSING SUMMARY
================================================================================

⏱️  Total Time: 156.3s (2.6 minutes)

📈 Results:
   Total files: 5
   ✅ Successful: 3
   ⏭️  Skipped: 1
   ❌ Failed: 1

📄 Processing Stats:
   Total pages processed: 58
   Average time per file: 52.1s
   Average pages per file: 19.3

❌ Failed Files:
   • corrupted-file.pdf
     Error: Invalid PDF format or file not found in stage

✅ Batch processing complete!
   Finished at: 2025-10-16 14:25:51
```

### Database Summary

After processing, run the summary cell to see all processed documents:

```
📊 All Processed Documents in Database
================================================================================
Total documents processed: 12

1. fpls-15-1373081.pdf
   Document ID: fpls-15-1373081.pdf
   Pages: 14
   Content Size: 2.34 MB
   Processed: 2025-10-15 10:15:32

2. nature-genetics-2024.pdf
   Document ID: nature-genetics-2024.pdf
   Pages: 22
   Content Size: 3.87 MB
   Processed: 2025-10-16 14:23:19

...

================================================================================
📈 Summary Statistics
================================================================================
Total documents: 12
Total pages: 234
Total content: 45.67 MB
Average pages per document: 19.5
```

## Best Practices

### 1. Start Small

When processing a new collection:
```python
PROCESS_ALL = True
MAX_FILES = 3  # Test with 3 files first
```

Verify results, then remove limit:
```python
MAX_FILES = None  # Process all remaining files
```

### 2. Monitor Progress

- Watch for consistent timing across files
- Check for error patterns (e.g., all large files failing)
- Verify page counts are reasonable

### 3. Handle Failures

If files fail:
1. Check error messages in summary
2. Verify file exists in stage: `LIST @GWAS.PDF_RAW.PDF_STAGE;`
3. Download and inspect problem file locally
4. Fix or exclude the file
5. Re-run batch with `SKIP_EXISTING = True`

### 4. Optimize Performance

For large batches (50+ files):

**Warehouse Sizing:**
```sql
-- Use larger warehouse for batch processing
ALTER WAREHOUSE DEMO_JGH SET WAREHOUSE_SIZE = 'MEDIUM';

-- Return to small after batch completes
ALTER WAREHOUSE DEMO_JGH SET WAREHOUSE_SIZE = 'X-SMALL';
```

**Process in Chunks:**
```python
# Process 10 files at a time
PROCESS_ALL = True
MAX_FILES = 10
SKIP_EXISTING = True

# Run cell multiple times - each run processes 10 new files
```

### 5. Cost Management

AI_PARSE_DOCUMENT costs scale with:
- Number of pages
- Document complexity
- Processing time

**Estimate before processing:**
- Check file sizes with discovery cell
- Estimate ~30-60 seconds per average paper
- Monitor credits in Snowflake UI

## Comparison: Batch vs Single-File

| Feature | Batch Mode | Single-File Mode |
|---------|------------|------------------|
| **Processing** | Multiple PDFs in one run | One PDF at a time |
| **Setup** | Minimal - auto-discovers files | Manual - set PDF_FILENAME each time |
| **Progress** | Comprehensive batch statistics | Per-file output only |
| **Error Handling** | Continues on errors | Stops on error |
| **Use Case** | Production, large collections | Development, debugging |
| **Time Efficiency** | High - process overnight | Low - requires monitoring |
| **Skip Logic** | Automatic | Manual deletion required |

## Common Workflows

### Workflow 1: Initial Collection Processing

```python
# 1. Upload all PDFs
# PUT file:///research_papers/*.pdf @GWAS.PDF_RAW.PDF_STAGE/

# 2. Discover files (Cell 1)
# Shows: "Found 47 PDF files in stage"

# 3. Test with 3 files (Cell 2)
PROCESS_ALL = True
MAX_FILES = 3

# 4. Run batch processing (Cell 3)
# Verify results look good

# 5. Process remaining files (Cell 2)
MAX_FILES = None  # Process all

# 6. Run batch processing again (Cell 3)
# SKIP_EXISTING = True ensures only new files are processed
```

### Workflow 2: Incremental Updates

```python
# New PDFs added to stage periodically

# 1. Discover files (Cell 1)
# Shows: "Total PDFs in stage: 50"
# Shows: "Already processed: 43"
# Shows: "Ready to process: 7"

# 2. Configure to process new files only (Cell 2)
PROCESS_ALL = True
SKIP_EXISTING = True  # This is the key!
MAX_FILES = None

# 3. Run batch processing (Cell 3)
# Only 7 new files will be processed
```

### Workflow 3: Selective Reprocessing

```python
# Need to reprocess specific files (e.g., after pipeline improvements)

# 1. Delete existing records
DELETE FROM GWAS.PDF_RAW.PARSED_DOCUMENTS
WHERE document_id IN ('paper1.pdf', 'paper2.pdf');

# 2. Configure selective processing (Cell 2)
PROCESS_ALL = False
SELECTED_FILES = ['paper1.pdf', 'paper2.pdf']
SKIP_EXISTING = False

# 3. Run batch processing (Cell 3)
# Only specified files are reprocessed
```

### Workflow 4: Testing New PDFs

```python
# Test batch processing on a small subset before full run

# 1. Upload test PDFs to separate folder
# PUT file:///test/*.pdf @GWAS.PDF_RAW.PDF_STAGE/test/

# 2. Process test files first
PROCESS_ALL = False
SELECTED_FILES = [
    'test/sample1.pdf',
    'test/sample2.pdf',
]

# 3. Verify results

# 4. Process main collection
PROCESS_ALL = True
SKIP_EXISTING = True
```

## Troubleshooting

### No PDFs Found

**Symptom:** "No PDF files found in stage root"

**Solutions:**
1. Verify upload: `LIST @GWAS.PDF_RAW.PDF_STAGE;`
2. Check file extensions (must be `.pdf`)
3. Ensure files are at root level, not in subdirectories
4. Re-upload if needed

### All Files Skipped

**Symptom:** "Skipped: 5" but you want to reprocess

**Solution:**
```python
SKIP_EXISTING = False  # Force reprocessing
```

Or delete specific records:
```sql
DELETE FROM GWAS.PDF_RAW.PARSED_DOCUMENTS
WHERE document_id = 'file-to-reprocess.pdf';
```

### Batch Processing Hangs

**Symptom:** Processing stops at one file

**Causes:**
- Large PDF (100+ pages)
- Complex layouts
- Snowflake warehouse suspended

**Solutions:**
1. Increase warehouse size temporarily
2. Check Snowflake query history for timeout errors
3. Process large files individually with increased timeout
4. Exclude problem file and process rest of batch

### High Failure Rate

**Symptom:** "Failed: 8/10 files"

**Investigation:**
1. Check error messages in batch summary
2. Verify files are valid PDFs:
   ```bash
   # Local validation
   file *.pdf
   ```
3. Check stage permissions
4. Verify AI_PARSE_DOCUMENT access
5. Check file sizes (very large files may timeout)

### Inconsistent Timing

**Symptom:** Some files take 10s, others 180s

**Expected:** 
- Timing varies with:
  - Page count
  - Document complexity (tables, images)
  - OCR needs (scanned vs digital)
  - Current warehouse load

**Normal range:** 20-90 seconds per typical research paper

## Performance Benchmarks

Based on typical GWAS research papers:

| Document Type | Avg Pages | Avg Time | Pages/Second |
|--------------|-----------|----------|--------------|
| Journal article | 8-15 | 30-45s | 0.3 |
| Research paper | 15-25 | 45-75s | 0.3 |
| Review paper | 25-40 | 75-120s | 0.3 |
| Supplement | 5-50 | 20-150s | 0.25 |

**Batch of 50 papers (avg 20 pages each):**
- Estimated time: 40-60 minutes
- Total pages: ~1,000
- Expected cost: ~$5-10 (varies by Snowflake pricing)

## Future Enhancements

Potential improvements to batch processing:

1. **Parallel Processing**
   - Use Snowpark Python UDFs for parallelization
   - Process multiple files simultaneously
   - Reduce total batch time

2. **Smart Retry Logic**
   - Automatically retry failed files with different settings
   - Exponential backoff for transient errors
   - Separate queue for problem files

3. **Progressive Results**
   - Save results incrementally (not just at end)
   - Enable partial batch recovery
   - Real-time dashboard integration

4. **File Prioritization**
   - Process smaller files first (quick wins)
   - Deprioritize large or complex files
   - User-defined priority queue

5. **Quality Checks**
   - Validate extracted content quality
   - Flag low-confidence extractions
   - Suggest manual review candidates

## API Integration

For programmatic batch processing:

```python
# Example: Snowflake Stored Procedure for batch processing
CREATE OR REPLACE PROCEDURE process_pdf_batch(
    max_files INT DEFAULT NULL
)
RETURNS TABLE (filename STRING, status STRING, pages INT, time_seconds FLOAT)
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'batch_process'
AS
$$
def batch_process(session, max_files):
    # Implementation of batch logic
    # Returns results as table
    pass
$$;

-- Call the procedure
CALL process_pdf_batch(10);
```

## Summary

Batch processing transforms the GWAS Intelligence Pipeline from a single-file tool into a production-ready system for processing entire research paper collections:

✅ **Efficiency**: Process dozens of papers in one run
✅ **Reliability**: Robust error handling and recovery
✅ **Visibility**: Comprehensive progress and statistics
✅ **Flexibility**: Multiple processing modes for different scenarios
✅ **Cost-Effective**: Smart skip logic avoids redundant processing

Perfect for:
- Literature reviews (50-200 papers)
- Ongoing research tracking (incremental updates)
- Bulk database population
- Production pipelines

---

**Next Steps:**
1. Try batch processing with 3-5 test PDFs
2. Review results and statistics
3. Scale to your full collection
4. Set up automated incremental processing

