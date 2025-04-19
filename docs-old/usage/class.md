# Display Control Options

nbsync provides several class options that
allow you to control how Jupyter notebook content is
displayed in your documentation. These options can be
specified using standard Markdown attribute syntax.

## Default Behavior (No Class Options)

When no class options are specified, nbsync
displays only the figure output from the referenced
Jupyter notebook cell.

**Example:**

```markdown
![alt text](class.ipynb){#image}
```

This produces the following output:

![alt](class.ipynb){#image}

This default behavior is ideal for when you only want
to show visualizations without the accompanying code.

### Automatic Fallback to Source Code

If the referenced cell has no output (for example, if the cell
hasn't been executed or doesn't produce a visual output),
the plugin will automatically display the cell's source code instead.

This fallback mechanism ensures that:

- Your documentation is never left with "missing" content
- Readers can still understand what code should produce an output
- You can identify cells that need to be executed in your notebooks

**Example of fallback behavior:**

```markdown
![alt text](){#func}
```

This produces the following output (since the referenced cell has no visual output):

![alt](){#func}

### Designed for Non-Visual Code

This automatic fallback is especially useful for cells that
intentionally don't produce visual output, such as:

- Function definitions
- Class declarations
- Data preparation code
- Configuration settings

This design makes the workflow more intuitive - the plugin automatically shows the
source code for cells without visual output, making your documentation process
simpler and more efficient. No additional configuration is needed for these
common scenarios.

This automatic fallback makes your documentation more robust and
helps identify when notebook cells need to be executed to generate
expected visualizations.

## Source Code Only

The `source="only"` option instructs nbsync to
display only the source code of the cell, without
its output.

**Example:**

```markdown
![alt text](){#image source="only"}
```

This produces the following output:

![alt](){#image source="only"}

This option is useful when:

- You want to explain the code that generates a visualization
- The code itself is the primary focus
- You're creating tutorials where readers should focus on implementation

## Complete Cell

The `source="1"` option displays both the source code and
the output of the cell, similar to how it appears in
Jupyter notebooks.

**Example:**

```markdown
![alt text](){#image source="1"}
```

This produces the following output:

![alt](){#image source="1"}

This option provides a comprehensive view and is ideal for:

- Educational content where both code and result are important
- Detailed explanations of data processing and visualization techniques
- Demonstrating how code changes affect output

## Combining Options

You can combine them with other standard Markdown attributes:

**Example:**

```markdown
![alt](){#image source="only" title="My title" hl_lines="3 4"}
```

This produces the following output:

![alt](){#image source="only" title="My title" hl_lines="3 4"}

Here, we use two additional attributes:

- `title="My title"` to add a title to the image
- `hl_lines="3 4"` to highlight lines 3 and 4 in the source code

For more information on how to use the `title` and `hl_lines` attributes,
see the [Adding a title][title] and [Highlighting specific lines][hl_lines]
from the MkDocs Material documentation.

[title]: https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#adding-a-title
[hl_lines]: https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#highlighting-specific-lines

## Best Practices

- Use the default (no options) when you want a clean document focused on results
- Use `source="only"` for code-focused explanations or tutorials
- Use `source="1"` for comprehensive educational material
- Be consistent with your choice of options throughout your documentation

These class options give you flexibility in how you
present Jupyter notebook content while maintaining a
clean, readable document structure.
