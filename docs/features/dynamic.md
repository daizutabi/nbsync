# Dynamic Updates and Execution

nbsync provides powerful capabilities for dynamic notebook execution and
real-time updates, ensuring your documentation always reflects your current
code.

## On-Demand Execution

Execute notebooks during documentation builds with the `.execute` option:

```markdown
![Description](notebook.ipynb){.execute}
```

This ensures that your notebook is always executed with the latest code before
being included in your documentation.

## Automatic Updates

When running MkDocs in serve mode, nbsync automatically:

1. Detects changes to referenced notebooks and Python files
2. Re-executes affected notebooks
3. Updates the documentation in real-time

This creates a seamless development workflow where you can edit your code and
immediately see the results in your documentation.

## Execution Options

### Execution Context

Control the execution environment with custom options:

```markdown
![Description](notebook.ipynb){.execute kernel="python3" timeout=60}
```

Options include:

- `kernel`: Specify which Jupyter kernel to use
- `timeout`: Set maximum execution time in seconds
- `env`: Define environment variables for execution

### Selective Execution

Execute only specific cells within a notebook:

```markdown
![First visualization](notebook.ipynb){.execute #fig1}
![Second visualization](notebook.ipynb){.execute #fig2}
```

This allows you to reference and execute only the parts of notebooks that you
need for a particular documentation page.

## Caching

nbsync implements smart caching to avoid unnecessary re-execution:

- Results are cached based on content hash
- Only changed notebooks are re-executed
- Cache can be explicitly invalidated when needed

Configure caching behavior in your `mkdocs.yml`:

```yaml
plugins:
  - nbsync:
      cache_dir: .cache/nbsync
      cache_timeout: 3600 # seconds
```

## Error Handling

nbsync provides robust error handling for execution failures:

- Clear error messages shown in the documentation
- Option to continue building despite execution errors
- Detailed logs for debugging execution issues

Control error behavior in your configuration:

```yaml
plugins:
  - nbsync:
      halt_on_error: false
      error_format: "detailed"
```

## Real-World Use Cases

### Continuous Integration

Automatically execute notebooks as part of your CI/CD pipeline to ensure
documentation accuracy:

```yaml
# In GitHub Actions workflow
- name: Build documentation
  run: |
    pip install mkdocs-material nbsync
    mkdocs build
```

### Interactive Documentation

Create interactive documentation that automatically updates as users interact
with examples:

```markdown
Try changing the parameters:

Parameter: `{slider:1:10:1}`

![Result](notebook.ipynb){.execute param=$slider}
```

### Regular Updates

Schedule regular execution of documentation to keep visualizations current with
underlying data:

```bash
# Cron job for regular updates
0 0 * * * cd /path/to/docs && mkdocs build --clean
```
