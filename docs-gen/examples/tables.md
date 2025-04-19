# Visualizations in Tables

One of nbsync's most powerful features is the ability to organize visualizations
in tables. This creates clean, comparative layouts that help readers understand
relationships between different parameters or methods.

## Basic Table Layout

Create a simple comparison table:

```markdown source="tabbed-nbsync"
![](../scripts/plot.py){#.}

|         Sine Wave         |        Cosine Wave        |
| :-----------------------: | :-----------------------: |
| ![](){`plot_trig("sin")`} | ![](){`plot_trig("cos")`} |
```

## Parameter Exploration Grid

Compare multiple parameter combinations:

```markdown source="tabbed-nbsync"
![](../scripts/models.py){#.}

### Learning Rate Comparison

|               |             **Batch Size: 32**             |             **Batch Size: 64**             |             **Batch Size: 128**             |
| :-----------: | :----------------------------------------: | :----------------------------------------: | :-----------------------------------------: |
| **LR: 0.001** | ![](){`plot_training(lr=0.001, batch=32)`} | ![](){`plot_training(lr=0.001, batch=64)`} | ![](){`plot_training(lr=0.001, batch=128)`} |
| **LR: 0.01**  | ![](){`plot_training(lr=0.01, batch=32)`}  | ![](){`plot_training(lr=0.01, batch=64)`}  | ![](){`plot_training(lr=0.01, batch=128)`}  |
|  **LR: 0.1**  |  ![](){`plot_training(lr=0.1, batch=32)`}  |  ![](){`plot_training(lr=0.1, batch=64)`}  |  ![](){`plot_training(lr=0.1, batch=128)`}  |
```

## Method Comparison

Compare different algorithms or methods:

```markdown source="tabbed-nbsync"
![](../scripts/clustering.py){#.}

### Clustering Algorithm Comparison

| Dataset |                  K-Means                   |                   DBSCAN                   |                   Hierarchical                   |
| :-----: | :----------------------------------------: | :----------------------------------------: | :----------------------------------------------: |
|  Blobs  |  ![](){`cluster_plot("blobs", "kmeans")`}  |  ![](){`cluster_plot("blobs", "dbscan")`}  |  ![](){`cluster_plot("blobs", "hierarchical")`}  |
|  Moons  |  ![](){`cluster_plot("moons", "kmeans")`}  |  ![](){`cluster_plot("moons", "dbscan")`}  |  ![](){`cluster_plot("moons", "hierarchical")`}  |
| Circles | ![](){`cluster_plot("circles", "kmeans")`} | ![](){`cluster_plot("circles", "dbscan")`} | ![](){`cluster_plot("circles", "hierarchical")`} |
```

## Time Series Visualization

Compare time series with different window sizes:

```markdown source="tabbed-nbsync"
![](../scripts/time_series.py){#.}

### Moving Average Window Size Comparison

|                Raw Data                |             Window = 7              |             Window = 30              |             Window = 90              |
| :------------------------------------: | :---------------------------------: | :----------------------------------: | :----------------------------------: |
| ![](){`plot_time_series(window=None)`} | ![](){`plot_time_series(window=7)`} | ![](){`plot_time_series(window=30)`} | ![](){`plot_time_series(window=90)`} |
```

## Dataset Comparison

Compare visualizations across different datasets:

```markdown source="tabbed-nbsync"
![](../scripts/datasets.py){#.}

### Distribution Comparison

|               |            Histogram            |            Box Plot            |            Violin Plot            |
| :-----------: | :-----------------------------: | :----------------------------: | :-------------------------------: |
| **Dataset A** | ![](){`plot_dist("A", "hist")`} | ![](){`plot_dist("A", "box")`} | ![](){`plot_dist("A", "violin")`} |
| **Dataset B** | ![](){`plot_dist("B", "hist")`} | ![](){`plot_dist("B", "box")`} | ![](){`plot_dist("B", "violin")`} |
| **Dataset C** | ![](){`plot_dist("C", "hist")`} | ![](){`plot_dist("C", "box")`} | ![](){`plot_dist("C", "violin")`} |
```

## Tables with Text and Metrics

Mix visualizations with text and metrics:

```markdown source="tabbed-nbsync"
![](../scripts/evaluation.py){#.}

### Model Evaluation

|    Model    |       Loss Curve        |                                       Metrics                                        |
| :---------: | :---------------------: | :----------------------------------------------------------------------------------: |
| **Model A** | ![](){`plot_loss("A")`} | Accuracy: ![](){`get_metric("A", "accuracy")`}<br>F1: ![](){`get_metric("A", "f1")`} |
| **Model B** | ![](){`plot_loss("B")`} | Accuracy: ![](){`get_metric("B", "accuracy")`}<br>F1: ![](){`get_metric("B", "f1")`} |
```

## Interactive Tables

Create tables with interactive elements:

```markdown
Select dataset:

- [Iris](){.param dataset="iris"}
- [Wine](){.param dataset="wine"}
- [Digits](){.param dataset="digits"}

![](../scripts/interactive.py){#.}

|                         PCA                          |                         t-SNE                         |                         UMAP                          |
| :--------------------------------------------------: | :---------------------------------------------------: | :---------------------------------------------------: |
| ![](){`dimensionality_reduction("$dataset", "pca")`} | ![](){`dimensionality_reduction("$dataset", "tsne")`} | ![](){`dimensionality_reduction("$dataset", "umap")`} |
```

## Best Practices for Tables

1. **Consistent Sizing**: Use the same figure size for all plots in a table

   ```python
   def my_plot(param):
       fig, ax = plt.subplots(figsize=(4, 3))  # Consistent size
       # ...
       return fig
   ```

2. **Row and Column Headers**: Use bold text for headers to improve readability

   ```markdown
   | **Feature** | **Distribution** | **Correlation** |
   ```

3. **Alignment**: Center-align cells for balanced appearance

   ```markdown
   | :--------: | :------------: | :-------------: |
   ```

4. **Limited Complexity**: Avoid tables that are too large or complex

   - Keep tables to 3-4 columns maximum
   - Split large comparisons into multiple tables

5. **Context**: Add captions or descriptions to explain the significance of the
   comparisons
