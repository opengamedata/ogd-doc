*********************
Architecture Overview
*********************

.. include:: ./_overview.md
   :parser: myst_parser.sphinx_

.. include:: ./storage.md
   :parser: myst_parser.sphinx_

.. include:: ./processing.md
   :parser: myst_parser.sphinx_

.. TODO : port from .dot definition to an inline mermaid chart instead. Or maybe a non-inline chart in own file, for reusability.

Data processing is outlined by the graph below.

.. graphviz:: ./architecture.dot

.. include:: ./automation.md
   :parser: myst_parser.sphinx_

.. include:: ./apis.md
   :parser: myst_parser.sphinx_

.. include:: ./dashboards.md
   :parser: myst_parser.sphinx_

.. include:: ./game_schemas.md
   :parser: myst_parser.sphinx_
