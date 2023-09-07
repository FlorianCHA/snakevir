Requirements
============

Snakevir requires |PythonVersions|, |SnakemakeVersions| and |graphviz|.

Snakevir is developed to work on an slurm HPC.

------------------------------------------------------------------------

Install Snakevir from github
============================

First, install the Snakevir python package with github and pip.

.. code-block:: bash
   python3 -m pip install snakevir
   snakevir --help

------------------------------------------------------------------------

Steps for HPC distributed cluster installation
==============================================

Snakevir uses any available snakemake profiles to cluster installation and resources management.
Run the command `snakevir install_cluster` to install tools and most databases needed by snakevir.
We tried to make cluster installation as easy as possible, but it is somehow necessary to adapt a few files according to your cluster environment.


.. click:: snakevir.main:install_cluster
   :prog: snakevir install_cluster
   :show-nested:

1. Adapt your cluster configuration
-------------------------------------

Now that Snakevir is installed, it proposes default configuration files, but they can be modified. Please check and adapt these files to your own system architecture.

For adapt the cluster configuration ou can use the `snakevir edit_cluster` command.

.. click:: snakevir.main:edit_cluster
   :prog: snakevir edit_cluster
   :show-nested:

2. Adapt tools
--------------

As Snakevir uses many tools, you must install them using the `snakevir edit_tools` command.

.. note::
    This function is in progress.


.. |PythonVersions| image:: https://img.shields.io/badge/python-3.7%2B-blue
   :target: https://www.python.org/downloads
   :alt: Python 3.7+

.. |SnakemakeVersions| image:: https://img.shields.io/badge/snakemake-≥5.10.0-brightgreen.svg?style=flat
   :target: https://snakemake.readthedocs.io
   :alt: Snakemake 5.10.0+

.. |graphviz| image:: https://img.shields.io/badge/graphviz-%3E%3D2.40.1-green
   :target: https://graphviz.org/
   :alt: graphviz 2.40.1+
