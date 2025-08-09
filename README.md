# nbsync

[![PyPI Version][pypi-v-image]][pypi-v-link]
[![Python Version][python-v-image]][python-v-link]
[![Build Status][GHAction-image]][GHAction-link]
[![Coverage Status][codecov-image]][codecov-link]

<strong>Connect Jupyter notebooks and Markdown documents</strong>

nbsync is a core library that seamlessly bridges Jupyter notebooks and Markdown documents, enabling dynamic content synchronization and execution.

## Why Use nbsync?

### The Documentation Challenge

Data scientists, researchers, and technical writers face a common dilemma:

- **Development happens in notebooks** - ideal for experimentation and visualization
- **Documentation lives in markdown** - perfect for narrative and explanation
- **Connecting the two is painful** - screenshots break, exports get outdated

### Our Solution

nbsync creates a live bridge between your notebooks and markdown documents by:

- **Keeping environments separate** - work in the tool best suited for each task
- **Maintaining connections** - reference specific figures from notebooks
- **Automating updates** - changes to notebooks reflect in documentation

## Key Benefits

- **True Separation of Concerns**:
  Develop visualizations in Jupyter notebooks and write documentation
  in markdown files, with each tool optimized for its purpose.

- **Intuitive Markdown Syntax**:
  Use standard image syntax with a simple extension to reference
  notebook figures: `![alt text](notebook.ipynb){#figure-id}`

- **Automatic Updates**:
  When you modify your notebooks, your documentation updates
  automatically.

- **Clean Source Documents**:
  Your markdown remains readable and focused on content, without
  code distractions or complex embedding techniques.

- **Enhanced Development Experience**:
  Take advantage of IDE features like code completion and syntax
  highlighting in the appropriate environment.

## Quick Start

### 1. Installation

```bash
pip install nbsync
```

### 2. Basic Usage

```python
from nbsync.sync import Synchronizer
from nbstore import Store

# Initialize with a notebook store
store = Store("path/to/notebooks")
sync = Synchronizer(store)

# Process markdown with notebook references
markdown_text = """
# My Document

![Chart description](my-notebook.ipynb){#my-figure}
"""

# Convert markdown with notebook references to final output
for element in sync.convert(markdown_text):
    # Process each element (string or Cell objects)
    print(element)
```

### 3. Mark Figures in Your Notebook

In your Jupyter notebook, identify figures with a comment:

```python
# #my-figure
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot([1, 2, 3, 4], [10, 20, 25, 30])
```

### 4. Reference in Markdown

Use standard Markdown image syntax with the figure identifier:

```markdown
![Chart description](my-notebook.ipynb){#my-figure}
```

### Control how results render

You can control how executed outputs render using attributes:

- `source`: where to place the source relative to the result.
  Supported values include `on`/`1` (above), `below`, `only`,
  `material-block`, `tabbed-left`, `tabbed-right`. See tests for details.
- `result`: wrap the execution result in a fenced code block using the
  given language (similar to mkdocs-exec). For example:

````markdown
```python exec="1" result="text"
print(2)
```
````

## The Power of Separation

Creating documentation and developing visualizations involve different
workflows and timeframes. When building visualizations in Jupyter notebooks,
you need rapid cycles of execution, verification, and modification.

nbsync is designed specifically to address these separation of
concerns, allowing you to:

- **Focus on code** in notebooks without documentation distractions
- **Focus on narrative** in markdown without code interruptions
- **Maintain powerful connections** between both environments

Each environment is optimized for its purpose, while nbsync
handles the integration automatically.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

<!-- Badges -->
[pypi-v-image]: https://img.shields.io/pypi/v/nbsync.svg
[pypi-v-link]: https://pypi.org/project/nbsync/
[python-v-image]: https://img.shields.io/pypi/pyversions/nbsync.svg
[python-v-link]: https://pypi.org/project/nbsync
[GHAction-image]: https://github.com/daizutabi/nbsync/actions/workflows/ci.yaml/badge.svg?branch=main&event=push
[GHAction-link]: https://github.com/daizutabi/nbsync/actions?query=event%3Apush+branch%3Amain
[codecov-image]: https://codecov.io/github/daizutabi/nbsync/coverage.svg?branch=main
[codecov-link]: https://codecov.io/github/daizutabi/nbsync?branch=main
