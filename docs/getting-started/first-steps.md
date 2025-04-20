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

Create or use an existing notebook with visualizations.
Tag cells you want to reference with a comment:

![](analysis.ipynb){#simple-plot source="only" identifier="1" title="notebooks/analysis.ipynb"}

### 2. Reference in Your Documentation

In one of your markdown files (e.g., `docs/index.md`), add:

```markdown
# My Project Documentation

Here's a visualization from our analysis:

![Sine wave plot](analysis.ipynb){#simple-plot}
```

![Sine wave plot](analysis.ipynb){#simple-plot}

### 3. Create a Python Script

Create a file `scripts/plotting.py` with visualization functions:

```python title="scripts/plotting.py"
--8<-- "scripts/plotting.py"
```

### 4. Use Functions in Your Documentation

Create a new file `docs/examples.md`:

```markdown
# Examples

Let's demonstrate different plots:

![](plotting.py){#.}

## Sine Waves

|     Frequency = 1     |     Frequency = 2     |
| :-------------------: | :-------------------: |
| ![](){`plot_sine(1)`} | ![](){`plot_sine(2)`} |

## Histogram Examples

|           20 Bins           |           50 Bins           |
| :-------------------------: | :-------------------------: |
| ![](){`plot_histogram(20)`} | ![](){`plot_histogram(50)`} |
```

![](plotting.py){#.}

|     Frequency = 1     |     Frequency = 2     |
| :-------------------: | :-------------------: |
| ![](){`plot_sine(1)`} | ![](){`plot_sine(2)`} |

|           20 Bins           |           50 Bins           |
| :-------------------------: | :-------------------------: |
| ![](){`plot_histogram(20)`} | ![](){`plot_histogram(50)`} |

### 5. Create a Markdown-Based Notebook

Create a file `docs/custom.md`:

````markdown
# Custom Analysis

Here's an analysis created directly in markdown:

```python .md#_
import numpy as np
import pandas as pd

# Generate sample data
data = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'group': np.random.choice(['A', 'B', 'C'], 100)
})
```

```python .md#scatter
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(3, 2))
sns.scatterplot(data=data, x='x', y='y', hue='group')
plt.title('Scatter Plot by Group')
```

![Scatter plot](.md){#scatter}
````

```python .md#_
import numpy as np
import pandas as pd

# Generate sample data
data = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'group': np.random.choice(['A', 'B', 'C'], 100)
})
```

```python .md#scatter
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(3, 2))
sns.scatterplot(data=data, x='x', y='y', hue='group')
plt.title('Scatter Plot by Group')
```

![Scatter plot](){#scatter}

### 7. Run Your Documentation

Start the MkDocs development server:

```bash
mkdocs serve --open
```

## Troubleshooting

### Common Issues

1. **Images Not Showing**:
    - Check paths in your configuration
    - Ensure notebooks have correctly tagged cells
    - Verify Python dependencies are installed

2. **Execution Errors**:
    - Check the console output for error messages
    - Ensure your environment has all required packages

3. **Changes Not Reflecting**:
    - Hard refresh your browser
    - Restart the MkDocs server
    - Check file paths and identifiers
