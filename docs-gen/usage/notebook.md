# Working with Notebooks

nbsync provides seamless integration with Jupyter notebooks, allowing you to
reference specific cells or figures from your notebooks directly in your
documentation.

## Preparing Your Notebook

To make cells in your Jupyter notebook referenceable, you need to tag them with
identifiers. There are two ways to do this:

### Method 1: Using Comments

Add a comment with a hash identifier at the beginning of a cell:

```python
# #my-plot
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
plt.title("My Plot")
```

The identifier here is `my-plot`.

### Method 2: Using Cell Metadata

In Jupyter notebook or JupyterLab, you can add metadata to cells:

1. Select the cell you want to tag
2. Open the Property Inspector (side panel)
3. Under "Cell Metadata", add:
   ```json
   {
     "nbsync": {
       "id": "my-plot"
     }
   }
   ```

## Referencing in Documentation

Once you've tagged cells in your notebook, you can reference them in your
Markdown files:

```markdown
![My plot description](path/to/notebook.ipynb){#my-plot}
```

This will include the output of the tagged cell in your documentation.

## Multiple Cell References

You can reference multiple cells from the same notebook:

```markdown
# Analysis Results

## Data Preparation

![Data summary](analysis.ipynb){#data-prep}

## Visualization

![Plot of results](analysis.ipynb){#result-plot}

## Statistical Tests

![Statistical analysis](analysis.ipynb){#statistics}
```

## Automatic Execution

To ensure your notebook is executed before being included in your documentation,
add the `.execute` attribute:

```markdown
![My plot](analysis.ipynb){#my-plot .execute}
```

This is particularly useful for:

- Ensuring results are up-to-date
- Including notebooks that haven't been executed yet
- Running notebooks with different parameters

## Execution Options

Control the execution behavior with additional attributes:

```markdown
![My plot](analysis.ipynb){#my-plot .execute kernel="python3" timeout=60}
```

Available options include:

- `kernel`: Specify which Jupyter kernel to use
- `timeout`: Maximum execution time in seconds
- `allow_errors`: Whether to continue execution after errors (true/false)

## Dynamic Parameters

Pass parameters to your notebook during execution:

```markdown
![Result with parameter](analysis.ipynb){#parametrized-plot param_value=42}
```

In your notebook, access the parameter using:

```python
# #parametrized-plot
import matplotlib.pyplot as plt
from nbsync import get_param

# Get parameter value (with default if not provided)
value = get_param('param_value', default=10)

plt.figure(figsize=(8, 5))
plt.plot(range(value))
plt.title(f"Plot with {value} points")
```

## Multiple Output Formats

Control the output format:

```markdown
![SVG Plot](analysis.ipynb){#my-plot format=svg}
```

Supported formats:

- `png` (default): Raster image
- `svg`: Vector graphics
- `html`: Interactive HTML (for interactive visualizations)

## Best Practices

1. **Organize Notebooks Logically**

   - Group related visualizations in the same notebook
   - Use meaningful cell identifiers

2. **Keep Cells Focused**

   - Each tagged cell should generate a single, clear output
   - Avoid cells with multiple outputs unless intentional

3. **Handle Dependencies**

   - Ensure cells are self-contained or depend only on previous cells
   - Import necessary libraries in each tagged cell to ensure portability

4. **Document Cell Purpose**

   - Add comments explaining what each cell does
   - Document any assumptions or limitations

5. **Consider Performance**
   - Optimize computationally intensive cells
   - Use caching for expensive calculations
