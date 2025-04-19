# Installation

Installing nbsync is straightforward and can be done using pip, the Python
package manager.

## Prerequisites

Before installing nbsync, ensure you have the following:

- Python 3.8 or higher
- pip (Python package manager)
- MkDocs (documentation generator)

## Basic Installation

Install nbsync using pip:

```bash
pip install nbsync
```

This command installs the latest stable version of nbsync and its core
dependencies.

## Installation with Optional Dependencies

For full functionality, install with all optional dependencies:

```bash
pip install nbsync[all]
```

This includes:

- Jupyter kernel support
- Advanced visualization capabilities
- All supported file format handlers

## Development Installation

If you want to contribute to nbsync or use the latest development version:

```bash
git clone https://github.com/daizutabi/nbsync.git
cd nbsync
pip install -e .
```

## Verifying Installation

After installation, verify that nbsync is correctly installed:

```bash
pip show nbsync
```

You should see information about the installed version of nbsync.

## Compatibility

nbsync is compatible with:

- MkDocs 1.4.0+
- Python 3.8+
- Jupyter Notebook 6.0+
- JupyterLab 3.0+

## Troubleshooting

### Common Installation Issues

If you encounter issues during installation:

1. **Dependency Conflicts**: Try installing in a fresh virtual environment

   ```bash
   python -m venv nbsync-env
   source nbsync-env/bin/activate  # On Windows: nbsync-env\Scripts\activate
   pip install nbsync
   ```

2. **Permission Errors**: Use user installation

   ```bash
   pip install --user nbsync
   ```

3. **Outdated Dependencies**: Update pip and setuptools
   ```bash
   pip install --upgrade pip setuptools
   ```

### Getting Help

If you continue to experience installation issues:

- Check the [GitHub Issues](https://github.com/daizutabi/nbsync/issues) for
  similar problems
- Open a new issue with details of your environment and the error messages
