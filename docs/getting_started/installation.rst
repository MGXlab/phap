.. _conda: https://docs.conda.io/projects/conda/en/latest/ 

.. _installation:

Installation
============

.. _installation-software:

Software dependencies
---------------------
To run the workflow your will need

- ``snakemake > 6.x``
- ``singularity >= 3.6`` 
- ``mamba >= 0.15.2``

.. _installation-conda:

Conda environment
-----------------
It is recommended to use a conda_ environment.
The file ``conda-linux-54.lock`` can be used to recreate the complete environment 
used during development.

.. note::

   The provided ``lock`` file contains an explicit list of all packages,
   produced with ``conda-lock lock -f environment.yaml -p linux-64``.
   This ensures all packages are exactly the same versions/builds, so we 
   minimize the risk of running into dependencies issues

To get a working environment:

.. code-block:: bash 

    $ git clone https://github.com/MGXlab/phap.git
    $ cd phap

    # Note the long notation --file flag; -f will not work.
    $ conda create -n phap --file=conda-linux-64.lock

    # Activate it - use the name you gave above, if it is different
    $ conda activate phap

    # The (phap) prefix shows we have activated it
    # Check the snakemake version
    (phap) $ snakemake --version
    6.6.1

.. _installation-data:

Data dependencies
-----------------

* RaFaH, vHULK, HTP

For these tools there is no need to pre-download and setup anything - all 
data and software dependencies required for running them are bundled within 
their respective singularity image.

* VirHostMatcher-Net

Databases and models need to be downloaded from the VirHostMatcher data repo
`see here <https://github.com/WeiliWw/VirHostMatcher-Net#downloading>`_.
`Both models <https://github.com/WeiliWw/VirHostMatcher-Net#complete-genome-mode-and-short-viral-contig-mode>`_
for complete and short contigs were used during development.
The unpacked data must be used with the ``data_dir`` option within the 
`config.yaml <configuration>`_.

* WIsH

VirHostMatcher-Net authors also provide models for WIsH predictions.
The unpacked archive from above comes with a ``host_wish_model`` directory, which
contains 62,493 WIsH models for all genomes used in the
VirHostMatcher-Net paper. These are used here.

.. note::
    The location of the unpacked ``data`` archive - and **not** the path to 
    ``data/host_wish_model`` - must be used with the ``data_dir``
    option within the ``config.yaml``.

.. _installation-ncbi:

NCBI Taxonomy
-------------
The ``ete3.NCBITaxa`` class is used to get taxonomy information and calculate
the LCA of all predictions, when possible. This requires a ``taxa.sqlite``
to be available either in its default location
( ``$HOME/.ete3toolkit/taxa.sqlite`` ) or provided in the config. See more about
that on `ETE3's page <http://etetoolkit.org/docs/latest/tutorial/tutorial_ncbitaxonomy.html>`_.

.. _installation-singularity:

Singularity containers
----------------------

Definition files, along with documentation of how to use them to build 
the containers are in ``resources/singularity``.
The pre-built containers are all available through the 
`standard singularity library <https://cloud.sylabs.io/library/papanikos_182>`_.
These are pulled at runtime (or used from cache).
Alternatively, you can pull all ``.sif`` files from the cloud, store them locally.
You can then point the path to these image files in the ``config.yaml``.

