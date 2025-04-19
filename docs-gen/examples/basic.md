# Basic Examples

This page demonstrates the fundamental ways to use nbsync in your documentation.

## Referencing a Jupyter Notebook

The simplest usage pattern is to reference a cell from an existing Jupyter
notebook:

```markdown
![Line plot](../notebooks/visualizations.ipynb){#line-plot}
```

**Result**: Displays the output of the cell tagged with `#line-plot` in the
notebook.

## Including Python Files

Reference a Python file and use its functions:

```markdown
![](../scripts/plot.py){#.}

Here's a sine wave:

![](){`plot_sine(1, 0.5)`}
```

**Result**: Includes the `plot.py` file and executes the `plot_sine` function
with arguments `1` and `0.5`.

## Creating a Notebook in Markdown

Define a notebook directly in your markdown:

````markdown source="tabbed-nbsync"
```python .md#data-generation
import numpy as np
import matplotlib.pyplot as plt

# Generate random data
data = np.random.randn(1000)
```

```python .md#visualization
# Create a histogram
plt.figure(figsize=(8, 4))
plt.hist(data, bins=30, alpha=0.7)
plt.title("Histogram of Random Data")
plt.grid(True, alpha=0.3)
```

![Histogram](){#visualization}
````

**Result**: Creates a notebook with two cells and displays the output of the
second cell.

## Dynamic Content in Tables

Organize visualizations in tables for easy comparison:

```markdown
![](../scripts/stats.py){#.}

|      Line Plot       |      Bar Plot       |
| :------------------: | :-----------------: |
| ![](){`plot_line()`} | ![](){`plot_bar()`} |

| Parameters |             Values              |
| :--------: | :-----------------------------: |
|    Mean    |  ![](){`display_stat("mean")`}  |
|   Median   | ![](){`display_stat("median")`} |
|  Std Dev   |  ![](){`display_stat("std")`}   |
```

**Result**: Creates a table with visualizations and statistics.

## Interactive Parameters

Create documentation with interactive parameters:

```markdown
Choose a window size:

- [Small](){.param window=10}
- [Medium](){.param window=50}
- [Large](){.param window=100}

![Moving average](../notebooks/time_series.ipynb){#moving-avg window=$window}
```

**Result**: Allows switching between different window sizes for the moving
average visualization.

## Combining Multiple Sources

Mix different sources in a single document:

````markdown
# Data Analysis

## Raw Data Overview

![Data summary](../notebooks/preprocessing.ipynb){#summary}

## Statistical Tests

![](../scripts/statistics.py){#.}

Significance test results:
![](){`run_ttest(alpha=0.05)`}

## Visualization

```python .md#final-plot
import matplotlib.pyplot as plt
import pandas as pd

# Load processed data
data = pd.read_csv("../data/processed.csv")

plt.figure(figsize=(10, 6))
plt.scatter(data['x'], data['y'], alpha=0.6)
plt.title("Final Results")
plt.xlabel("Variable X")
plt.ylabel("Variable Y")
```
````

![Final visualization](){#final-plot}

````

**Result**: Combines references to a notebook, Python script, and inline code in
one cohesive document.

## Real-Time Updating

Demonstrate how content updates when source files change:

1. Display content from a notebook
2. Update the notebook in another window
3. See changes reflected in documentation (in serve mode)

```markdown
![Real-time updating](../notebooks/live_data.ipynb){#latest .execute}
````

**Result**: Shows the latest results from the notebook, automatically refreshing
when the notebook changes.
