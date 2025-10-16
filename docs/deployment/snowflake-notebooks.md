# Running GWAS Notebook in Snowflake Notebooks

## Overview

The `gwas_extraction_demo.ipynb` notebook is designed to run in **both** environments:
- ✅ **Local development** (with `.env` credentials)
- ✅ **Snowflake Notebooks** (Container Runtime with `get_active_session()`)

## Architecture

### Dual Environment Detection

The notebook automatically detects its execution environment:

```python
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
    # Running in Snowflake Notebooks
except:
    # Running locally - use credentials from .env
    session = Session.builder.configs({...}).create()
```

## Local Development Setup

### Prerequisites
1. Python 3.10+ with uv venv
2. `.env` file with credentials
3. Jupyter notebook server

### Steps
1. **Activate venv**:
   ```bash
   source .venv/bin/activate  # or use uv venv
   ```

2. **Create `.env` file**:
   ```bash
   SNOWFLAKE_ACCOUNT=your-account
   SNOWFLAKE_USER=your-username
   SNOWFLAKE_PASSWORD=your-password
   SNOWFLAKE_ROLE=ACCOUNTADMIN
   SNOWFLAKE_WAREHOUSE=your-warehouse
   ```

3. **Run notebook**:
   ```bash
   jupyter notebook gwas_extraction_demo.ipynb
   ```

## Snowflake Notebooks Setup

### Prerequisites
1. Snowflake account with Notebooks feature enabled
2. Compute pool for Container Runtime
3. External Access Integration (for PyPI packages)

### Creating a Notebook in Snowflake

#### Option 1: Via Snowsight UI

1. **Navigate to Notebooks**:
   - Sign in to Snowsight
   - Go to **Projects** → **Notebooks**
   - Click **+ Notebook**

2. **Configure Settings**:
   - **Name**: `GWAS_Extraction_Demo`
   - **Location**: `GWAS.PDF_PROCESSING`
   - **Runtime**: `Run on container`
   - **Runtime Version**: `Python 3.11` (CPU or GPU)
   - **Compute Pool**: Select or create a compute pool

3. **Upload Notebook**:
   - Upload `gwas_extraction_demo.ipynb`
   - Or copy/paste cells manually

4. **Run**: All cells will use `get_active_session()` automatically

#### Option 2: Via SQL

```sql
-- 1. Create compute pool (if not exists)
CREATE COMPUTE POOL IF NOT EXISTS GWAS_COMPUTE_POOL
  MIN_NODES = 1
  MAX_NODES = 3
  INSTANCE_FAMILY = CPU_X64_S;

-- 2. Create external access integration for PyPI
CREATE OR REPLACE NETWORK RULE pypi_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('pypi.org', 'pypi.python.org', 'pythonhosted.org', 'files.pythonhosted.org');

CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION pypi_access_integration
  ALLOWED_NETWORK_RULES = (pypi_network_rule)
  ENABLED = TRUE;

-- 3. Create notebook
CREATE NOTEBOOK GWAS.PDF_PROCESSING.GWAS_EXTRACTION_DEMO
  FROM '@GWAS.PDF_RAW.PDF_STAGE/gwas_extraction_demo.ipynb'
  QUERY_WAREHOUSE = DEMO_JGH
  COMPUTE_POOL = GWAS_COMPUTE_POOL
  RUNTIME_NAME = 'PYTHON_RUNTIME_3_11'
  EXTERNAL_ACCESS_INTEGRATIONS = (pypi_access_integration)
  COMMENT = 'GWAS trait extraction pipeline';
```

### Required Packages

The Container Runtime comes with most packages pre-installed. Additional packages needed:

```python
# Install in notebook cell if needed
import sys
!{sys.executable} -m pip install python-dotenv PyMuPDF
```

**Note**: In Snowflake Notebooks, `python-dotenv` is optional since credentials come from `get_active_session()`.

## Key Differences

