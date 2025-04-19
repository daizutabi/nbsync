# First Steps

Let's walk through a quick example of using nbsync to integrate notebooks with
your MkDocs documentation.

## Setting Up Your Project

Start with a typical MkDocs project structure:

```
my-project/
├── docs/
│   ├── index.md
│   └── ...
├── notebooks/
│   ├── analysis.ipynb
│   └── ...
├── scripts/
│   ├── plotting.py
│   └── ...
└── mkdocs.yml
```

## Configure MkDocs

Update your `mkdocs.yml` to include nbsync:

```yaml
site_name: My Documentation
theme:
  name: material

plugins:
  - search
  - nbsync:
      src_dir:
        - ../notebooks
        - ../scripts
```

## Creating Your First Integration

### 1. Prepare a Jupyter Notebook

Create or use an existing notebook with visualizations. Tag cells you want to
reference with a comment:

```python
# In your notebook
# #simple-plot
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
plt.figure(figsize=(8, 4))
plt.plot(x, np.sin(x))
plt.title("Simple Sine Wave")
```

### 2. Reference in Your Documentation

In one of your markdown files (e.g., `docs/index.md`), add:

```markdown
# My Project Documentation

Here's a visualization from our analysis:

![Sine wave plot](../notebooks/analysis.ipynb){#simple-plot}
```

### 3. Create a Python Script

Create a file `scripts/plotting.py` with visualization functions:

```python
# scripts/plotting.py
import matplotlib.pyplot as plt
import numpy as np

def plot_sine(frequency=1):
    """Plot a sine wave with given frequency."""
    x = np.linspace(0, 10, 100)
    plt.figure(figsize=(6, 3))
    plt.plot(x, np.sin(frequency * x))
    plt.title(f"Sine Wave (f={frequency})")
    plt.ylim(-1.2, 1.2)

def plot_histogram(bins=20):
    """Plot a histogram of random data."""
    data = np.random.randn(1000)
    plt.figure(figsize=(6, 3))
    plt.hist(data, bins=bins)
    plt.title(f"Histogram (bins={bins})")
```

### 4. Use Functions in Your Documentation

Create a new file `docs/examples.md`:

```markdown
# Examples

Let's demonstrate different plots:

![](../scripts/plotting.py){#.}

## Sine Waves

|     Frequency = 1     |     Frequency = 2     |
| :-------------------: | :-------------------: |
| ![](){`plot_sine(1)`} | ![](){`plot_sine(2)`} |

## Histogram Examples

|           20 Bins           |           50 Bins           |
| :-------------------------: | :-------------------------: |
| ![](){`plot_histogram(20)`} | ![](){`plot_histogram(50)`} |
```

### 5. Create a Markdown-Based Notebook

Create a file `docs/custom.md`:

````markdown
# Custom Analysis

Here's an analysis created directly in markdown:

````markdown source="tabbed-nbsync"
```python .md#data
import numpy as np
import pandas as pd

# Generate sample data
data = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'group': np.random.choice(['A', 'B', 'C'], 100)
})
```
````
````

```python .md#scatter
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8, 6))
sns.scatterplot(data=data, x='x', y='y', hue='group')
plt.title('Scatter Plot by Group')
```

![Scatter plot](){#scatter}

```

```

## 6. Run Your Documentation

Start the MkDocs development server:

```bash
mkdocs serve
```

Navigate to http://localhost:8000 to see your documentation with the integrated
visualizations.

## Next Steps

Now that you have the basics working, you can:

1. [Explore advanced notebook features](../usage/notebook.md)
2. [Learn about Python file integration](../usage/python-files.md)
3. [Discover markdown-based notebooks](../usage/markdown-files.md)
4. [See real-world examples](../examples/basic.md)

## Troubleshooting

### Common Issues

1. **Images Not Showing**:

   - Check paths in your configuration
   - Ensure notebooks have correctly tagged cells
   - Verify Python dependencies are installed

2. **Execution Errors**:

   - Check the console output for error messages
   - Ensure your environment has all required packages
   - Increase timeout if operations are complex

3. **Changes Not Reflecting**:
   - Hard refresh your browser
   - Restart the MkDocs server
   - Check file paths and identifiers
