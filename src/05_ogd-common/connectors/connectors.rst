`opengamedata-common` Chapter 1: Connectors, Interfaces, & Outerfaces
=====================================================================

OpenGameData uses classes called ``connectors`` to aid in loading input data and writing output data.
Specific ``connector`` subclasses, called ``interface``s, perform **in**put, and subclasses called ``outerface``s perform **out**put.
Because these are such fundamental and important pieces of the architecture, and because 3rd-party users are able and encouraged to extend the set of available in/outerfaces, these deserve their own chapter.

TODO : This whole chapter will be reworked to merge the various stabs at writing up documentation

.. include:: ./connectors_and_interfaces.md
   :parser: myst_parser.sphinx_

.. include:: ./intro_to_interfaces.md
   :parser: myst_parser.sphinx_

.. include:: ./storage_connectors.md
   :parser: myst_parser.sphinx_

.. include:: ./interface_classes.md
   :parser: myst_parser.sphinx_

.. include:: ./writing_an_interface.md
   :parser: myst_parser.sphinx_

.. include:: ./outerface_classes.md
   :parser: myst_parser.sphinx_

.. include:: ./writing_an_outerface.md
   :parser: myst_parser.sphinx_

.. include:: ./current_supported_connectors.md
   :parser: myst_parser.sphinx_
