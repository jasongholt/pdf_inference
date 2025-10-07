# Project Structure

## 📁 Directory Organization

```
gwas_intelligence/
├── .cursorrules                 # Cursor AI configuration and best practices
├── .env                        # Environment variables (gitignored)
├── .gitignore                  # Git ignore rules
├── LICENSE                     # Project license
├── README.md                   # Project overview
├── SECURITY_CHECKLIST.md       # Security guidelines
├── PROJECT_STRUCTURE.md        # This file
│
├── docs/                       # All documentation
│   ├── README.md              # Documentation index
│   ├── development/           # Development notes, experiments
│   ├── deployment/            # Deployment guides
│   └── security/              # Security documentation
│
├── src/                       # Source code
│   └── utils/                 # Utility functions
│
├── scripts/                   # Scripts
│   ├── python/                # Python scripts
│   └── sql/                   # SQL scripts (alternative location)
│
├── sql/                       # SQL scripts (primary location)
│   ├── setup/                 # Database setup scripts
│   ├── queries/               # Query templates
│   └── migrations/            # Schema migrations
│
├── tests/                     # Test suite
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   └── fixtures/              # Test data and fixtures
│
├── notebooks/                 # Jupyter notebooks (if multiple)
│   └── *.ipynb
│
├── scratch/                   # Temporary/experimental files (gitignored)
│   └── README.md             # Scratch directory guide
│
├── output/                    # Generated outputs (gitignored)
│   ├── data/                  # Processed data
│   ├── reports/               # Generated reports
│   └── logs/                  # Log files
│
└── config/                    # Configuration files
    └── *.example              # Example configs (no secrets)
```

## 📝 File Organization Rules

### Root Directory
**Only these files belong in root:**
- Core notebooks (main analysis/demo notebooks)
- Essential config files (.cursorrules, .gitignore, .env)
- Project documentation (README.md, LICENSE, etc.)
- Package files (requirements.txt, pyproject.toml, environment.yml)

**Do NOT create in root:**
- Random .md files → Use `/docs/`
- Test scripts → Use `/tests/` or `/scratch/`
- Temporary files → Use `/scratch/`
- SQL scripts → Use `/sql/`

### Documentation Files
```
README.md                  → Root (project overview)
LICENSE                    → Root (license)
CONTRIBUTING.md            → Root (contribution guide)
CHANGELOG.md               → Root (version history)
SECURITY_CHECKLIST.md      → Root or /docs/security/
PROJECT_STRUCTURE.md       → Root (this file)

All other .md files        → /docs/ subdirectories
```

### Python Code
```
Main application code      → /src/
Utility functions         → /src/utils/
Standalone scripts        → /scripts/python/
Test files               → /tests/
Notebooks                → Root or /notebooks/
Temporary experiments    → /scratch/
```

### SQL Scripts
```
Setup scripts            → /sql/setup/
Query templates          → /sql/queries/
Schema migrations        → /sql/migrations/
Deployment SQL           → /sql/deployment/
```

### Configuration Files
```
.env                     → Root (gitignored)
.env.example             → Root (template, committed)
config.yml               → /config/ or root
*.example files          → Same location as actual file
```

## 🤖 AI Assistant Behavior

### When Creating New Files

**Documentation (.md):**
```
Q: "Create a doc about X"
A: Creates /docs/development/x-explanation.md
   (or appropriate /docs/ subfolder)
```

**Python Scripts (.py):**
```
Q: "Create a utility for X"
A: Creates /src/utils/x_utility.py

Q: "Create a test for X"
A: Creates /tests/unit/test_x.py

Q: "Let's test something quickly"
A: Creates /scratch/test_x.py
```

**SQL Scripts (.sql):**
```
Q: "Create setup SQL"
A: Creates /sql/setup/setup_x.sql

Q: "Write a query for X"
A: Creates /sql/queries/query_x.sql
```

### Cursor Rules Monitoring