### Local Execution
- ✅ Requires `.env` file with credentials
- ✅ Uses `Session.builder.configs()` to create session
- ✅ Full control over warehouse, role, database
- ✅ Can use local file system for PDFs

### Snowflake Notebooks Execution
- ✅ No `.env` file needed
- ✅ Uses `get_active_session()` for session
- ✅ Inherits notebook's warehouse and role
- ✅ PDFs must be in Snowflake stages
- ✅ Access to GPU compute (if compute pool has GPUs)
- ✅ Native integration with Snowflake features

## Best Practices

### For Both Environments

1. **Always use session object**: Don't create multiple sessions
2. **Use stages for file storage**: Never use local file paths in production
3. **Clean up temporary tables**: Use `TRANSIENT` tables for intermediate results
4. **Monitor costs**: Track warehouse and compute pool usage

### For Snowflake Notebooks

1. **Use compute pools efficiently**:
   - Stop compute pool when not in use
   - Right-size: Start with small, scale if needed
   - Use GPU pools only for GPU-intensive tasks

2. **Manage external access**:
   - Create specific network rules for each service
   - Use least-privilege access integrations
   - Monitor external data egress

3. **Package management**:
   - Pin package versions for reproducibility
   - Test package installations in notebook
   - Consider creating custom runtime image for production

## Troubleshooting

### "No module named 'snowflake.snowpark.context'"
- **Cause**: Running locally with old snowflake-snowpark-python version
- **Fix**: Upgrade: `pip install --upgrade snowflake-snowpark-python`

### "Session no longer exists"
- **Cause**: Session expired (common in long-running notebooks)
- **Fix**: Re-run connection cell to refresh session

### "Cannot import get_active_session"
- **Cause**: Running locally (expected behavior)
- **Fix**: Ensure `.env` file exists with valid credentials

### "External access denied" (Snowflake Notebooks)
- **Cause**: Missing external access integration for PyPI
- **Fix**: Create external access integration (see SQL above)
- **Alternative**: Ask admin to grant access

## Performance Considerations

### Local Development
- **Pros**: Fast iteration, full control, easy debugging
- **Cons**: Limited compute, network latency to Snowflake

### Snowflake Notebooks
- **Pros**: Scales with Snowflake, no network latency, GPU access
- **Cons**: Compute pool costs, slower package installation

### Recommendation
1. **Develop locally**: Fast prototyping and debugging
2. **Test in Snowflake Notebooks**: Validate production behavior
3. **Deploy as Snowflake Notebook**: For scheduled/production runs

## Cost Optimization

### Compute Pools
- Use **suspend_timeout_seconds**: Auto-stop when idle
- Right-size instance family: CPU vs GPU, size tiers
- Share compute pools across notebooks

### Warehouses
- Use X-SMALL for development
- Scale up only for production/large datasets
- Use `AUTO_SUSPEND` and `AUTO_RESUME`

## Security

### Local Development
- ✅ Never commit `.env` file (in `.gitignore`)
- ✅ Use key-pair authentication instead of passwords
- ✅ Rotate credentials regularly

### Snowflake Notebooks
- ✅ Use role-based access control (RBAC)
- ✅ Limit external access integrations
- ✅ Audit notebook access and usage
- ✅ Use secrets for external API keys

## Next Steps

1. **Test locally**: Run the notebook with your `.env` file
2. **Create compute pool**: Set up Snowflake container runtime
3. **Upload to Snowflake**: Create notebook in Snowsight
4. **Compare results**: Ensure both environments produce same output

## Resources

- [Snowflake Notebooks Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-ml/notebooks-on-spcs)
- [Container Runtime Guide](https://docs.snowflake.com/en/developer-guide/snowpark-container-services/overview)
- [External Access Integrations](https://docs.snowflake.com/en/developer-guide/external-network-access/creating-using-external-network-access)
- [Compute Pools](https://docs.snowflake.com/en/sql-reference/sql/create-compute-pool)

