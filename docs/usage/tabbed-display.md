# Tabbed Display

nbsync provides a tabbed interface feature that allows you to show both source
code and its output results in an elegant, interactive format.

## Basic Usage

To create a tabbed display, wrap your notebook cell definitions with the
`source="tabbed-nbsync"` attribute:

````markdown source="tabbed-nbsync"
```python .md#simple-plot
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
plt.figure(figsize=(8, 5))
plt.plot(x, np.sin(x))
plt.title("Simple Sine Wave")
```

![Sine wave plot](){#simple-plot}
````

This creates a tabbed interface with two tabs:

- **Source**: Shows the Python code
- **Output**: Shows the rendered output

## Multiple Cells in Tabs

You can include multiple cells within a tabbed display:

````markdown source="tabbed-nbsync"
```python .md#data-generation
import numpy as np
import pandas as pd

# Generate sample data
np.random.seed(42)
data = pd.DataFrame({
    'x': np.random.normal(0, 1, 100),
    'y': np.random.normal(0, 1, 100),
    'category': np.random.choice(['A', 'B', 'C'], 100)
})

# Display the first few rows
data.head()
```

![Data preview](){#data-generation}

```python .md#visualization
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x='x', y='y', hue='category')
plt.title('Scatter Plot by Category')
plt.grid(True, alpha=0.3)
```

![Scatter plot](){#visualization}
````

Each code-output pair gets its own set of tabs.

## Custom Tab Labels

Customize the tab labels:

````markdown source="tabbed-nbsync" tabs="{'source': 'Python Code', 'output': 'Visualization'}"
```python .md#custom-tabs
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
plt.figure(figsize=(8, 5))
plt.plot(x, np.sin(x))
plt.title("Custom Tab Labels Example")
```

![Custom tab example](){#custom-tabs}
````

## Including Python Files in Tabs

Reference Python files with tabbed display:

````markdown source="tabbed-nbsync"
![](../scripts/visualization.py){#.}

```markdown
Here's a sine wave with frequency 1:

![](){`plot_sine(1)`}

And here's one with frequency 2:

![](){`plot_sine(2)`}
```
````

This shows the Python file source in one tab and the rendered output in another.

## Integration with External Notebooks

Reference cells from external notebooks with tabbed display:

```markdown source="tabbed-nbsync"
![Notebook visualization](../notebooks/analysis.ipynb){#visualization}
```

## Advanced Customization

### Tab Styling

Apply custom styling to your tabs:

````markdown source="tabbed-nbsync" class="custom-tabs" active="output"
```python .md#styled-tabs
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
plt.figure(figsize=(8, 5))
plt.plot(x, np.sin(x))
plt.title("Styled Tabs Example")
```

![Styled tab example](){#styled-tabs}
````

Add custom CSS to your documentation:

```css
.custom-tabs .tabbed-labels {
  background-color: #f8f9fa;
  border-radius: 4px 4px 0 0;
}

.custom-tabs .tabbed-labels label {
  font-weight: 500;
  padding: 10px 16px;
}

.custom-tabs .tabbed-content {
  border: 1px solid #e1e4e8;
  border-radius: 0 0 4px 4px;
  padding: 16px;
}
```

### Initial Tab Selection

Control which tab is initially active:

````markdown source="tabbed-nbsync" active="output"
```python .md#output-first
import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
plt.title("Output First Example")
```

![Output first example](){#output-first}
````

## Layout Options

### Side-by-Side Display

Create a side-by-side display of code and output:

````markdown source="tabbed-nbsync" layout="side-by-side"
```python .md#side-by-side
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
plt.figure(figsize=(6, 4))
plt.plot(x, np.sin(x))
plt.title("Side-by-Side Example")
```

![Side-by-side example](){#side-by-side}
````

### Full-Width Display

Create a full-width display for complex visualizations:

````markdown source="tabbed-nbsync" layout="full-width"
```python .md#dashboard
import matplotlib.pyplot as plt
import numpy as np

# Create a complex dashboard
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Plot 1: Line plot
x = np.linspace(0, 10, 100)
axes[0, 0].plot(x, np.sin(x))
axes[0, 0].set_title("Sine Wave")

# Plot 2: Bar chart
axes[0, 1].bar(['A', 'B', 'C', 'D'], [3, 7, 9, 4])
axes[0, 1].set_title("Bar Chart")

# Plot 3: Scatter plot
axes[1, 0].scatter(np.random.rand(50), np.random.rand(50))
axes[1, 0].set_title("Scatter Plot")

# Plot 4: Histogram
axes[1, 1].hist(np.random.normal(0, 1, 1000), bins=30)
axes[1, 1].set_title("Histogram")

plt.tight_layout()
```

![Dashboard example](){#dashboard}
````

## Best Practices

1. **Consistent Presentation**

   - Use the same tabbed display style throughout your documentation
   - Maintain consistent tab ordering (source, then output)

2. **Appropriate Code Size**

   - Keep code cells reasonably sized for readability
   - Split complex code into multiple tabbed sections

3. **Visualization Sizing**

   - Set appropriate figure sizes for your layout
   - Consider how visualizations will appear in tabs

4. **Narrative Context**

   - Provide explanatory text before or after tabbed sections
   - Don't rely solely on code comments for explanation

5. **Progressive Disclosure**
   - Use tabs to hide complexity initially
   - Show output by default for results-focused sections
