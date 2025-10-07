# Cursor Setup Notes

**Created:** October 7, 2025

## Overview

This document describes the Cursor AI configuration and project structure setup for the GWAS Intelligence project.

## Files Created

### Configuration Files
1. **`.cursorrules`** - Main AI behavior configuration
   - Defines file placement rules
   - Snowflake best practices
   - Streamlit coding patterns
   - Security requirements
   - MCP server usage guidelines

2. **`.cursorignore`** - Performance optimization
   - Excludes large/generated files from AI indexing
   - Speeds up Cursor by focusing on relevant code

3. **`.gitignore`** (updated) - Security and cleanliness
   - Added `scratch/` directory
   - Added temp file patterns (`*_scratch.py`, `debug_*.py`, etc.)
   - Protects all temporary and experimental files

### Documentation
1. **`PROJECT_STRUCTURE.md`** - Complete structure guide
2. **`CURSOR_QUICK_REFERENCE.md`** - Quick reference card
3. **`docs/README.md`** - Documentation organization guide
4. **`scratch/README.md`** - Scratch directory guide
5. **This file** - Setup notes

### Directory Structure
```
Created organized folders:
- docs/development/    (dev notes, experiments)
- docs/deployment/     (deployment guides)
- docs/security/       (security docs)
- tests/unit/          (unit tests)
- tests/integration/   (integration tests)
- tests/fixtures/      (test fixtures)
- scratch/             (temporary files, gitignored)
- sql/setup/           (database setup)
- sql/queries/         (query templates)
- src/utils/           (utility code)
```

## How It Works

### File Placement Rules

The `.cursorrules` file instructs Cursor AI to:

1. **Documentation (.md files)**
   - Root: Only README.md, LICENSE, CONTRIBUTING.md, etc.
   - Everything else → `/docs/` subdirectories

2. **Code (.py files)**
   - Production code → `/src/`
   - Tests → `/tests/`
   - Temporary/experiments → `/scratch/`

3. **SQL scripts**
   - Setup → `/sql/setup/`
   - Queries → `/sql/queries/`

4. **Temporary files**
   - All go to `/scratch/` (gitignored)
   - Includes: debug_*.py, temp_*.py, *_scratch.py

### MCP Server Integration

The `.cursorrules` file references two MCP servers:

1. **Notebook MCP** - For editing Jupyter notebooks
   - Can modify cells programmatically
   - Clear outputs
   - Add/remove cells

2. **Snowflake Docs MCP** - Query Snowflake documentation
   - Look up syntax
   - Check available models
   - Get best practices

### Best Practices Encoded

**Snowflake:**
- Always use environment variables for credentials
- Uppercase SQL keywords
- Fully qualify table names (DB.SCHEMA.TABLE)
- Use `get_active_session()` in Streamlit
- Cache expensive queries
- Leverage Cortex AI properly

**Streamlit:**
- Cache data with `@st.cache_data(ttl=600)`
- Cache resources with `@st.cache_resource`
- Use session state for state management
- Minimize reruns with forms
- Provide user feedback

**Security:**
- Never commit credentials
- Clear notebook outputs
- Use .env for secrets
- Check before commits

## Benefits

1. **Clean Repository**
   - No clutter in root directory
   - Organized folder structure
   - Gitignored temporary files

2. **Consistent Behavior**
   - AI always knows where to put files
   - Follows project conventions
   - Suggests cleanup when needed

3. **Security**
   - Built-in credential checks
   - Reminds about sensitive data
   - Clear notebook output reminders

4. **Performance**
   - `.cursorignore` speeds up AI
   - Focuses on relevant code
   - Ignores large data files

5. **Collaboration**
   - Clear structure for team members
   - Documented conventions
   - Easy onboarding

## Customization

To customize behavior, edit `.cursorrules`:

```bash
# Open in Cursor
cursor .cursorrules

# Key sections to customize:
# - File Organization Rules (lines ~25-50)
# - Snowflake Best Practices (lines ~75-150)
# - Streamlit Best Practices (lines ~155-225)
# - Security Rules (lines ~350-375)
```

## Common Issues & Solutions

### Issue: Files Still Created in Root

**Cause:** AI might not be reading `.cursorrules`

**Solution:**
1. Verify `.cursorrules` exists in root
2. Restart Cursor
3. Be specific in prompts: "Create in docs/development/"

### Issue: Too Many Temp Files

**Cause:** Not using `/scratch/` directory

**Solution:**
1. Move experiments to `/scratch/`
2. Set up cleanup cron job
3. Use patterns: `debug_*.py`, `temp_*.py`

### Issue: Cursor Slow

**Cause:** Indexing large files

**Solution:**
1. Check `.cursorignore` is present
2. Add large file patterns
3. Exclude output directories

## Maintenance

### Regular Tasks

1. **Clean scratch directory** (weekly)
   ```bash
   find scratch/ -type f -mtime +7 -delete
   ```

2. **Review .cursorrules** (monthly)
   - Update best practices as learned
   - Add new patterns
   - Refine file placement rules

3. **Update documentation** (as needed)
   - Keep PROJECT_STRUCTURE.md current
   - Update CURSOR_QUICK_REFERENCE.md
   - Document new conventions

## Next Steps

### Optional Improvements

1. **Pre-commit Hooks**
   - Auto-clear notebook outputs
   - Check for credentials
   - Enforce file placement

2. **CI/CD Integration**
   - Validate structure in CI
   - Check for files in wrong places
   - Automated cleanup

3. **Team Alignment**
   - Share `.cursorrules` across projects
   - Standardize conventions
   - Document team-specific patterns

## Resources

- `.cursorrules` - Full configuration
- `PROJECT_STRUCTURE.md` - Complete guide
- `CURSOR_QUICK_REFERENCE.md` - Quick tips
- Cursor documentation: https://docs.cursor.sh/

## Conclusion

This setup provides:
- ✅ Clean, organized project structure
- ✅ Automatic file placement
- ✅ Security best practices
- ✅ Snowflake & Streamlit conventions
- ✅ No more root directory clutter!

The AI now knows where files should go and will follow best practices automatically.

