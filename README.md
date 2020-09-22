[![spike2py](https://raw.githubusercontent.com/MartinHeroux/pliffy/master/docs/source/img/pliffy_650x200.png)](https://github.com/MartinHeroux/pliffy)


[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![coverage](https://img.shields.io/badge/coverage-98%25-yellowgreen)
    [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md)
[![Documentation Status](https://readthedocs.org/projects/spike2py/badge/?version=latest)](https://pliffy.readthedocs.io/en/latest/?badge=latest)

**pliffy** makes difference plots. These plots are simple and informative. At present, **pliffy** makes difference plots from two independent groups (e.g. treatment *vs* control) or two measurements made in the same group (e.g. pre-treatment *vs* post-treatment). All raw data points are plotted by default, and data is summarised with the mean and confidence interval. The confidence interval is calculated using the appropriate *t*-distribution and is set to 95% by default.

**pliffy** plots are simple to generate. The simplest **pliffy** plot only requires two inputs, `data_a` and `data_b`. Because these two datasets (**a** and **b**) are used to compute the **d**ifference, these plots are referred to `abd` plots. For example, lets imagine we already have our two datasets loaded:

```python
>>> from pliffy import PliffyInfoABD, plot_abd
>>> info = PliffyInfoABD(data_a=data_a, data_b=data_b)
>>> plot_abd(info)
```

[![emg_raw](https://raw.githubusercontent.com/MartinHeroux/pliffy/master/docs/source/img/readme_example1.png)](https://github.com/MartinHeroux/pliffy)


## Documentation

Introductory tutorials, how-to's and other useful documentation are available on [Read the Docs](https://spike2py.readthedocs.io/en/latest/index.html)

## Installing

**spike2py** is available on PyPI:

```console
$ python -m pip install pliffy
```

**pliffy** officially supports Python 3.8+.

## Contributing

Like this project? Want to help? We would love to have your contribution! Please see [CONTRIBUTING](CONTRIBUTING.md) to get started.

## Code of conduct

This project adheres to the Contributor Covenant code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [heroux.martin@gmail.com](heroux.martin@gmail.com).

## License

[GPLv3](./LICENSE)
