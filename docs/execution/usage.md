# Usage

A dry-run (_always a good idea before each execution_)

```
(phap)$ snakemake -n \
--use-conda \
--conda-frontend mamba \
--use-singularity \
--singularity-args "-B /path/to/databases/data:/data" 
```

## Basic

```
# From within this directory
# Make sure you have defined a samplesheet
(phap)$ snakemake -p \
--use-conda \
--conda-frontend mamba \
--use-singularity -j16 \
--singularity-args "-B /path/to/databases/data:/data"
```

where `/path/to/database/data` is the directory containing tables, 
WIsH models and CRISPR blast [databases](#data-dependencies).

* The `-j` flag controls the number of jobs (cores) to be run in parallel.
Change this according to your setup.
* The `-p` flag prints commands that are being submitted for execution.
* Binding the data dir with the `--signularity-args` is required. 
You **must also provide this path as a value** for the `data_dir` option
in the `config.yaml`.


## Advanced 

For more complex use cases (e.g. executing some intermediate step again 
without affecting the rest of the output) it is wise to check snakemake's help 
menu with 

```
$ snakemake --help
```

Daunting at first, but covers __a lot__.
