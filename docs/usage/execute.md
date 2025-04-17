# Execute Option

The `exec` attribute allows you to dynamically execute
notebooks when building your documentation. This powerful feature
ensures your documentation always displays the most up-to-date
results without requiring manual notebook execution.

## Basic Usage

To execute a notebook when referenced in your documentation,
simply add the `exec` attribute:

```markdown
![Cell output](notebook.ipynb){#data-visualization exec="1"}
```

This will execute the entire notebook before extracting and
displaying the specified cell's output.

## Requirements

To use the `exec` attribute, you need to have nbconvert
installed:

```bash
pip install nbconvert
```

## Key Benefits

### 1. Automated Workflow

The `exec` attribute streamlines your documentation workflow:

- **No manual execution required** - notebooks are automatically
  executed during documentation build
- **Apply once, execute completely** - adding `exec` to one
  reference executes the entire notebook
- **State preservation** - executed notebook states are preserved
  during development server sessions

### 2. Smart Execution Management

nbsync intelligently manages notebook execution:

- **Execution caching** - notebooks are only re-executed when
  necessary
- **Change detection** - automatically re-executes when notebook
  content changes
- **No duplication needed** - apply `exec` to just one cell
  reference per notebook

### 3. Documentation Consistency

Using `exec` ensures documentation consistency:

- **Fresh results** - visualizations and outputs always reflect
  the current code
- **No stale outputs** - eliminates inconsistencies from partial
  manual executions
- **Clean notebook states** - entire notebooks are executed,
  preventing internal state conflicts

## Usage Patterns

### Single Execution Point

You only need to add `exec` to one cell reference per
notebook, typically the first one:

```markdown
![First visualization](analysis.ipynb){#first-chart exec="1"}

More explanation here...

![Second visualization](analysis.ipynb){#second-chart}
```

### Combining with Other Options

The `exec` attribute can be combined with other display options:

```markdown
![Execute and show full cell](notebook.ipynb){#setup exec="1" source="1"}
![Execute and show only source](notebook.ipynb){#helper-function exec="1" source="only"}
```

## Behavior Notes

- Executed notebooks are **not saved back** to disk - your
  original notebooks remain unchanged
- Once executed in a serve session, notebooks won't be re-executed
  when markdown files change
- Notebooks will automatically re-execute when their content
  changes
- The entire notebook is always executed, ensuring all cells have
  consistent state

This execution model provides a perfect balance between
performance and up-to-date documentation.
