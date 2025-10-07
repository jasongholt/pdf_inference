/*
 * 🧬 GWAS Trait Viewer - Streamlit App Setup
 * ============================================
 * Run this SQL script BEFORE deploying the Streamlit app
 * to ensure all required resources exist.
 */

-- Set context
USE ROLE ACCOUNTADMIN;
USE DATABASE SYNGENTA;
USE SCHEMA PDF_PROCESSING;
USE WAREHOUSE SYNGENTA_DOC_AI_WH_MEDIUM;

-- =============================
-- 1️⃣ CREATE STAGE FOR STREAMLIT
-- =============================
CREATE STAGE IF NOT EXISTS STREAMLIT_STAGE
  COMMENT = 'Stage for Streamlit app source files';

-- Verify stage created
SHOW STAGES LIKE 'STREAMLIT_STAGE';

-- =============================
-- 2️⃣ VERIFY COMPUTE POOL EXISTS
-- =============================
SHOW COMPUTE POOLS;

-- If compute pool doesn't exist, create it:
-- (Uncomment if needed)
/*
CREATE COMPUTE POOL IF NOT EXISTS CPU_X64_XS
  MIN_NODES = 1
  MAX_NODES = 3
  INSTANCE_FAMILY = CPU_X64_XS
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = FALSE
  COMMENT = 'Compute pool for Streamlit apps on containers';
*/

-- =============================
-- 3️⃣ VERIFY EXTERNAL ACCESS INTEGRATION
-- =============================
SHOW INTEGRATIONS LIKE 'PYPI%';

-- If integration doesn't exist, create it:
-- (Uncomment if needed)
/*
-- Create network rule for PyPI
CREATE OR REPLACE NETWORK RULE PYPI_NETWORK_RULE
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('pypi.org', 'pypi.python.org', 'pythonhosted.org', 'files.pythonhosted.org');

-- Create external access integration
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION PYPI_ACCESS_INTEGRATION
  ALLOWED_NETWORK_RULES = (PYPI_NETWORK_RULE)
  ENABLED = TRUE
  COMMENT = 'Allow access to PyPI for package installation';
*/

-- =============================
-- 4️⃣ GRANT PERMISSIONS (if needed)
-- =============================

-- Grant usage on compute pool
-- GRANT USAGE ON COMPUTE POOL CPU_X64_XS TO ROLE ACCOUNTADMIN;

-- Grant usage on external access integration
-- GRANT USAGE ON INTEGRATION PYPI_ACCESS_INTEGRATION TO ROLE ACCOUNTADMIN;

-- Grant Streamlit creation privilege
GRANT CREATE STREAMLIT ON SCHEMA SYNGENTA.PDF_PROCESSING TO ROLE ACCOUNTADMIN;

-- =============================
-- 5️⃣ VERIFY DATA TABLES EXIST
-- =============================
SHOW TABLES IN SCHEMA SYNGENTA.PDF_PROCESSING;

-- Check if we have data
SELECT 
    'PARSED_DOCUMENTS' as table_name,
    COUNT(*) as row_count
FROM SYNGENTA.PDF_PROCESSING.PARSED_DOCUMENTS

UNION ALL

SELECT 
    'GWAS_TRAIT_ANALYTICS' as table_name,
    COUNT(*) as row_count
FROM SYNGENTA.PDF_PROCESSING.GWAS_TRAIT_ANALYTICS

UNION ALL

SELECT 
    'MULTIMODAL_PAGES' as table_name,
    COUNT(*) as row_count
FROM SYNGENTA.PDF_PROCESSING.MULTIMODAL_PAGES;

-- =============================
-- ✅ SETUP COMPLETE!
-- =============================
SELECT '✅ Setup verification complete! Ready to deploy Streamlit app.' as status;

