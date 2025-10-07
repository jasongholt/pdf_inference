# 🧹 Recommended Cleanup Actions

These are optional cleanup actions to further organize your repository:

## SQL Files in Root

Consider moving these SQL files to appropriate directories:

```bash
# Move to sql/setup/
mv setup.sql sql/setup/
mv setup_container.sql sql/setup/
mv recreate_app.sql sql/setup/

# Or if they're Streamlit-specific, keep in root
# (since they're deployment scripts for Streamlit app)
```

## File Organization

Current root files:
- ✅ .cursorrules - Keep (AI config)
- ✅ .cursorignore - Keep (AI config)
- ✅ .gitignore - Keep (git config)
- ✅ .env - Keep (credentials, gitignored)
- ✅ README.md - Keep (project overview)
- ✅ LICENSE - Keep (license)
- ✅ PROJECT_STRUCTURE.md - Keep (structure guide)
- ✅ CURSOR_QUICK_REFERENCE.md - Keep (quick ref)
- ✅ gwas_extraction_demo.ipynb - Keep (main notebook)
- ⚠️ setup.sql - Consider moving to /sql/setup/
- ⚠️ setup_container.sql - Consider moving to /sql/setup/
- ⚠️ recreate_app.sql - Consider moving to /sql/setup/

## Commands to Clean Up

```bash
# Option 1: Move SQL files
mkdir -p sql/setup
mv *.sql sql/setup/

# Option 2: Leave Streamlit deployment SQL in root
# (if they're frequently used for deployment)

# Clean Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# Clean Jupyter checkpoints
find . -type d -name .ipynb_checkpoints -exec rm -rf {} + 2>/dev/null

# List what's in root now
ls -1
```

## Before First Commit

```bash
# 1. Clear notebook outputs
jupyter nbconvert --clear-output --inplace gwas_extraction_demo.ipynb

# 2. Review what will be committed
git status

# 3. Verify .env is not staged
git ls-files | grep -i .env
# Should return nothing

# 4. Add files
git add .cursorrules .cursorignore .gitignore
git add PROJECT_STRUCTURE.md CURSOR_QUICK_REFERENCE.md
git add README.md LICENSE
git add gwas_extraction_demo.ipynb
git add docs/ tests/ src/ sql/
git add scratch/README.md

# 5. Commit
git commit -m "feat: Add Cursor AI configuration and project structure

- Added .cursorrules with Snowflake/Streamlit best practices
- Added .cursorignore for performance
- Updated .gitignore with scratch/ and temp file patterns
- Created organized directory structure
- Added comprehensive documentation
- MCP server integration for notebooks and Snowflake docs
- Security best practices enforced"

# 6. Push
git push origin main
```

## Optional: Move SECURITY_CHECKLIST.md

Already done! Moved to `docs/security/SECURITY_CHECKLIST.md`

## Regular Maintenance

Set up a weekly cleanup routine:

```bash
# Add to crontab or run manually
# Clean old scratch files
find scratch/ -type f -mtime +7 -delete

# Clean Python cache
find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null

# Clean Jupyter checkpoints  
find . -name .ipynb_checkpoints -type d -exec rm -rf {} + 2>/dev/null
```

Save as a script: `cleanup.sh`

```bash
#!/bin/bash
echo "🧹 Cleaning temporary files..."
find scratch/ -type f -mtime +7 -delete 2>/dev/null
find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null
find . -name .ipynb_checkpoints -type d -exec rm -rf {} + 2>/dev/null
echo "✅ Cleanup complete!"
```

Make executable: `chmod +x cleanup.sh`

Run weekly: `./cleanup.sh`
