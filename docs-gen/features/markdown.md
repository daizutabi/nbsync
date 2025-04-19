# Notebooks from Markdown

nbsync allows you to create Jupyter notebooks directly from your markdown files,
enabling a seamless integration of documentation and code execution.

## Basic Syntax

To define a notebook cell within markdown, use the following syntax:

````markdown
```python .md#cell-id
# Your Python code here
import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
```

![Description](){#cell-id}
````

This creates:

1. A Python code cell with the content between the backticks
2. An output cell that displays the result of executing the code
3. A connection between the two using the `#cell-id` identifier

## Tabbed Display

Using the `source="tabbed-nbsync"` attribute, you can create a tabbed interface
that shows both the source code and the execution result:

````markdown source="tabbed-nbsync"
```python .md#plot
import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
plt.title("Simple Plot")
```

![Plot result](){#plot}
````

## Multiple Cells

You can define multiple cells in a single markdown file, each with its own
identifier:

````markdown
```python .md#cell1
import numpy as np
data = np.random.randn(100)
```

```python .md#cell2
import matplotlib.pyplot as plt
plt.hist(data, bins=20)
```

![Histogram](){#cell2}
````

## Execution Context

Cells are executed in sequence, maintaining state between them. Variables
defined in earlier cells are available to later cells, just like in a Jupyter
notebook.

## Markdown Within Cells

You can include markdown cells in your notebook by using:

````markdown
```markdown .md#md1
## Analysis Results

The following visualization shows our findings.
```
````

## Advanced Features

### Setting Figure Size

Control the output size directly in your code:

````markdown
```python .md#custom-size
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot([1, 2, 3, 4], [1, 4, 9, 16])
```

![Sized plot](){#custom-size}
````

### Embedding Variables

Embed variables from your code into your markdown text:

````markdown
```python .md#stats
data = [1, 2, 3, 4, 5]
mean = sum(data) / len(data)
```

The mean of the data is `{mean:.2f}`.
````

### Multiple Outputs

Generate and display multiple outputs from a single cell:

````markdown
```python .md#multi-out
import matplotlib.pyplot as plt
import numpy as np

# First plot
fig1, ax1 = plt.subplots()
ax1.plot(np.random.randn(50).cumsum())
fig1.savefig('plot1.png')

# Second plot
fig2, ax2 = plt.subplots()
ax2.hist(np.random.randn(100), bins=20)
fig2.savefig('plot2.png')
```

First plot:

![Plot 1](){#multi-out:0}

Second plot:

![Plot 2](){#multi-out:1}
````
