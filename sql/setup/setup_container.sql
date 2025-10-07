/*
 * 🐳 Convert Streamlit App to SPCS Container Runtime
 * ===================================================
 * Run this SQL after deploying the app with SnowCLI
 * to convert it from warehouse runtime to container runtime.
 */

USE ROLE ACCOUNTADMIN;
USE DATABASE SYNGENTA;
USE SCHEMA PDF_PROCESSING;

-- =============================
-- 1️⃣ ALTER APP TO USE CONTAINER RUNTIME
-- =============================

ALTER STREAMLIT GWAS_TRAIT_VIEWER
  SET RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
      COMPUTE_POOL = CPU_X64_XS
      EXTERNAL_ACCESS_INTEGRATIONS = (PYPI_ACCESS_INTEGRATION);

-- =============================
-- 2️⃣ VERIFY CONFIGURATION
-- =============================

-- Show app details
SHOW STREAMLIT LIKE 'GWAS_TRAIT_VIEWER' IN SCHEMA SYNGENTA.PDF_PROCESSING;

-- Check app properties
DESC STREAMLIT GWAS_TRAIT_VIEWER;

-- =============================
-- 3️⃣ CHECK STATUS
-- =============================

-- Monitor app status (run periodically)
SELECT 
    SYSTEM$GET_STREAMLIT_STATUS('GWAS_TRAIT_VIEWER') as status;

-- =============================
-- 🎯 OPTIONAL: MANUAL SHUTDOWN
-- =============================

-- If you need to shut down the app to free compute pool node:
-- ALTER STREAMLIT GWAS_TRAIT_VIEWER SHUTDOWN;

-- To restart, just access it from Snowsight - it will auto-restart

-- =============================
-- 🔄 OPTIONAL: REVERT TO WAREHOUSE
-- =============================

-- If you need to revert to warehouse runtime:
/*
ALTER STREAMLIT GWAS_TRAIT_VIEWER
  SET RUNTIME_NAME = 'SYSTEM$WAREHOUSE_RUNTIME';
*/

-- =============================
-- ✅ SETUP COMPLETE!
-- =============================
SELECT '✅ Container runtime configured! App will build on next access.' as status;

