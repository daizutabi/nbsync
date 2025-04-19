# Notebook Execution

nbsync provides powerful capabilities for executing notebooks during
documentation builds, ensuring your visualizations and results are always
up-to-date.

## Basic Execution

To execute a notebook during the documentation build, add the `.execute`
attribute:

```markdown
![Plot description](notebook.ipynb){#cell-id .execute}
```

This tells nbsync to:

1. Execute the notebook before including it in the documentation
2. Capture the outputs
3. Display the specified cell's output

## Execution Options

Control execution behavior with additional attributes:

```markdown
![Plot description](notebook.ipynb){#cell-id .execute kernel="python3" timeout=60}
```

Available options include:

- `kernel`: Specify which Jupyter kernel to use (e.g., "python3", "ir")
- `timeout`: Maximum execution time in seconds
- `allow_errors`: Whether to continue execution after errors (true/false)
- `env`: Environment variables to set during execution

## Parameterized Execution

Pass parameters to notebooks during execution:

```markdown
![Population growth](population.ipynb){#growth-plot .execute
country="France" start_year=1950 end_year=2020}
```

In your notebook, retrieve these parameters using:

```python
# #growth-plot
from nbsync import get_param

country = get_param('country', 'World')  # Default to 'World' if not specified
start_year = int(get_param('start_year', 1900))
end_year = int(get_param('end_year', 2000))

# Use parameters in your code
data = load_population_data(country, start_year, end_year)
plot_population(data)
```

## Dynamic Parameter Selection

Create interactive parameter selection:

```markdown
Select region:

- [Europe](){.param region="Europe"}
- [Asia](){.param region="Asia"}
- [Africa](){.param region="Africa"}
- [Americas](){.param region="Americas"}

![Regional data](stats.ipynb){#regional-plot .execute region="$region"}
```

The `$region` syntax uses the value selected by the user.

## Execution Context

### Global Configuration

Set default execution options in your `mkdocs.yml`:

```yaml
plugins:
  - nbsync:
      execute:
        enabled: true
        timeout: 300
        kernel: python3
        allow_errors: false
```

### Notebook-Specific Configuration

Override global settings for specific notebooks:

```markdown
<!-- Long-running simulation with custom kernel -->

![Simulation](complex_model.ipynb){#simulation .execute
kernel="python3-gpu" timeout=1800}
```

## Conditional Execution

Execute notebooks only when certain conditions are met:

```markdown
![Weather data](weather.ipynb){#forecast .execute only_if="update_weather"}
```

Control this with environment variables or build flags:

```bash
UPDATE_WEATHER=true mkdocs build
```

## Dependency Management

### Specifying Requirements

For notebooks with special dependencies, specify requirements:

```markdown
![ML model results](deep_learning.ipynb){#results .execute
requirements="tensorflow,keras,scikit-learn"}
```

### Using Virtual Environments

Execute notebooks in specific virtual environments:

```markdown
![Data analysis](analysis.ipynb){#summary .execute venv="data-science-env"}
```

## Error Handling

### Controlling Error Behavior

Decide how to handle execution errors:

```markdown
<!-- Stop on errors (default) -->

![Critical analysis](critical.ipynb){#results .execute allow_errors=false}

<!-- Continue despite errors -->

![Experimental analysis](experimental.ipynb){#results .execute allow_errors=true}
```

### Displaying Error Information

Show error messages in your documentation:

```markdown
![Debugging example](debug.ipynb){#error-demo .execute show_errors=true}
```

## Performance Optimization

### Caching

Enable caching to avoid re-executing unchanged notebooks:

```yaml
plugins:
  - nbsync:
      cache:
        enabled: true
        dir: .cache/nbsync
        timeout: 3600 # Seconds
```

### Selective Execution

Execute only what you need:

```markdown
<!-- Execute only specific cells -->

![Performance comparison](benchmark.ipynb){#benchmarks .execute cells="setup,run_benchmark"}
```

## Best Practices

1. **Balance Build Time and Freshness**

   - Use caching for expensive computations
   - Consider which notebooks truly need execution on each build

2. **Handle Long-Running Notebooks**

   - Set appropriate timeouts
   - Consider pre-executing complex notebooks

3. **Manage Dependencies**

   - Ensure all required packages are available in the execution environment
   - Document special requirements

4. **Error Handling Strategy**

   - Decide whether builds should fail on notebook errors
   - Add appropriate error handling in notebooks

5. **Use Parameterization Effectively**
   - Design notebooks to be parameterizable from the start
   - Provide sensible defaults for all parameters
