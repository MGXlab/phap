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

* CrispropenDB

Data are provided by the authors on this
`link <http://crispr.genome.ulaval.ca/dash/PhageHostIdentifier_DBfiles.zip>_`.
Once you download the archive unzip it and build the required BLAST db files.

To make sure that the BLAST db is compatible with the blast version wrapped
in the singularity image that is used here you can ``cd`` in the unzipped
directory from above and run

.. code-block:: bash

    $ singularity run library://dcarrillo/default/crispropendb:0.1 \
            makeblastdb -in SpacersDB.fasta \
            -out SpacersDB \
            -dbtype nucl

The resulting database files can be moved with the rest of the unzipped files.
You should have a final data directory with the following contents

.. code-block:: bash:

   $ tree data
    data
    ├── CrisprOpenDB.sqlite
    ├── SpacersDB.00.nhr
    ├── SpacersDB.00.nin
    ├── SpacersDB.00.nsq
    ├── SpacersDB.01.nhr
    ├── SpacersDB.01.nin
    ├── SpacersDB.01.nsq
    ├── SpacersDB.nal
    ├── SpacersDB.ndb
    ├── SpacersDB.not
    ├── SpacersDB.ntf
    └── SpacersDB.nto

The location of this ``data`` directory must be supplied separately as a mount
point for singularity ``data2`` if you want to run ``CrisprOpenDB``.

* PHIST

Authors don't provide a default database. To create one, it must be a
folder containing genome assemblies of the candidate hosts in FASTA format, one
file per species. A file describing the taxonomy for these genomes is also
required.

For development, we used a subset of RefSeq containing [bacterial and archaeal
reference and representative sequences](https://www.ncbi.nlm.nih.gov/assembly/?term=(Bacteria%5Borgn%5D+OR+Archaea%5Borgn%5D)+AND+(reference_genome%5Bfilter%5D+OR+representative_genome%5Bfilter%5D)).
If you wish to use this database, we provide ``resources/phist_genomes_download.txt``
with the commands to download the genomes (14,983 bacterial + 511 archaeal
genomes, listed on March 4 2022). Taxonomy in the form of taxid can be found
under ``resources/phist_genomes_taxids.txt``.

.. code-block:: bash:

   # Create directory to store the genomes.
   $ mkdir -p phist_db/hosts_genomes

   # Download genomes using parallel and 5 CPUs
   $ parallel --joblog download.log -j 5 :::: phist_genomes_download.txt

If you want to run this tool, the  directory containing the genomes 
(``hosts_genomes`` in example above) must be supplied separately as a mount
point for singularity ``data3``.

Taxonomy file must be a two-columns tabular file containing the name of the
assembly file and its taxid as shown below. The location of this file should be
provided in the ``taxids_file`` option within the  `config.yaml <configuration>`_.

.. code-block:: bash:

    $ head resources/phist_genomes_taxids.txt

    genome_file	taxid
    GCF_000005845.2_ASM584v2_genomic.fna.gz	511145
    GCF_000006605.1_ASM660v1_genomic.fna.gz	306537
    GCF_000006685.1_ASM668v1_genomic.fna.gz	243161
    GCF_000006765.1_ASM676v1_genomic.fna.gz	208964



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
