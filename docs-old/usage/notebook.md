# Notebook Configuration

This page explains how to configure nbsync to work with
your Jupyter notebooks.

## Setting the Notebook Directory

The first step is to specify where your Jupyter notebooks are
located. This is done using the `src_dir` option in your
`mkdocs.yml` configuration file.

**Example:**

```yaml title="mkdocs.yml"
plugins:
  - nbsync:
      src_dir: ../notebooks
```

The `src_dir` path is relative to your `docs` directory.
For example, with the configuration above and the following
project structure:

```text
project/
├─ docs/
│  └─ index.md
├─ notebooks/    <- src_dir points here
│  ├─ data-analysis.ipynb
│  └─ visualization.ipynb
└─ mkdocs.yml
```

All notebooks in the `notebooks` directory will be available
to reference in your markdown files.
The `src_dir` can contain subdirectories, and all
notebooks in the subdirectories will also be available.

## Referencing Notebooks in Markdown

Once you've configured the notebook directory, you can reference
notebooks using the standard Markdown image syntax with attributes:

```markdown
![Alt text](visualization.ipynb){#figure-identifier}
```

Where:

- `Alt text` is the alternative text for the image
- `visualization.ipynb` is the path to the notebook file,
  relative to the `src_dir` (See the directory tree above)
- `#figure-identifier` is the identifier for the specific
  figure in the notebook

For more information about using class options to control how notebook
content is displayed, see the [Display Control Options](class.md) page.

## Identifying Figures in the Notebook

In your Jupyter notebook, you need to mark which figures you want
to reference in your documentation. This is done using a special
comment format at the beginning of a code cell.

**Example:**

```python title="visualization.ipynb"
# #my-figure
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot([1, 2, 3, 4], [10, 20, 25, 30])
ax.set_title('Sample Visualization')
```

The comment format has the following rules:

- It must be the first non-empty line in the cell
- It starts with a Python comment character (`#`) followed by a space
- Then comes the figure identifier, which also starts with `#`
- Example: `# #my-figure` identifies a figure with the ID `my-figure`

You can then reference this figure in your markdown:

```markdown
![Sample Chart](visualization.ipynb){#my-figure}
```

### Benefits of This Approach

This identifier method is:

- Simple to add and recognize in your notebooks
- Visible during normal notebook editing
- Doesn't require special cell tags or hidden metadata
- Maintains notebook usability for non-documentation purposes

When you look at your notebook, you can immediately identify
cells that will be referenced in the documentation by looking
for the `# #identifier` pattern at the top of the cell.

## Automatic Notebook Selection

When working with multiple figures from the same notebook,
you can simplify your markdown by omitting the notebook filename
in subsequent references. The plugin will automatically use
the most recently specified notebook.

**Example:**

```markdown
![First Chart](visualization.ipynb){#figure-1}

![Second Chart](){#figure-2} <!-- Uses visualization.ipynb -->

Some text between figures...

![Third Chart](analysis.ipynb){#figure-3}

![Fourth Chart](){#figure-4} <!-- Uses analysis.ipynb -->
```

### How It Works

The plugin keeps track of the most recently referenced notebook:

1. When a notebook is explicitly specified, it becomes the "active" notebook
2. Empty parentheses `()` tell the plugin to use the active notebook
3. Any new explicit notebook reference updates the active notebook

### Benefits

This feature significantly reduces maintenance effort:

- **Less repetition** in your markdown files
- **Easier refactoring** - if you rename a notebook, you only need
  to update the first reference, not every occurrence
- **Cleaner documentation source** with fewer duplicate filenames

This approach is particularly useful for pages that reference multiple
figures from the same notebook in sequence.

### Declaring Active Notebooks

You can explicitly declare which notebook to use throughout a document
by using the special identifier `#.`:

```markdown
![](analysis.ipynb){#.}

<!-- Now all empty references will use analysis.ipynb -->

![First chart](){#chart1}
![Second chart](){#chart2}
```

This marker doesn't output any content - it only sets the active
notebook. It's useful to place at the beginning of your document
to clearly indicate which notebook will be used.
