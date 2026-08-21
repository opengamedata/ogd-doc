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
From a high-level point of view, the documentation is organized in a hierarchy of *Guide* -> *Unit* -> *Chapter*.

Each *guide* contains documentation intended for a particular type of stakeholder within OpenGameData's software ecosystem. *Guides* are divided into *Units* that cover a significant segment of the documentation, and each *Unit* is, in turn, made up of several *Chapters*.

#### Guides

We currently provide guides for four stakeholders:

1. End Users, often researchers or data analysts, who use OGD tools and data but do not necessarily directly work with software code.
2. Game Producers, who have games that utilize OGD tools for data collection, and are responsible for any changes to their games (even if they do not directly modify game code themselves).
3. Game/Data Engineers, who directly write code in either a game or a new code module that works with existing OGD software frameworks, but do not directly work on the source code of OGD software itself.
4. Maintainers, who work directly on OGD software development.

Each guide should have a single `index.rst` that starts with a header, includes a few sentences or short paragraph introducing the guide, but is principally made up of a table of contents that includes the `index.rst` from each unit in the guide. Otherwise, there is no significant "implementation" of a guide - it is predominantly just an organizing structure.

In addition to the *guides*, there are two top-level structures: the "introduction," which could be seen as a cross-cutting guide to the docs themselves, and an "appendices" folder. These contain the same general structure as the proper "*guides*," even if they don't quite fit the semantic meaning of the term.

#### Units

A *unit* is meant to divide the content of a *guide* into reasonably-sized parts for ease of navigation. There is no hard-and-fast rule for the size of a *unit*; typically we base units on significant components of the work/tools used by the stakeholders for whom the guide is written.

For example, the maintainer *guide* has *units* for each major repository (or major collection of smaller repositories) in the OGD ecosystem. On the other hand, the engineer *guide* has *units* for each broad framework within which external engineering might take place, where each framework might involve multiple components that have their own units in the maintainer *guide*. Concretely, the logging *unit* of the engineer *guide* covers information about the client telemetry libraries, the logging API, and some information about data storage, each of which fall under separate units within the maintainer *guide*.

Structurally, there should be one folder for each *unit*, named according to the unit title.
The unit index is always named `index.rst` and contains a few sentences or brief paragraph of introduction, similar to the `index.rst` of a unit.
It then lists each chapter, providing a table of contents for the unit.
There is a [unit index template](../../util/templates/unit_index.rst) available.

#### Chapters

Chapters contain true content, so they are made up of an `index.rst` document merging multiple **Markdown** shards.

The pieces making up the chapter should be placed in a subfolder, with a name based on the topic of the chapter.
The "assembly" **reStructuredText** file is then named `index.rst`, and uses the `.. mdinclude` directive to assemble the individual **Markdown** shards, shown in the [**reStructuredText** chapter index template](../../util/templates/chapter_index.rst).
The **Markdown** shards, in turn, will each begin with level-2 headers, and include only their section of the content.
This is demonstrated in the [**Markdown** shard template](../../util/templates/chapter_shard.rst).
A chapter may have a single shard; it is not necessary to break the content down further for short chapters.

#### Folder Structure

Taking all the information given above, the structure of the documentation source has a structure similar to that demonstrated below:

- unit_a/
    - chapter_1/
        - index.rst
        - ch1_shard_1.md
        - ch1_shard_2.md
    - chapter_2/
        - index.rst
        - ch2_shard_1.md
        - ch2_shard_2.md
        - ch2_shard_3.md
    - . . .
    - index.rst
- unit_b/
    - chapter_1/
        - index.rst
        - ch1_shard_1.md
    - chapter_2/
        - index.rst
        - ch2_shard_1.md
        - ch2_shard_2.md
    - . . .
    - index.rst
- . . .
