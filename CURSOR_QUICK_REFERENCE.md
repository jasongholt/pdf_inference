# 🚀 Cursor Quick Reference

Quick reference for working with this project using Cursor AI.

## 📁 Where Do Files Go?

| I want to create... | Put it in... | Why? |
|---------------------|-------------|------|
| Documentation | `/docs/development/` | Keeps docs organized |
| Security notes | `/docs/security/` | Security-specific docs |
| Deployment guide | `/docs/deployment/` | Deployment docs |
| Python utility | `/src/utils/` | Reusable code |
| Test file | `/tests/unit/` or `/tests/integration/` | Proper test structure |
| SQL query | `/sql/queries/` | Query templates |
| Setup SQL | `/sql/setup/` | Database setup |
| Quick experiment | `/scratch/` | Gitignored, temporary |
| Debug script | `/scratch/` | Gitignored, temporary |
| Notebook | Root or `/notebooks/` | Main notebooks visible |

## 🤖 Cursor AI Features

### Available MCP Servers

1. **Notebook MCP** - Edit Jupyter notebooks
   ```
   "Edit the notebook to add a new cell..."
   "Clear all outputs in the notebook"
   ```

2. **Snowflake Docs MCP** - Query Snowflake documentation
   ```
   "What's the syntax for CREATE SEARCH SERVICE?"
   "Show me Cortex AI embedding models"
   ```

### Cursor Rules (.cursorrules)

The `.cursorrules` file tells Cursor AI:
- ✅ Where to place new files
- ✅ Snowflake best practices
- ✅ Streamlit coding patterns
- ✅ Security requirements
- ✅ Code style preferences

**You can customize it!** Edit `.cursorrules` to change AI behavior.

## 💬 Helpful Prompts

### Project Organization
```
"Create a development doc about X"
→ Creates /docs/development/x-explanation.md

"Create a test for the loader function"
→ Creates /tests/unit/test_loader.py

"Let me debug this quickly"
→ Creates /scratch/debug_issue.py
```

### Snowflake Development
```
"Query the GWAS_TRAIT_ANALYTICS table"
"Create a search service for multimodal RAG"
"Show me how to use Cortex AI embeddings"
"What's the best way to cache this query?"
```

### Streamlit Development
```
"Add a new page to the Streamlit app"
"How do I cache this data loading?"
"Create a metric card component"
"Fix the rerun issue on this page"
```

### Security & Cleanup
```
"Check for hardcoded credentials"
"Clear notebook outputs before commit"
"What files should I not commit?"
"Clean up the scratch directory"
```

## ⚡ Quick Commands

### Before Committing
```bash
# Clear notebook outputs
jupyter nbconvert --clear-output --inplace gwas_extraction_demo.ipynb

# Check git status
git status

# Verify .env is gitignored
git check-ignore .env

# See what would be committed
git add --dry-run .
```

### Cleanup
```bash
# Clean scratch files older than 7 days
find scratch/ -type f -mtime +7 -delete

# Clean Python cache
find . -name "__pycache__" -exec rm -rf {} +

# Clean Jupyter checkpoints
find . -name ".ipynb_checkpoints" -exec rm -rf {} +
```

### Project Navigation
```bash
# View structure
tree -L 2 -I '__pycache__|.git'

# Find Python files
find src/ -name "*.py"

# Find docs
find docs/ -name "*.md"

# Search in code
grep -r "function_name" src/
```

## 🎯 Common Tasks

### Adding a New Feature

1. **Explore** in `/scratch/` or notebook
   ```
   "Let's prototype the feature in scratch/"
   ```

2. **Implement** in `/src/`
   ```
   "Move this to src/utils/ as a proper function"
   ```

3. **Test** in `/tests/`
   ```
   "Create tests for this utility"
   ```

4. **Document** in `/docs/`
   ```
   "Document this feature in docs/development/"
   ```

### Working with Notebooks

```
# Ask Cursor to edit notebook
"Add a new cell that loads data from Snowflake"
"Clear all notebook outputs"
"Add markdown section explaining this code"

# Before committing
jupyter nbconvert --clear-output --inplace *.ipynb
```

