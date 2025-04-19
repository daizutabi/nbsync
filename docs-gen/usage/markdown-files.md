# Creating Notebooks from Markdown

nbsync allows you to create and execute Jupyter notebooks directly from your
markdown documentation files, combining narrative and code in a single source.

## Basic Structure

To define a notebook within markdown, use code blocks with special identifiers:

````markdown
```python .md#cell-id
# Your Python code here
import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
```

![Output description](){#cell-id}
````

This creates:

1. A Python code cell with the content between the backticks
2. An output cell that displays the result of executing the code
3. A connection between them using the `#cell-id` identifier

## Multiple Cells

You can define multiple cells in a single markdown file:

````markdown
```python .md#setup
import numpy as np
import matplotlib.pyplot as plt
data = np.random.randn(1000)
```

```python .md#histogram
plt.figure(figsize=(10, 6))
plt.hist(data, bins=30, alpha=0.7)
plt.title("Histogram of Random Data")
```

![Histogram visualization](){#histogram}
````

Cells are executed in sequence, maintaining state between them just like in a
Jupyter notebook.

## Tabbed Display

Using the `source="tabbed-nbsync"` attribute, you can create a tabbed interface
that shows both the source code and the execution result:

````markdown source="tabbed-nbsync"
```python .md#plot
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
plt.figure(figsize=(8, 5))
plt.plot(x, np.sin(x))
plt.title("Simple Sine Wave")
```

![Sine wave plot](){#plot}
````

This creates a tabbed interface with "Source" and "Output" tabs.

## Including Markdown Cells

You can include markdown cells in your notebook:

````markdown
```markdown .md#intro
# Analysis Results

This notebook explores the dataset and presents key findings.

## Dataset Overview
```

```python .md#data-overview
import pandas as pd
df = pd.read_csv("data.csv")
df.head(3)
```

![Data overview](){#data-overview}
````

## Advanced Usage

### Multiple Outputs

Generate and display multiple outputs from a single cell:

````markdown
```python .md#multiple-plots
import matplotlib.pyplot as plt
import numpy as np

# First plot
fig1, ax1 = plt.subplots()
ax1.plot(np.random.randn(50).cumsum())
plt.title("Random Walk")
plt.close()  # Close but don't display yet

# Second plot
fig2, ax2 = plt.subplots()
ax2.hist(np.random.randn(1000), bins=30)
plt.title("Histogram")
plt.close()  # Close but don't display yet

# Return both figures
fig1, fig2
```

First plot:
![Random walk](){#multiple-plots:0}

Second plot:
![Histogram](){#multiple-plots:1}
````

### Variable Interpolation

Embed variables computed in your notebook cells into your markdown text:

````markdown
```python .md#stats
import numpy as np
data = np.random.randn(1000)
mean = np.mean(data)
std = np.std(data)
```

The dataset has a mean of `{mean:.2f}` and a standard deviation of `{std:.2f}`.
````

### Code with Errors

Handle code cells that might produce errors:

````markdown
```python .md#error-example
# This will raise an error
1 / 0
```

![Error output](){#error-example .allow-errors}
````

The `.allow-errors` attribute prevents the build from failing when errors occur.

## Integration with Python Files

You can use external Python files in your markdown-based notebooks:

````markdown
```python .md#setup
from my_module import DataProcessor
processor = DataProcessor("data.csv")
```

```python .md#visualization
processor.plot_distribution("age")
```

![Age distribution](){#visualization}
````

## Best Practices

1. **Organize Cells Logically**

   - Group related code together
   - Follow a natural progression from data loading to analysis to visualization

2. **Use Meaningful Identifiers**

   - Choose clear, descriptive IDs for your cells
   - Follow a consistent naming convention

3. **Document Your Code**

   - Include comments in code cells
   - Use markdown cells to explain complex analyses

4. **Balance Code and Narrative**

   - Intersperse code cells with explanatory text
   - Focus on telling a story with your data

5. **Optimize Performance**
   - Keep computationally intensive operations to a minimum
   - Consider caching results of expensive operations

## Limitations

- Interactive widgets are not fully supported in markdown-based notebooks
- Very complex notebooks might be better maintained as separate .ipynb files
- Some advanced Jupyter features may not be available
