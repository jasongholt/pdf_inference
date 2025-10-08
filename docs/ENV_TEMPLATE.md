# .env File Template

Create a `.env` file in the project root with your Snowflake credentials.

## Template

Copy this content to a new file named `.env` in the project root:

```bash
# Snowflake Connection Configuration
# ===================================
# NEVER commit this file to git!

# Snowflake Account (format: account.region)
# Example: abc12345.us-east-1
SNOWFLAKE_ACCOUNT=your_account_here

# Snowflake User
SNOWFLAKE_USER=your_username_here

# Snowflake Password
SNOWFLAKE_PASSWORD=your_password_here

# Optional: Warehouse (defaults to DEMO_JGH if not set)
SNOWFLAKE_WAREHOUSE=DEMO_JGH

# Optional: Database (defaults to GWAS if not set)
SNOWFLAKE_DATABASE=GWAS

# Optional: Schema (defaults to PDF_PROCESSING if not set)
SNOWFLAKE_SCHEMA=PDF_PROCESSING
```

## Finding Your Snowflake Account

Your Snowflake account identifier has the format: `account.region`

**Example**: `abc12345.us-east-1`

### How to find it:

1. **From Snowflake Web UI URL**:
   - URL: `https://abc12345.us-east-1.snowflakecomputing.com`
   - Account: `abc12345.us-east-1`

2. **From SnowSQL**:
   ```sql
   SELECT CURRENT_ACCOUNT() || '.' || CURRENT_REGION() as account_locator;
   ```

3. **From Snowflake Web UI**:
   - Admin → Accounts
   - Look for "Account Locator" and "Region"

## Example

```bash
# Example .env file
SNOWFLAKE_ACCOUNT=mycompany.us-east-1
SNOWFLAKE_USER=john_doe
SNOWFLAKE_PASSWORD=MySecureP@ssw0rd!
SNOWFLAKE_WAREHOUSE=DEMO_JGH
```

## Testing Your Configuration

After creating your `.env` file, you can test it by running the first few cells of the notebook:

1. Cell 1: Imports (should succeed)
2. Cell 2: Configuration (should succeed)
3. Cell 3: Database & Schema creation (tests connection)

If Cell 3 fails, check:
- Account format is correct
- Username and password are correct
- User has required privileges
- Network can reach Snowflake (not blocked by firewall)

## Security Notes

- ✅ `.env` is in `.gitignore` - it won't be committed
- ✅ Never share your `.env` file
- ✅ Use different credentials for dev/prod
- ✅ Consider using key-pair authentication for production
- ✅ Rotate passwords regularly

## Alternative: Key-Pair Authentication

For production, consider using key-pair authentication instead of passwords:

```bash
SNOWFLAKE_ACCOUNT=mycompany.us-east-1
SNOWFLAKE_USER=john_doe
SNOWFLAKE_PRIVATE_KEY_PATH=/path/to/private_key.p8
SNOWFLAKE_PRIVATE_KEY_PASSPHRASE=optional_passphrase
```

See Snowflake documentation for setting up key-pair auth:
https://docs.snowflake.com/en/user-guide/key-pair-auth
