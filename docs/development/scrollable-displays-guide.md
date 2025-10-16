# Scrollable Elements in Snowflake Notebooks

## Overview

This guide shows how to create scrollable HTML displays in Snowflake Notebooks (and Jupyter notebooks) for better data visualization when dealing with large tables or long content.

## Key Features Added

### 1. Scrollable Table Container
```css
.table-container {
    max-height: 400px;         /* Fixed height */
    overflow-y: auto;          /* Vertical scroll */
    overflow-x: auto;          /* Horizontal scroll */
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

**Benefits:**
- ✅ Table scrolls vertically when it has many rows
- ✅ Also scrolls horizontally for wide tables
- ✅ Maintains clean layout with fixed height
- ✅ Works in both Snowflake and Jupyter notebooks

### 2. Sticky Table Header
```css
.data-table thead {
    position: sticky;
    top: 0;
    z-index: 10;
}
```

**Benefits:**
- ✅ Header stays visible while scrolling
- ✅ Always know which column you're looking at
- ✅ Professional table UX

### 3. Custom Scrollbar Styling
```css
.table-container::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
.table-container::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
}
```

**Benefits:**
- ✅ Cleaner, more compact scrollbars
- ✅ Matches overall design aesthetic
- ✅ Works in Chrome, Edge, Safari

### 4. Full Container Scroll (Optional)
```css
.results-container {
    max-height: 900px;
    overflow-y: auto;
}
```

**Benefits:**
- ✅ Entire display scrolls if needed
- ✅ Useful for very long outputs
- ✅ Can be adjusted or removed

## HTML Structure

```html
<div class="results-container">
    <!-- Metrics cards (always visible) -->
    <div class="metric-container">
        <!-- Cards here -->
    </div>
    
    <!-- Scrollable table -->
    <div class="table-container">
        <table class="data-table">
            <thead>
                <!-- Sticky header -->
            </thead>
            <tbody>
                <!-- Scrollable rows -->
            </tbody>
        </table>
    </div>
    
    <!-- Info sections (visible when scrolled) -->
</div>
```

## Usage in Python

```python
from IPython.display import HTML, display

html = """
<style>
    .table-container {
        max-height: 400px;
        overflow-y: auto;
        overflow-x: auto;
    }
    
    .data-table thead {
        position: sticky;
        top: 0;
        background: white;
        z-index: 10;
    }
</style>

<div class="table-container">
    <table class="data-table">
        <!-- Your table content -->
    </table>
</div>
"""

display(HTML(html))
```

## Adjustable Parameters

### Table Height
```css
/* Small table (10-15 rows visible) */
max-height: 300px;

/* Medium table (15-20 rows visible) */
max-height: 400px;

/* Large table (20-30 rows visible) */
max-height: 600px;

/* Very large (30+ rows visible) */
max-height: 800px;
```

### Scrollbar Width
```css
/* Thin scrollbar */
.table-container::-webkit-scrollbar {
    width: 6px;
}

/* Standard scrollbar */
width: 8px;

/* Wide scrollbar (easier to grab) */
width: 12px;
```

### Scroll Behavior
```css
/* Smooth scrolling */
.table-container {
    scroll-behavior: smooth;
}

/* Hide scrollbar until hover (macOS style) */
.table-container {
    overflow-y: auto;
    scrollbar-width: thin;  /* Firefox */
}
.table-container::-webkit-scrollbar {
    width: 0px;  /* Hidden by default */
}
.table-container:hover::-webkit-scrollbar {
    width: 8px;  /* Shown on hover */
}
```

## Common Use Cases

### 1. Large Data Tables

**Problem:** 50+ rows make the notebook hard to navigate

**Solution:**
```python
html = f"""
<style>
    .table-container {{ max-height: 400px; overflow-y: auto; }}
    .data-table thead {{ position: sticky; top: 0; }}
</style>
<div class="table-container">
    <table class="data-table">
        <!-- 100 rows of data -->
    </table>
</div>
"""
```

### 2. Wide Tables (Many Columns)

**Problem:** Table extends beyond screen width

**Solution:**
```python
html = f"""
<style>
    .table-container {{ 
        max-height: 500px;
        overflow-x: auto;  /* Enable horizontal scroll */
        overflow-y: auto;
    }}
</style>
<div class="table-container">
    <table class="data-table" style="min-width: 1200px;">
        <!-- Wide table with 15+ columns -->
    </table>
</div>
"""
```

### 3. Long Text Content

**Problem:** Long markdown/text output clutters notebook

**Solution:**
```python
html = f"""
<style>
    .content-container {{
        max-height: 300px;
        overflow-y: auto;
        padding: 15px;
        background: #f5f5f5;
        border-radius: 8px;
    }}
</style>
<div class="content-container">
    {long_text_content}
</div>
"""
```

### 4. Code Output

**Problem:** Long code snippets or logs

**Solution:**
```python
html = f"""
<style>
    .code-container {{
        max-height: 400px;
        overflow-y: auto;
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 15px;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
    }}
</style>
<div class="code-container">
    <pre>{code_output}</pre>
</div>
"""
```

## Browser Compatibility

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| `overflow-y: auto` | ✅ | ✅ | ✅ | ✅ |
| `position: sticky` | ✅ | ✅ | ✅ | ✅ |
| `::-webkit-scrollbar` | ✅ | ❌ | ✅ | ✅ |
| `scrollbar-width` | ❌ | ✅ | ❌ | ❌ |

**Note:** Firefox uses `scrollbar-width: thin;` instead of webkit styles.

## Complete Example

```python
from IPython.display import HTML, display
import pandas as pd

# Generate sample data
data = [{'ID': i, 'Name': f'Item {i}', 'Value': i*10} for i in range(50)]

