# Code Execution in Images

nbsync introduces a powerful feature that allows code execution directly within
markdown image syntax, enabling dynamic visualizations embedded anywhere in your
documentation.

## Basic Syntax

The core syntax for executing code within an image is:

```markdown
![](){`code_to_execute()`}
```

This syntax allows you to call Python functions or execute code snippets
directly, with their output displayed as images.

## Embedded in Tables

One of the most powerful applications is placing dynamic visualizations in
tables:

```markdown
| Parameter Value 1 | Parameter Value 2 |
| :---------------: | :---------------: |
| ![](){`plot(1)`}  | ![](){`plot(2)`}  |
| ![](){`hist(1)`}  | ![](){`hist(2)`}  |
```

This creates a grid of visualizations that can be easily compared, perfect for
parameter exploration or comparing different visualization techniques.

## Complete Example

Here's a complete example showing how to use this feature with an external
Python file:

```markdown source="tabbed-nbsync"
![](analysis.py){#.}

### Exploring Learning Rates

|        Learning Rate: 0.01         |        Learning Rate: 0.1         |        Learning Rate: 0.5         |
| :--------------------------------: | :-------------------------------: | :-------------------------------: |
| ![](){`plot_learning_curve(0.01)`} | ![](){`plot_learning_curve(0.1)`} | ![](){`plot_learning_curve(0.5)`} |

### Comparing Optimizers

|         SGD Optimizer          |         Adam Optimizer          |         RMSprop Optimizer          |
| :----------------------------: | :-----------------------------: | :--------------------------------: |
| ![](){`plot_optimizer("sgd")`} | ![](){`plot_optimizer("adam")`} | ![](){`plot_optimizer("rmsprop")`} |
```

## Advanced Features

### Inline Code Execution

Execute code directly inline without an external file:

````markdown
![](){```
import matplotlib.pyplot as plt
import numpy as np
x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x))

```}

```
````

### Combining with Markdown Features

The code execution can be combined with other markdown features:

```markdown
<figure markdown>
  ![](){`plot_results("experiment1")`}
  <figcaption>Results from Experiment 1 showing accuracy over time</figcaption>
</figure>
```

### Code with Arguments

Pass complex arguments to your functions:

```markdown
![](){`visualize_data(dataset="mnist", model="cnn", metrics=["accuracy", "loss"])`}
```

## Technical Details

- Code is executed in the same Python environment as your documentation build
- Output is captured and embedded as images
- Execution context is maintained throughout the document
- Error messages are displayed if code execution fails

## Best Practices

1. **Optimize for Performance** - Keep code execution efficient, especially for
   large documentation sites

2. **Provide Meaningful Context** - Use captions and surrounding text to explain
   visualizations

3. **Handle Errors Gracefully** - Ensure your functions include proper error
   handling

4. **Control Figure Sizes** - Set appropriate figure sizes for your layout

5. **Cache Results When Possible** - For compute-intensive visualizations, use
   caching mechanisms
