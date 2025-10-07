# Documentation

This directory contains all project documentation organized by category.

## 📁 Directory Structure

```
docs/
├── README.md                    # This file
├── development/                 # Development notes, experiments, AI-generated explanations
├── deployment/                  # Deployment guides and instructions
└── security/                    # Security documentation and guidelines
```

## 📂 Folder Purposes

### `/development/`
- Development notes and experiments
- Cursor/AI-generated explanations
- Technical deep-dives
- Architecture decisions
- Code exploration notes

**Example files:**
- `snowflake-cortex-exploration.md`
- `embedding-model-comparison.md`
- `performance-optimization-notes.md`

### `/deployment/`
- Deployment guides
- Infrastructure setup
- CI/CD documentation
- Environment configuration
- Release procedures

**Example files:**
- `snowflake-setup-guide.md`
- `streamlit-deployment.md`
- `environment-setup.md`

### `/security/`
- Security best practices
- Credential management
- Access control documentation
- Compliance notes
- Security checklists

**Example files:**
- `credential-management.md`
- `snowflake-security-model.md`
- `data-privacy-guidelines.md`

## 📝 Documentation Guidelines

### When to Create Documentation

1. **Always document**:
   - Setup procedures
   - Architecture decisions
   - Complex algorithms
   - Security practices
   - Deployment processes

2. **Consider documenting**:
   - Debugging sessions (if lessons learned)
   - Performance optimizations
   - Model selection rationale
   - Data schemas

3. **Don't document**:
   - Obvious code behavior
   - Temporary experiments (use `/scratch/` instead)
   - Personal notes (keep local or in scratch)

### Documentation Best Practices

1. **Use clear titles** - Make it easy to find what you need
2. **Include dates** - Add creation/update dates at the top
3. **Link related docs** - Cross-reference related documentation
4. **Keep it current** - Update docs when code changes
5. **Use examples** - Show code snippets and examples
6. **Add context** - Explain *why*, not just *what*

### Markdown Formatting

Use consistent formatting:
- `# H1` for title
- `## H2` for major sections
- `### H3` for subsections
- Code blocks with language: \`\`\`python
- Lists for steps or items
- Tables for comparisons
- Emojis for visual organization (optional but helpful)

## 🔗 Main Documentation Files

Key documentation files in the root directory:

- **README.md** - Project overview, quick start
- **LICENSE** - Project license
- **SECURITY_CHECKLIST.md** - Security guidelines
- **CONTRIBUTING.md** - Contribution guidelines (if created)
- **CHANGELOG.md** - Version history (if created)

## 🤖 AI Assistant Guidelines

When Cursor creates documentation:
- Place in appropriate `/docs/` subfolder
- Use clear, descriptive filenames
- Add date and context at the top
- Link to related code files
- Update this README if adding new categories

## 📚 Additional Resources

- [Markdown Guide](https://www.markdownguide.org/)
- [Technical Writing Best Practices](https://developers.google.com/tech-writing)
- [Documentation-Driven Development](https://gist.github.com/zsup/9434452)

