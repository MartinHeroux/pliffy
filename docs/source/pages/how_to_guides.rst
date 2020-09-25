How To Guides
=============

Save figure
-----------
To save a **pliffy** plot, we have to specify a minimum of three things in `PliffyInfoABD`:

    - `figure_name`
    - `save`
    - `save_path`

For example:

.. code-block:: python

    >>> from pliffy import PliffyInfoABD, plot_abd
    >>> import random
    >>> random.seed(42)
    >>> data = [random.random() * 100 for _ in range(60)]
    >>> data_a = data[:30]
    >>> data_b = data[30:]
    >>> info = PliffyInfoABD(data_a=data_a,
                             data_b=data_b,
                             figure_name='great_figure',
                             save=True,
                             save_path='/home/martin/Desktop/'
                             )
    >>> plot_abd(info)

This will save our **pliffy** plot with the name `great_figure.png` to the specified folder. The plot is saved as a `png` at a `dpi=180` because these are the default values.

These can easily be changed:

.. code-block:: python

    >>> info = PliffyInfoABD(data_a=data_a,
                             data_b=data_b,
                             figure_name='great_figure',
                             save=True,
                             save_path='/home/martin/Desktop/',
                             dpi=300,
                             save_type='png',
                             )
    >>> plot_abd(info)

Alternatively, we may want to save our plot to a vector-based format, like `svg` or `pdf`. This too is possible with **pliffy**.

.. code-block:: python

    >>> info_pdf = PliffyInfoABD(data_a=data_a,
                              data_b=data_b,
                              figure_name='great_figure_pdf',
                              save=True,
                              save_path='/home/martin/Desktop/',
                              save_type='pdf',
                              )
    >>> plot_abd(info_pdf)
    >>> info_svg = PliffyInfoABD(data_a=data_a,
                              data_b=data_b,
                              figure_name='great_figure_svg',
                              save=True,
                              save_path='/home/martin/Desktop/',
                              save_type='svg',
                              )
    >>> plot_abd(info_svg)

Add pliffy plots as subplots to a figure
----------------------------------------
Thus far we have generated **pliffy** plots on their own. However, by passing a matplotlib axis object to the `plot_abd` function, we can create a **pliffy** plot on a pre-existing figure.

for example, this is useful if we want to create a pair of related **pliffy** plots, one on top of the other, for a one-column figure in the paper we are about to submit.

.. code-block:: python

    >>> from pliffy import PliffyInfoABD, plot_abd
    >>> import random
    >>> random.seed(42)
    # Generate random data for first subplot
    >>> data = [random.random() * 100 for _ in range(60)]
    >>> data_a = data[:30]
    >>> data_b = data[30:]
    # Create figure
    >>> fig, axes = plt.subplots(ncols=2, figsize=(3, 6))
    # Create info for first subplot, and plot (note show=False)
    >>> info1 = PliffyInfoABD(data_a=data_a, data_b=data_b,  show=False)
    >>> plot_abd(info1, axes[0])
    # Generate random data for second subplot
    >>> data = [random.random() * 100 for _ in range(60)]
    >>> data_a = data[:30]
    >>> data_b = data[30:]
    # Create info for second subplot, and plot (note show=True)
    >>> info2 = PliffyInfoABD(data_a=data_a, data_b=data_b,  show=True)
    >>> plot_abd(info2, axes[1])

.. image:: ../img/how_to_subplots.png
   :width: 250
   :align: center

That looks pretty good. But what if we want to prepare a publication-quality figure? All that is missing (other than actual data and axes labels!) are the letters to reference to our subplots. This can easily be added with matplotlib.

.. code-block:: python

    >>> import matplotlib.pyplot as plt
    >>> for ax, letter in zip(axes, ('A', 'B')):
            ax.text(-0.4, 1, letter, fontsize=16, transform=ax.transAxes)

.. image:: ../img/how_to_subplots2.png
   :width: 250
   :align: center