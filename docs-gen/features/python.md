# Python File Integration

nbsync allows you to reference and execute code from external Python files,
enabling better code organization and reusability in your documentation.

## Basic Usage

To reference a Python file in your documentation:

```markdown
![Description](path/to/file.py){#.}
```

The `{#.}` identifier marks the current URL context, allowing the Python file to
be executed and its output displayed.

## Function Execution

Execute specific functions from a Python file by calling them directly in the
image syntax:

```markdown
![](){`function_name(arg1, arg2)`}
```

This powerful syntax executes the function with the provided arguments and
displays the result.

## Example Implementation

Let's say you have a Python file called `plots.py` with visualization functions:

```python title="plots.py"
import matplotlib.pyplot as plt
import numpy as np

def plot_sine(frequency=1, amplitude=1):
    """Plot a sine wave with given frequency and amplitude."""
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x)

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(x, y)
    ax.set_title(f"Sine Wave (f={frequency}, A={amplitude})")
    ax.set_ylim(-amplitude*1.2, amplitude*1.2)
    ax.grid(True)

    return fig

def plot_histogram(n_samples=1000, bins=30):
    """Plot a histogram of random data."""
    data = np.random.randn(n_samples)

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.hist(data, bins=bins, alpha=0.7)
    ax.set_title(f"Histogram (n={n_samples}, bins={bins})")
    ax.grid(True, alpha=0.3)

    return fig
```

You can then reference and use these functions in your markdown:

```markdown source="tabbed-nbsync"
![](plots.py){#.}

## Sine Wave Examples

|     Frequency = 1     |     Frequency = 2     |
| :-------------------: | :-------------------: |
| ![](){`plot_sine(1)`} | ![](){`plot_sine(2)`} |

## Histogram Examples

|   1000 Samples, 30 Bins   |       5000 Samples, 50 Bins       |
| :-----------------------: | :-------------------------------: |
| ![](){`plot_histogram()`} | ![](){`plot_histogram(5000, 50)`} |
```

## Advanced Usage

### Accessing Class Methods

You can access methods from classes defined in Python files:

```markdown
![](){`MyClass().method(arg)`}
```

### Chaining Method Calls

Chain multiple method calls for more complex operations:

```markdown
![](){`data.process().visualize(type="bar")`}
```

### Lazy Loading

Python files are only loaded when they're actually referenced, improving
performance for large documentation sites.

## Best Practices

1. **Organize Related Functions** - Group related visualization functions in
   thematic Python files

2. **Parameterize Functions** - Design functions with parameters to enable
   exploration in documentation

3. **Return Figures** - Have your functions return figure objects for proper
   rendering

4. **Document Function Behavior** - Include docstrings to explain function
   parameters and behavior

5. **Keep Context Independent** - Make functions self-contained to avoid
   unexpected behavior