html = """
<style>
    /* Scrollable container */
    .table-container {
        max-height: 400px;
        overflow-y: auto;
        overflow-x: auto;
        margin: 20px 0;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Table styles */
    .data-table {
        width: 100%;
        border-collapse: collapse;
        background: white;
    }
    
    /* Sticky header */
    .data-table thead {
        position: sticky;
        top: 0;
        z-index: 10;
    }
    
    .data-table th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px;
        text-align: left;
        font-weight: bold;
    }
    
    .data-table td {
        padding: 10px 12px;
        border-bottom: 1px solid #e0e0e0;
        background: white;
    }
    
    .data-table tbody tr:hover {
        background-color: #f5f5f5;
    }
    
    /* Custom scrollbar */
    .table-container::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    .table-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    .table-container::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    
    .table-container::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
</style>

<h3>📊 Scrollable Data Table (50 rows)</h3>
<p style="color: #666;">Use mouse wheel or scrollbar to view all rows. Header stays fixed.</p>

<div class="table-container">
    <table class="data-table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Value</th>
            </tr>
        </thead>
        <tbody>
"""

# Add rows
for item in data:
    html += f"""
            <tr>
                <td>{item['ID']}</td>
                <td>{item['Name']}</td>
                <td>{item['Value']}</td>
            </tr>
    """

html += """
        </tbody>
    </table>
</div>
"""

display(HTML(html))
```

## Tips & Best Practices

### 1. Choose Appropriate Heights

```python
# Rule of thumb:
# - Show 10-20 rows without scrolling
# - Each row ≈ 40-50px with padding
# - 400px = ~10 rows visible

rows_visible = 15
row_height = 45  # pixels
header_height = 50
max_height = (rows_visible * row_height) + header_height  # 725px
```

### 2. Add User Hints

```html
<div style="color: #666; font-size: 13px; margin-bottom: 10px;">
    💡 <strong>Scrollable table</strong> - Use mouse wheel or scrollbar to view all {total_rows} rows
</div>
```

### 3. Combine with Pandas

```python
# Display scrollable pandas dataframe
df_html = df.to_html(classes='data-table', index=False)

html = f"""
<style>
    .table-container {{ max-height: 400px; overflow-y: auto; }}
    .data-table thead {{ position: sticky; top: 0; background: white; }}
</style>
<div class="table-container">
    {df_html}
</div>
"""
display(HTML(html))
```

### 4. Responsive Design

```css
/* Mobile-friendly scrollable tables */
@media (max-width: 768px) {
    .table-container {
        max-height: 300px;  /* Smaller on mobile */
    }
    
    .data-table {
        font-size: 12px;    /* Smaller text */
    }
}
```

### 5. Performance with Large Datasets

For very large tables (1000+ rows), consider:

```python
# Option 1: Pagination
# Show only first 100 rows, add "Load more" button

# Option 2: Virtual scrolling
# Use JavaScript library like Tabulator

# Option 3: Server-side filtering
# Load data on demand as user scrolls
```

## Snowflake-Specific Considerations

### 1. Snowflake Notebooks Container Runtime

Works perfectly with:
- ✅ IPython.display.HTML
- ✅ All CSS features shown above
- ✅ Sticky headers
- ✅ Custom scrollbars

### 2. Streamlit in Snowflake

For Streamlit apps, use native components:
```python
import streamlit as st

# Use st.dataframe with height
st.dataframe(df, height=400)

# Or use container with scrolling
with st.container():
    st.dataframe(df, use_container_width=True)
```

### 3. Snowsight Query Results

Native Snowsight already has scrollable results, but for custom displays:
```sql
-- Use HTML in SQL for custom displays
SELECT 
    '<div class="table-container" style="max-height: 400px; overflow-y: auto;">'
    || table_html 
    || '</div>' as scrollable_display
FROM ...
```

## Troubleshooting

### Sticky Header Not Working

**Problem:** Header scrolls away

**Solution:** Ensure parent has overflow set:
```css
.table-container {
    overflow-y: auto;  /* Must be set */
}
.data-table thead {
    position: sticky;
    top: 0;
    background: white;  /* Must have background */
    z-index: 10;        /* Must be higher than tbody */
}
```

### Scrollbar Not Visible

**Problem:** Content scrolls but no scrollbar appears

**Solution:** 
```css
/* Explicitly show scrollbar */
.table-container {
    overflow-y: scroll;  /* Always show (even if not needed) */
}

/* Or auto (shows only when needed) */
overflow-y: auto;
```

### Table Columns Misaligned

**Problem:** Columns shift when scrolling

**Solution:**
```css
.data-table {
    table-layout: fixed;  /* Fixed column widths */
}

/* Or specify widths */
.data-table th:nth-child(1) { width: 100px; }
.data-table th:nth-child(2) { width: 200px; }
```

### Performance Issues

**Problem:** Slow scrolling with many rows

**Solutions:**
1. Limit rows displayed: `df.head(100)`
2. Use pagination
3. Simplify HTML/CSS
4. Remove :hover effects for large tables

## Summary

Scrollable elements in Snowflake Notebooks provide:

✅ **Better UX** - Clean, organized displays
✅ **Space efficient** - More content in less vertical space
✅ **Professional look** - Sticky headers and smooth scrolling
✅ **Easy to implement** - Just CSS, no JavaScript needed
✅ **Works everywhere** - Jupyter, Snowflake, local notebooks

**Key Pattern:**
```python
display(HTML("""
<style>
    .container { max-height: 400px; overflow-y: auto; }
    thead { position: sticky; top: 0; }
</style>
<div class="container">
    <!-- Your content -->
</div>
"""))
```

Use this pattern for tables, logs, text outputs, or any content that might grow large!

