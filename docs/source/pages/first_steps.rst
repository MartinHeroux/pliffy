.. _installation:

Installation
============

Create a virtual environment
----------------------------

pliffy works with `Python 3.8 or above`_. It is recommended you create a dedicated `Python environment`_ before you install pliffy. In your project directory, run the following commands:

.. code-block:: bash

   python -m venv env

Then activate your new virtual environment.

On macOS and Linux:

.. code-block:: bash

   source env/bin/activate

On Windows:

.. code-block:: bash

   .\env\Scripts\activate

Install pliffy and its dependencies
-----------------------------------

With your virtual environment activated, run the following command:

.. code-block:: bash

   pip install pliffy

Testing your pliffy installation
--------------------------------

With your virtual environment activated, start Python and type the following:

.. code-block:: python

    >>> import pliffy
    >>> spike2py.demo()

.. _Python 3.8 or above: https://www.python.org/downloads/
.. _Python environment: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment
