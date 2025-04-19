# Working with Python Files

nbsync allows you to directly reference and execute functions from Python files,
providing a powerful way to organize your code and create dynamic documentation.

## Basic Usage

Reference a Python file in your documentation:

```markdown
![](path/to/file.py){#.}
```

The `{#.}` identifier is a special marker that indicates the current URL
context, making the Python file's functions available for execution.

## Writing Python Files for Documentation

When creating Python files for use with nbsync, follow these guidelines:

1. **Define functions that return visualizations**:

```python
# plots.py
import matplotlib.pyplot as plt
import numpy as np

def plot_sine(frequency=1, amplitude=1):
    """Plot a sine wave with given frequency and amplitude."""
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x)

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(x, y)
    ax.set_title(f"Sine Wave (f={frequency}, A={amplitude})")

    return fig  # Return the figure object
```

2. **Ensure functions return appropriate objects**:

   - For visualizations: Return Matplotlib figure objects
   - For data: Return pandas DataFrames, numpy arrays, or similar

3. **Document function parameters**:
   - Use docstrings to explain what each function does
   - Document parameter meanings and default values

## Function Execution

Execute specific functions from the referenced Python file:

```markdown
![](){`function_name(arg1, arg2)`}
```

This syntax calls the function with the provided arguments and displays the
result.

## Complete Example

Here's a complete example of using a Python file in your documentation:

```markdown
# Data Visualization

First, let's reference our plotting library:

![](../scripts/plots.py){#.}

## Sine Wave Examples

Here's a basic sine wave:

![](){`plot_sine(1, 1)`}

We can adjust the frequency:

![](){`plot_sine(2, 1)`}

Or the amplitude:

![](){`plot_sine(1, 2)`}

## Comparing Parameters

We can organize these in a table for comparison:

|       Frequency = 1        |       Frequency = 2        |       Frequency = 3        |
| :------------------------: | :------------------------: | :------------------------: |
|  ![](){`plot_sine(1, 1)`}  |  ![](){`plot_sine(2, 1)`}  |  ![](){`plot_sine(3, 1)`}  |
| ![](){`plot_sine(1, 0.5)`} | ![](){`plot_sine(2, 0.5)`} | ![](){`plot_sine(3, 0.5)`} |
```

## Advanced Techniques

### Working with Classes

You can use classes defined in your Python files:

```python
# analysis.py
class DataAnalyzer:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)

    def plot_distribution(self, column):
        fig, ax = plt.subplots(figsize=(8, 4))
        self.data[column].hist(ax=ax)
        ax.set_title(f"Distribution of {column}")
        return fig
```

Reference in markdown:

```markdown
![](../scripts/analysis.py){#.}

![](){`DataAnalyzer("../data/sales.csv").plot_distribution("revenue")`}
```

### Chaining Method Calls

Chain multiple method calls for more complex operations:

```markdown
![](){`load_data().preprocess().visualize("bar")`}
```

### Passing Complex Arguments

Pass complex arguments to your functions:

```markdown
![](){`create_chart(x_axis="date", metrics=["revenue", "profit"],
aggregate="monthly")`}
```

### Conditional Execution

Use conditional logic in your function calls:

```markdown
![](){`plot_data(dataset="sales",
filter_outliers=True if dataset_size > 1000 else False)`}
```

## Best Practices

1. **Organize Related Functions**

   - Group related functions in thematic Python files
   - Create logical separation between different types of functionality

2. **Handle Dependencies**

   - Ensure all necessary imports are within each function
   - Consider using dependency injection for shared resources

3. **Error Handling**

   - Implement robust error handling in your functions
   - Provide clear error messages that help identify issues

4. **Documentation**

   - Add docstrings to all functions
   - Include examples of function usage in comments

5. **Testing**
   - Test your Python files independently before using them in documentation
   - Consider adding a `if __name__ == "__main__"` block with example usage
