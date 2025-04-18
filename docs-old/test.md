# Test

## Notebook from Markdown

````markdown source="tabbed-nbsync"
```python .md#plot
import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
```

![alt](){#plot}
````

### Notebook from Python

```python title="plot.py"
--8<-- "scripts/plot.py"
```

```markdown source="tabbed-nbsync"
![](plot.py){#.}

|    `plot(1)`     |    `plot(2)`     |
| :--------------: | :--------------: |
| ![](){`plot(1)`} | ![](){`plot(2)`} |
```