### Snowflake Queries

```
# Ask for best practices
"What's the best way to cache this Snowflake query?"
"How do I use Cortex COMPLETE?"
"Show me the search service syntax"

# Get documentation
"Look up Cortex AI embedding models in Snowflake docs"
```

## 🔒 Security Reminders

### ❌ Never Commit
- `.env` file
- Credentials or passwords
- Private keys (*.pem, *.key)
- Sensitive data files
- Notebook outputs with sensitive data

### ✅ Always Do
- Use environment variables
- Clear notebook outputs
- Check `git status` before commit
- Review diffs: `git diff`
- Keep secrets in `.env` (gitignored)

## 📝 File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Utilities | `{purpose}_utils.py` | `snowflake_utils.py` |
| Tests | `test_{module}.py` | `test_loader.py` |
| SQL Setup | `setup_{purpose}.sql` | `setup_tables.sql` |
| SQL Query | `query_{purpose}.sql` | `query_traits.sql` |
| Docs | `{topic}-{detail}.md` | `cortex-embedding-guide.md` |
| Scratch | `debug_*.py` or `temp_*.py` | `debug_connection.py` |

## 🎨 Cursor Settings Tips

### Recommended Settings

1. **Enable Cursor Rules** - Already set up in `.cursorrules`
2. **Use .cursorignore** - Speeds up AI by ignoring irrelevant files
3. **Enable Copilot++** - Better code suggestions
4. **Use Cmd+K** - Quick inline edits
5. **Use Cmd+L** - Open chat

### Customizing Behavior

Edit `.cursorrules` to:
- Change where files are created
- Add project-specific patterns
- Define custom code style
- Add domain-specific knowledge

## 🆘 Troubleshooting

### Cursor Creating Files in Wrong Place

**Problem:** AI creates files in root instead of `/docs/`

**Solution:** 
1. Check `.cursorrules` is present
2. Be specific: "Create in docs/development/"
3. Remind: "Following .cursorrules, where should this go?"

### Too Much Clutter

**Problem:** Lots of temp files everywhere

**Solution:**
1. Use `/scratch/` for experiments
2. Set up regular cleanup
3. Review `.gitignore` patterns
4. Use `.cursorignore` to hide from AI

### AI Doesn't Know Snowflake Syntax

**Problem:** Incorrect Snowflake SQL

**Solution:**
1. Use Snowflake Docs MCP: "Look up in Snowflake docs"
2. Reference `.cursorrules` Snowflake section
3. Provide example: "Like this pattern..."

## 📚 Additional Resources

- **PROJECT_STRUCTURE.md** - Complete project organization guide
- **.cursorrules** - Full AI behavior configuration
- **docs/README.md** - Documentation guidelines
- **docs/security/SECURITY_CHECKLIST.md** - Security best practices

## 🎯 Daily Workflow

```bash
# 1. Start work
cd gwas_intelligence
source .venv/bin/activate  # if using venv

# 2. Use Cursor AI for development
# - Files go in correct directories automatically
# - Follows best practices from .cursorrules
# - Uses MCP servers for notebooks and Snowflake docs

# 3. Before committing
jupyter nbconvert --clear-output --inplace *.ipynb
git status
git diff

# 4. Clean up
find scratch/ -mtime +7 -delete

# 5. Commit
git add <files>
git commit -m "..."
git push
```

## 💡 Pro Tips

1. **Trust the Structure** - Let Cursor place files in correct folders
2. **Use Scratch** - Experiment freely in `/scratch/`
3. **Ask for Docs** - "Document this in docs/development/"
4. **Clear Outputs** - Before every commit!
5. **Review .cursorrules** - Customize for your workflow
6. **Use MCP Servers** - Leverage notebook and Snowflake docs access
7. **Keep Clean** - Regular cleanup of scratch files

---

**Remember:** The `.cursorrules` file is your project's AI assistant configuration. Customize it as needed!

