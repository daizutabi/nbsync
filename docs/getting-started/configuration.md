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