The `.cursorrules` file includes these automatic behaviors:

1. **File Placement**: AI will suggest appropriate directories
2. **Naming Conventions**: Consistent naming across the project
3. **Cleanup Reminders**: Suggest removing scratch files when done
4. **Security Checks**: Warn before creating files with credentials
5. **Documentation First**: Offer to document complex explanations

## 🧹 Keeping the Project Clean

### Regular Cleanup Tasks

```bash
# Remove old scratch files
find scratch/ -type f -mtime +30 -delete

# Clean Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Clean Jupyter checkpoints
find . -type d -name .ipynb_checkpoints -exec rm -r {} +

# Clean output files (careful!)
rm -rf output/*
```

### What Gets Gitignored

✅ **Automatically gitignored:**
- `/scratch/` - All temporary files
- `/output/` - Generated outputs
- `.env` - Environment variables
- `__pycache__/` - Python cache
- `*.pyc, *.pyo` - Compiled Python
- `.ipynb_checkpoints/` - Notebook checkpoints
- `*_scratch.py` - Scratch scripts
- `temp_*.py, debug_*.py` - Temp files

✅ **Committed to git:**
- `/docs/` - Documentation
- `/tests/` - Test suite
- `/src/` - Source code
- `/sql/` - SQL scripts
- `.cursorrules` - Cursor configuration
- `README.md` - Project docs
- Requirements files

## 📊 Project Workflow

### 1. Development
```
1. Explore in /scratch/ or notebooks
2. Move working code to /src/
3. Create tests in /tests/
4. Document in /docs/
```

### 2. Adding Features
```
1. Create feature branch
2. Write code in appropriate directory
3. Add tests
4. Update documentation
5. Clear notebook outputs
6. Commit and push
```

### 3. Deployment
```
1. Review /docs/deployment/ guides
2. Run setup scripts from /sql/setup/
3. Deploy application
4. Document any changes
```

## 🎯 Quick Reference

| File Type | Primary Location | Alternative | Gitignored? |
|-----------|-----------------|-------------|-------------|
| Documentation | `/docs/` | Root (key docs only) | No |
| Python code | `/src/` | `/scripts/python/` | No |
| Tests | `/tests/` | - | No |
| SQL scripts | `/sql/` | `/scripts/sql/` | No |
| Notebooks | Root or `/notebooks/` | - | No (clear outputs!) |
| Temp files | `/scratch/` | - | Yes |
| Output | `/output/` | - | Yes |
| Configs | `/config/` or root | - | Depends |
| Credentials | `.env` | - | Yes |

## 🔍 Finding Files

```bash
# Find all Python files (excluding cache)
find . -name "*.py" -not -path "*/__pycache__/*"

# Find all docs
find docs/ -name "*.md"

# Find all SQL
find sql/ -name "*.sql"

# Find large files
find . -type f -size +10M

# Show directory sizes
du -sh */ | sort -h
```

## 🤝 Team Collaboration

### For New Team Members

1. **Read this file first** to understand structure
2. **Check `.cursorrules`** for AI behavior and best practices
3. **Review `/docs/`** for project documentation
4. **Use `/scratch/`** for learning/exploration
5. **Ask questions** before creating files in unusual places

### For AI Assistants

1. **Always suggest** appropriate directory for new files
2. **Remind users** to clean `/scratch/` periodically
3. **Warn** if creating files in root unnecessarily
4. **Offer to document** complex operations in `/docs/`
5. **Follow conventions** defined in `.cursorrules`

## ✅ Checklist Before Committing

- [ ] All new .md files are in `/docs/` (except root essentials)
- [ ] Test files are in `/tests/`
- [ ] No files in `/scratch/` are being committed (it's gitignored)
- [ ] Notebook outputs are cleared
- [ ] No credentials in any files
- [ ] File is in appropriate directory per this guide
- [ ] `.cursorrules` guidelines were followed

---

**Remember:** A well-organized project is easier to maintain, collaborate on, and scale!

