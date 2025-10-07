# 🔒 Security Checklist for GitHub Repository

## ✅ Pre-Commit Security Checklist

Before pushing to GitHub, ensure all items below are completed:

### 1. **Credentials & Secrets**
- [ ] ✅ `.env` file is in `.gitignore` and NOT committed
- [ ] ✅ `.env.example` template is created (with no real credentials)
- [ ] ✅ No API keys, tokens, or passwords in code
- [ ] ✅ No private keys (`.pem`, `.key`, `.p8`) committed
- [ ] ✅ Snowflake credentials stored in environment variables only

### 2. **Configuration Files**
- [ ] ✅ All sensitive config files are gitignored
- [ ] ✅ No hardcoded connection strings
- [ ] ✅ No hardcoded account identifiers (partially acceptable for docs)
- [ ] ✅ Use environment variables for all credentials

### 3. **Data Files**
- [ ] ✅ No sensitive data files (CSV, Excel, databases) committed
- [ ] ✅ No PDFs with proprietary/confidential content
- [ ] ✅ Sample data is anonymized/synthetic
- [ ] ✅ Large files are excluded (use Git LFS if needed)

### 4. **Jupyter Notebooks**
- [ ] ⚠️ **ACTION NEEDED**: Clear all notebook outputs before committing
- [ ] ✅ No credentials in notebook cells
- [ ] ⚠️ Check for accidentally printed secrets in output cells
- [ ] ✅ Use `os.environ.get()` for all sensitive values

### 5. **Git History**
- [ ] ✅ No sensitive data in previous commits
- [ ] ✅ If secrets were committed, history must be rewritten
- [ ] ✅ Consider using tools like `git-secrets` or `trufflehog`

### 6. **Documentation**
- [ ] ✅ README doesn't contain credentials
- [ ] ✅ Deployment docs reference environment variables
- [ ] ✅ Include setup instructions without exposing secrets
- [ ] ✅ Add security best practices to documentation

---

## 🛡️ Current Security Status

### ✅ Completed
- Created comprehensive `.gitignore` for Python/Jupyter/Snowflake
- `.env` file is gitignored
- Notebook uses environment variables for credentials
- No hardcoded passwords found in notebook
- Added `.env.example` template

### ⚠️ Action Required

#### **CRITICAL: Clean Notebook Outputs**
Your notebook `gwas_extraction_demo.ipynb` may contain outputs that include:
- Query results with data
- Connection status messages
- Potentially sensitive information in cell outputs

**Before committing, run:**
```bash
# Option 1: Clear all outputs using Jupyter
jupyter nbconvert --clear-output --inplace gwas_extraction_demo.ipynb

# Option 2: Using nbstripout (install first)
pip install nbstripout
nbstripout gwas_extraction_demo.ipynb

# Option 3: Manual - in Jupyter: Kernel > Restart & Clear Output
```

#### **Check Account References**
The following files may contain account-specific references:
- Deployment scripts reference `SFSENORTHAMERICA-DEMOJHOLTAWSW`
- Database name `SYNGENTA` appears in multiple files

**Decision needed:**
- If sharing publicly → Replace with placeholders or environment variables
- If sharing with team/organization → May be acceptable, verify with security policy

---

## 🔐 Best Practices for Production

### Recommended: Use Key-Pair Authentication
Instead of passwords, use Snowflake key-pair authentication:

1. **Generate key pair:**
```bash
# Generate private key
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt

# Generate public key
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

2. **Update Snowflake user:**
```sql
ALTER USER your_username SET RSA_PUBLIC_KEY='YOUR_PUBLIC_KEY_HERE';
```

3. **Update your code:**
```python
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

with open("rsa_key.p8", "rb") as key:
    p_key = serialization.load_pem_private_key(
        key.read(),
        password=None,
        backend=default_backend()
    )

session = Session.builder.configs({
    "account": os.environ.get("SNOWFLAKE_ACCOUNT"),
    "user": os.environ.get("SNOWFLAKE_USER"),
    "private_key": p_key,
    # No password needed!
}).create()
```

### Additional Security Measures

1. **GitHub Secrets Scanning**
   - Enable GitHub's secret scanning in repository settings
   - Add custom patterns for your organization

2. **Pre-commit Hooks**
   ```bash
   # Install pre-commit
   pip install pre-commit
   
   # Create .pre-commit-config.yaml
   cat > .pre-commit-config.yaml <<EOF
   repos:
     - repo: https://github.com/pre-commit/pre-commit-hooks
       rev: v4.4.0
       hooks:
         - id: check-added-large-files
         - id: check-json
         - id: check-yaml
         - id: detect-private-key
         - id: end-of-file-fixer
         - id: trailing-whitespace
     
     - repo: https://github.com/Yelp/detect-secrets
       rev: v1.4.0
       hooks:
         - id: detect-secrets
   EOF
   
   # Install hooks
   pre-commit install
   ```

3. **Environment Variable Management**
   - Use `.env` for local development
   - Use secret managers for production (AWS Secrets Manager, Azure Key Vault, etc.)
   - Never log environment variables

4. **Regular Security Audits**
   ```bash
   # Scan for secrets in git history
   pip install trufflehog
   trufflehog --regex --entropy=False .
   
   # Or use gitleaks
   brew install gitleaks
   gitleaks detect --source . --verbose
   ```

---

## 📋 Quick Pre-Push Commands

Run these before pushing to GitHub:

```bash
# 1. Check git status
git status

# 2. Clear notebook outputs
jupyter nbconvert --clear-output --inplace gwas_extraction_demo.ipynb

# 3. Verify .env is not tracked
git ls-files | grep .env
# Should return nothing (or only .env.example)

# 4. Check for sensitive patterns
git diff --cached | grep -i "password\|secret\|key\|token\|api"

# 5. Add files safely
git add .gitignore
git add gwas_extraction_demo.ipynb
git add LICENSE README.md

# 6. Commit with meaningful message
git commit -m "Initial commit: GWAS extraction pipeline with security best practices"

# 7. Push to GitHub
git push origin main
```

---

## 🚨 If You Accidentally Commit Secrets

### Immediate Steps:
1. **Rotate the compromised credentials immediately**
2. **Remove from git history:**
   ```bash
   # Using git-filter-repo (recommended)
   pip install git-filter-repo
   git filter-repo --path .env --invert-paths
   
   # Or using BFG Repo-Cleaner
   java -jar bfg.jar --delete-files .env
   git reflog expire --expire=now --all && git gc --prune=now --aggressive
   ```
3. **Force push (only if repository is private/not shared):**
   ```bash
   git push origin --force --all
   ```

### For Public Repositories:
- Assume all committed secrets are compromised
- Rotate ALL credentials immediately
- Consider GitHub support for removing sensitive data
- Update security policies

---

## 📚 Additional Resources

- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Snowflake Key-Pair Authentication](https://docs.snowflake.com/en/user-guide/key-pair-auth)
- [OWASP Secrets Management](https://owasp.org/www-community/vulnerabilities/Sensitive_Data_Exposure)
- [Git Secrets Tool](https://github.com/awslabs/git-secrets)

---

## ✅ Final Checklist

Before pushing to GitHub:
- [ ] All credentials in `.env` (not committed)
- [ ] `.env.example` created and committed
- [ ] Notebook outputs cleared
- [ ] No sensitive data in repository
- [ ] `.gitignore` is comprehensive
- [ ] Pre-commit hooks installed (optional but recommended)
- [ ] Team/collaborators aware of security practices

**Remember:** Once code is pushed to GitHub, assume it's public forever (even in private repos).

