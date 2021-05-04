.. _configuration:

Configuration
=============

The ``config_template.yaml`` file provided with this repo has all available 
configurable options. Short explanations are provided as commented blocks for 
each option.

A configuration for the workflow must be available as a ``config.yaml`` 
within the ``config`` directory. A separate ``my_config.yaml`` overriding the default
options can be supplied at runtime, e.g.

.. code-block:: bash

    $ snakemake --configfile=path/to/my_config.yaml \
    <rest of snakemake options>

You can either copy the ``config_template.yaml`` and rename it to
``config.yaml`` or make your edits straight on the template and rename it to
``config.yaml``.

**All fields included in the template must be specified**, unless otherwise stated
in the comment.

.. _config-input:

Input data
----------

The tools wrapped in this workflow expect phage sequences as input.
You should try to make sure that the input sequences you want to analyze 
correspond to phage genomes/contigs (or at least viruses).

A separate workflow to identify phage/viral genomes/contigs is 
`What the Phage <https://github.com/replikation/What_the_Phage>`_.

The current workflow can handle multiple samples. 
For each sample, **all viral contigs to be analyzed should be provided as a 
single multifasta** (can be ``gz``-ipped). 
A mapping between sample ids and their corresponding fasta file is provided as
a samplesheet, as described below.

.. _config-samplesheet:

Sample sheet
------------

You must define a samplesheet with two tab (``\t``) separated columns. The
header line must contain two fields, ``sample    fasta``. 
Values from the ``sample`` column must be unique and
are used as sample identifiers. Their corresponding ``fasta`` values must be
valid paths to (multi)fasta files with the phage sequences for that sample.

An example:

.. code-block:: bash

    $ cat samples.tsv
    sample	fasta
    s01	/path/to/s01.fna
    s02	/path/to/another.fna.gz

.. note::

    There is no need to follow any convention for the fasta file name to 
    reflect the sample id. The values in the sample column are the ones to worry
    about, as these are the ones used as wildcards within the Snakefile.

You can either fill in the location of the samplesheet within the ``config/config.yaml``.
or use ``snakemake``'s ``--config samplesheet=/path/to/my_samples.tsv`` mechanism when
executing the wofkflow.

