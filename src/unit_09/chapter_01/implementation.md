## Implementation

### Languages

To write the **OGD** documentation, we use a combination of **reStructuredText** (**ReST**), **Markdown**, and a small handful of other special-use formats.
**ReST** is the default format for writing documentation used by the **Sphinx** build system.
Other formats, including **Markdown**, are supported via **Sphinx** extensions (e.g. the `myst_parser` extension).

**ReST** has a steep learning curve but offers significant features for controlling the structure of a document, as its name suggests.
**Markdown** is a markup language that is simple, easy to understand, and fast to write.
Thus, use **Markdown** to write most major sections of documents, and use **ReST** to assemble the individual **Markdown** docs into well-structured pages.

#### Markdown

We use **Markdown** as the primary way to write documentation of the OpenGameData system.
As mentioned above, **Sphinx** prefers **reStructuredText**, so we utilize the `myst-parser` extension to render **Markdown** documents.
This extension actually uses an implementation of **Markedly Structured Text**, or **MyST**.
**MyST** is built on the **CommonMark** specification, which is a particular dialect of **Markdown**, but adds some functionality of its own.

In general, we strive to only use the features of **Markdown** that are common across most or all **Markdown** dialects.
Any cases requiring advanced functionality should just be written in **ReST**.
The main exception to this rule is the use of $\LaTeX$-style math parsing, which is covered in the "Special Cases" section below.
That said, it may be helpful to be aware of non-standard things done by the parser we use.
For nitty-gritty details, see the latest version of the
[CommonMark specification](https://spec.commonmark.org/current/),
as well as **MyST**'s
[further extensions](https://myst-parser.readthedocs.io/en/latest/syntax/typography.html)
of **CommonMark**.

##### Markdown Primer

The [Markdown Guide](https://www.markdownguide.org/) website is a good reference on the (relatively simple) syntax of **Markdown**, including documentation of several popular extensions to the core **Markdown** language.
In addition, the Markdown Guide has a nice
[quick reference](https://www.markdownguide.org/cheat-sheet/)
on the most common syntax across **Markdown** and **Markdown**-like dialects.

Below, we include our own quick reference, adapted from the quick reference linked above, for the elements we most commonly use. The "Our Use" column indicates our conventions for when/how to use the various bits of syntax to create a visual language within the documentation. Most uses are obvious, but some are scoped to specific uses:

| Markdown                    | Syntax                             | Our Use                        |
| ---                         | ---                                | ---                            |
| Heading                     | \# H1                              | Doc Headers                    |
|                             | \#\# H2                            | Section Headers                |
|                             | \#\#\# H3                          | Subsection Headers             |
|                             | etc...                             | etc...                         |
| **Bold**                    | \*\*Bold\*\*                       | System/Tool Names              |
| *Italic*                    | \*Italic\*                         | Keywords                       |
| Quote                       | \> Quote                           | Keyword Definitions            |
| `code`                      | \`code\`                           | Variable/Class/Library Names   |
| ```code block```            | \`\`\`code block\`\`\`             | Example Code                   |
| [Link](./implementation.md) | \[Link\]\(Target URL\)             | Links to Other Pages           |
| Unordered List              | \- Item 1                          | Lists of Items                 |
|                             | \- Item 2                          |                                |
|                             | \- ...                             |                                |
| Table                       | \| Column 1 \| Column 2 \| ... \|  | Tables of information          |
|                             | \| ---      \| ---      \| ... \|  |                                |
|                             | \| Value 1  \| Value 2  \| ... \|  |                                |

#### reStructuredText

##### ReST Primer

#### Special Cases

As mentioned, we have a few special cases that use special formats outside of **ReST** and **Markdown**:

- **$\LaTeX$ formatting**: The `myst-parser` extension supports further extensions of its own, described on `myst-parser`'s own [readthedocs site](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html).
  We use `dollarmath` and `amsmath` to support inline use of $\LaTeX$-style implementation of mathematics content
  ([myst-parser page](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#math-shortcuts)).

- **Code-level documentation**: We use the `autodoc` extension of **Sphinx**, which turns module and function comment blocks into readable API reference
  ([sphinx-doc page](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#module-sphinx.ext.autodoc)).

- **Graphs and Visualizations**: We use **Graphviz**, a graph definition language enabled by the `graphviz` extension
  ([sphinx-doc page](https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html)).
  Note that documents using **Graphviz** heavily must be implemented in **ReST**, as **Markdown** does not have a means for rendering in-line **Graphviz** graphics.

### Documentation Organization

Now that we've covered the languages used to write the documentation, we can discuss the organization of the documentation implementation.
From a high-level point of view, the documentation is made up of several *Units* (listed in the [overview](../../00_intro/welcome.md)).
Each unit is, in turn, made up of several *Chapters*.

#### Units

The documentation source contains one folder for each unit, containing the section chapters, as well as a unit index.
The unit index is always named `index.rst` and lists each chapter, acting as a table of contents for the unit.
There is a [unit index template](../../util/templates/unit_index.rst) available.

The unit folder should also include a markdown file named `_<unit_name>.md`, which contains a brief overview of the unit contents.
This will be the first item included in the `index.rst` and serves a dual purpose:

1. Provides a uniform style of introduction to each unit.
2. Acts as an easily-identifiable "name" for the unit within the source directory, allowing us to leave unit names numeric, which should reduce the number of truly broken links whenever we add, rename, merge, or otherwise reorganize units.

There is a [unit overview template](../../util/templates/unit_name.rst) available.

#### Chapters

Chapters are implemented with a similar structure to units. However, since they contain true content, they are made up of an `index.rst` document merging multiple **Markdown** shards.

The pieces making up the chapter will be placed in a subfolder, with a numeric name like `chapter_01/`.
The "assembly" **reStructuredText** file is then named `index.rst`, and uses the `.. mdinclude` directive to assemble the individual **Markdown** shards, shown in the [**reStructuredText** chapter index template](../../util/templates/chapter_index.rst).
The **Markdown** shards, in turn, will each begin with level-2 headers, and include only their section of the content.
This is demonstrated in the [**Markdown** shard template](../../util/templates/chapter_shard.rst).
The first shard should be named beginning with an underscore, followed by the chapter name (e.g. `_chapter_name.md`), similar to the convention for units.
A chapter may have a single shard; it is not necessary to break the content down further for short chapters.

#### Folder Structure

Taking all the information given above, the structure of the documentation source has a structure similar to that demonstrated below:

- unit_01/
    - chapter_1/
        - _ch1_name.md
        - index.rst
        - ch1_shard_1.md
        - ch1_shard_2.md
    - chapter_2/
        - _ch2_name.md
        - index.rst
        - ch2_shard_1.md
        - ch2_shard_2.md
        - ch2_shard_3.md
    - . . .
    - _unit_a.md
    - index.rst
- unit_02/
    - chapter_1/
        - _ch1_name.md
        - index.rst
        - ch1_shard_1.md
    - chapter_2/
        - _ch2_name.md
        - index.rst
        - ch2_shard_1.md
        - ch2_shard_2.md
    - . . .
    - _unit_b.md
    - index.rst
- . . .
