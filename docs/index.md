# nbsync

<div class="grid cards" markdown>

- :material-notebook-edit: **Notebooks from Markdown**
  Extend standard markdown syntax to automatically generate notebooks from
  documentation
  [:octicons-arrow-right-24: Markdown Features](#notebooks-from-markdown)

- :material-language-python: **Python File Integration**
  Directly reference external Python files and reuse functions or classes
  [:octicons-arrow-right-24: Python Integration](#python-file-integration)

- :material-image-edit: **Code Execution in Images**
  Execute code within image notation for dynamic visualizations
  [:octicons-arrow-right-24: Dynamic Visualization](#code-execution-in-images)

- :material-refresh-auto: **Dynamic Updates**
  Real-time synchronization between notebooks and documentation
  [:octicons-arrow-right-24: Dynamic Updates](#dynamic-updates-and-execution)

</div>

## What is nbsync?

nbsync is an innovative plugin that seamlessly connects Jupyter notebooks with
MkDocs documentation. Going beyond traditional notebook integration, it provides
functionality to generate and execute notebooks directly from markdown (.md)
files and Python (.py) files.

It solves common challenges faced by data scientists, researchers, and technical
writers:

- **Development happens in notebooks** - ideal for experimentation and visualization
- **Documentation lives in markdown** - perfect for narrative and explanation
- **Traditional integration is challenging** - screenshots break, exports get outdated

## Key Features

### Notebooks from Markdown

Extend standard markdown syntax to define notebook cells within your
documentation. Present code and its output results concisely with tabbed
display.

````markdown source="tabbed-nbsync"
```python .md#plot source="on"
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(2, 1))
ax.plot([1, 3, 3, 4])
```

![Plot result](){#plot source="on"}
````

### Python File Integration

Directly reference external Python files and reuse defined functions or classes.
Avoid code duplication and improve maintainability.

```python title="plot.py"
--8<-- "scripts/plot.py"
```

```markdown source="tabbed-nbsync"
![Plot result](plot.py){#sqrt source="on"}
```

### Code Execution in Images

Execute Python code directly within image notation and display the results.
This enables easy placement of dynamic visualizations in tables or complex
layouts.

```markdown source="tabbed-nbsync"
|         Sine          |        Cosine         |
| :-------------------: | :-------------------: |
| ![](){`plot(np.sin)`} | ![](){`plot(np.cos)`} |
```

### Dynamic Updates and Execution

Automatic synchronization between notebooks and documentation ensures code
changes are reflected in real-time. View changes instantly in MkDocs serve mode.

## Getting Started

Follow these steps to get started with nbsync:

1. [Installation](getting-started/installation.md)
2. [Configuration](getting-started/configuration.md)
3. [First Steps](getting-started/first-steps.md)

## Examples

Explore the possibilities of nbsync through practical examples:

- [Basic Usage](examples/basic.md)
- [Visualizations in Tables](examples/tables.md)
- [Advanced Examples](examples/advanced.md)
