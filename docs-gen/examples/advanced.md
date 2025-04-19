# Advanced Examples

This page showcases advanced usage patterns for nbsync, demonstrating its full
potential for creating sophisticated, interactive documentation.

## Custom Styling with CSS

Apply custom styling to your visualizations:

```markdown
<style>
.custom-viz {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
</style>

<div class="custom-viz" markdown>
![](../scripts/custom_viz.py){#.}

![](){`create_dashboard(theme="light")`}

</div>
```

## Conditional Content

Create visualizations that adapt based on parameters:

```markdown
Select model complexity:

- [Simple](){.param complexity="simple"}
- [Medium](){.param complexity="medium"}
- [Complex](){.param complexity="complex"}

![](../scripts/models.py){#.}

![](){`visualize_model("$complexity")`}

{% if complexity == "complex" %}

### Warning

This model requires significant computational resources.
{% endif %}
```

## Interactive Dashboards

Create interactive dashboards with multiple components:

```markdown source="tabbed-nbsync"
![](../scripts/dashboard.py){#.}

<div class="grid">
<div class="grid-item" markdown>
### Overview
![](){`summary_stats()`}
</div>
<div class="grid-item" markdown>
### Trend Analysis
![](){`trend_plot()`}
</div>
<div class="grid-item" markdown>
### Distribution
![](){`distribution_plot()`}
</div>
<div class="grid-item" markdown>
### Forecast
![](){`forecast_plot(days=30)`}
</div>
</div>
```

## Workflow Integration

Document and visualize entire data science workflows:

````markdown source="tabbed-nbsync"
# Customer Segmentation Workflow

## 1. Data Preprocessing

```python .md#preprocess
import pandas as pd
import numpy as np

# Load data
data = pd.read_csv("../data/customers.csv")

# Clean data
data.dropna(inplace=True)
data['purchase_date'] = pd.to_datetime(data['purchase_date'])

# Feature engineering
data['total_spend'] = data['order_count'] * data['avg_order_value']
data['days_since_last'] = (pd.Timestamp.now() - data['purchase_date']).dt.days

# Normalize features
from sklearn.preprocessing import StandardScaler
features = ['total_spend', 'order_count', 'days_since_last']
data[features] = StandardScaler().fit_transform(data[features])

# Preview
data.head(3)
```
````

![Preprocessed data](){#preprocess}

## 2. Clustering Analysis

```python .md#clustering
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Determine optimal number of clusters
from sklearn.metrics import silhouette_score

scores = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(data[features])
    score = silhouette_score(data[features], labels)
    scores.append(score)

# Plot silhouette scores
plt.figure(figsize=(10, 5))
plt.plot(range(2, 11), scores, marker='o')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Analysis')
plt.grid(True, alpha=0.3)
```

![Silhouette analysis](){#clustering}

## 3. Final Segmentation

```python .md#segments
# Apply optimal clustering
optimal_k = np.argmax(scores) + 2  # +2 because we started at k=2
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
data['segment'] = kmeans.fit_predict(data[features])

# Visualize segments
import seaborn as sns

plt.figure(figsize=(12, 8))
sns.scatterplot(
    x='total_spend',
    y='order_count',
    hue='segment',
    size='days_since_last',
    sizes=(20, 200),
    palette='viridis',
    data=data
)
plt.title('Customer Segments')
plt.xlabel('Total Spend (normalized)')
plt.ylabel('Order Count (normalized)')
plt.legend(title='Segment')
```

![Customer segments](){#segments}

````

## Custom Component Integration

Integrate custom JavaScript components with your visualizations:

```markdown
![](../scripts/interactive.py){#.}

<div class="interactive-component">
  <div id="slider-container">
    <label for="parameter-slider">Parameter Value: <span id="slider-value">5</span></label>
    <input type="range" id="parameter-slider" min="1" max="10" value="5">
  </div>
  <div id="visualization-container">
    <img id="dynamic-image" src="data:image/png;base64,{`get_base64_image(5)`}" />
  </div>
</div>

<script>
document.getElementById('parameter-slider').addEventListener('input', function(e) {
  const value = e.target.value;
  document.getElementById('slider-value').textContent = value;
  // In a real implementation, this would call a backend API to get a new image
  // For demonstration, this just shows the concept
  document.getElementById('dynamic-image').src = `data:image/png;base64,${fetchImage(value)}`;
});

function fetchImage(value) {
  // In a real implementation, this would fetch from a backend
  return '...base64 encoded image...';
}
</script>
````

## Dynamic Documentation Generation

Generate documentation programmatically based on available data:

```markdown
![](../scripts/doc_generator.py){#.}

![](){`generate_model_comparisons()`}
```

With a Python script that dynamically generates markdown:

```python
def generate_model_comparisons():
    """Generate markdown tables comparing all available models."""
    import matplotlib.pyplot as plt
    from io import StringIO
    import base64

    # Get list of models (in a real scenario, this might come from a database)
    models = ['ModelA', 'ModelB', 'ModelC']
    metrics = ['accuracy', 'precision', 'recall', 'f1']

    # Generate markdown
    output = StringIO()
    output.write("# Model Comparison\n\n")

    # Create table header
    output.write("| Model | " + " | ".join(metrics) + " |\n")
    output.write("| :---: | " + " | ".join([":---:"] * len(metrics)) + " |\n")

    # Add rows
    for model in models:
        row = [f"**{model}**"]
        for metric in metrics:
            # In a real scenario, you would get actual values
            value = generate_metric_visualization(model, metric)
            row.append(value)
        output.write("| " + " | ".join(row) + " |\n")

    # Create a figure with the markdown
    fig = plt.figure(figsize=(1, 1))
    fig.text(0.5, 0.5, output.getvalue(), ha='center', va='center')
    plt.axis('off')

    return fig

def generate_metric_visualization(model, metric):
    """Generate a visualization for a specific metric."""
    # In a real scenario, this would create actual visualizations
    return f"![{model} {metric}](){{`plot_{metric}('{model}')`}}"
```
