=========
TkLsystem
=========

TkLsystem provides a tkinter interface to work with L-System equations.

.. image:: http://i.imgur.com/EWOaBJD.png
    :alt: TkLsystem
    :align: center

:Author: Yaşar Arabacı, 2014
:License: Creative Commons Attribution-ShareAlike 4.0 International Public License
:Version: 0.1

The goal is to create a simple interface to work with L-system equation systems. It is
supposed to be easy to use.

Features
---------
- Saving rendered images
- Saving/Loading equation systems
- Comes with a lot of example systems
- Caching long strings and rendered images to improve performance and responsiveness

Installation
------------

From PyPI with pip (easy)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ pip install TkLsystem


From Source at Github
~~~~~~~~~~~~~~~~~~~~~

* Clone the repository

.. code-block:: bash

    $ git clone https://github.com/yasar11732/tklsystem.git

* Install with setup.py

.. code-block:: bash

    $ python setup.py install
	
Run
---
.. code-block:: bash

    $ lsystem

Grammar
-------
* +: Turn right by specified angle
* -: Turn left by specified angle
* U: Pen-up, nothing will be drawn until pen is down
* D: Pen-down, continue drawing
* j: Jump forward, short cut for "U, forward, D"
* [: Push position and heading to stack
* ]: Pop position and heading from stack

Any other character will be treated as an alias for forward, unless they are specified as constants. Constants
are no action characters that is only used to control the growing of the string.

Examples
--------
* Examples are loaded into file browser on the right side. Click them to load.

Files
-----
* Your saved files normally resides in ~/lsf_files directory. They are also automatically loaded to file browser when program starts.
* You can save and load your custom equations.