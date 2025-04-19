# Configuration

Configuring nbsync for your MkDocs site is simple but powerful, allowing you to
customize how notebooks and Python files are integrated with your documentation.

## Basic Configuration

To use nbsync with MkDocs, add it to your `mkdocs.yml` file:

```yaml
plugins:
  - search
  - nbsync
```

This minimal configuration uses all the default settings.

## Source Directory Configuration

Specify where nbsync should look for notebooks and Python files:

```yaml
plugins:
  - search
  - nbsync:
      src_dir:
        - ../notebooks # Path to notebooks directory
        - ../scripts # Path to Python scripts
```

The `src_dir` option can be:

- A single path as a string
- A list of paths
- Relative to your docs directory
- Absolute paths (use with caution)

## Advanced Configuration

### Execution Settings

Control how notebooks are executed:

```yaml
plugins:
  - search
  - nbsync:
      execute:
        enabled: true # Enable notebook execution
        timeout: 300 # Maximum execution time in seconds
        kernel: python3 # Jupyter kernel to use
        allow_errors: false # Stop on first error
```

### Output Settings

Configure how outputs are handled:

```yaml
plugins:
  - search
  - nbsync:
      output:
        format: png # Output format (png, svg, html)
        dpi: 150 # Resolution for raster formats
        width: 800 # Default width for outputs
        height: auto # Default height for outputs
        include_source: true # Include source code with outputs
```

### Caching Settings

Optimize build performance with caching:

```yaml
plugins:
  - search
  - nbsync:
      cache:
        enabled: true # Enable caching
        dir: .cache/nbsync # Cache directory
        timeout: 3600 # Cache timeout in seconds
        invalidate_on_config: true # Invalidate cache on config changes
```

## Complete Configuration Example

Below is a comprehensive configuration example with all options:

```yaml
plugins:
  - search
  - nbsync:
      src_dir:
        - ../notebooks
        - ../scripts
      execute:
        enabled: true
        timeout: 300
        kernel: python3
        allow_errors: false
        env:
          MY_VAR: "value"
      output:
        format: png
        dpi: 150
        width: 800
        height: auto
        include_source: true
        theme: light
      cache:
        enabled: true
        dir: .cache/nbsync
        timeout: 3600
        invalidate_on_config: true
      watch:
        enabled: true # Auto-reload on file changes
        interval: 2 # Check interval in seconds
      debug: false # Enable debug mode
```

## Environment-Specific Configuration

You can use environment variables to control nbsync behavior:

```yaml
plugins:
  - search
  - nbsync:
      execute:
        enabled: !ENV [NBSYNC_EXECUTE, true]
        timeout: !ENV [NBSYNC_TIMEOUT, 300]
```

This allows different settings for development and production environments.

## Working with Other Plugins

nbsync integrates well with other MkDocs plugins:

```yaml
plugins:
  - search
  - social # Generate social cards
  - nbsync:
      # nbsync settings
  - git-revision-date-localized:
      # Show last update date
```

Ensure nbsync appears before plugins that might process its output.
