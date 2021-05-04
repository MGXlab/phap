# Usage

A dry-run (_always a good idea before each execution_)
```
(phap)$ snakemake -n --use-singluarity
--singularity-args "-B /path/to/databases/data:/data"
```

Basic:
```
# From within this directory
# Make sure you have defined a samplesheet
(phap)$ snakemake -p --use-singularity -j16 \
--singularity-args "-B /path/to/databases/data:/data"
```

where `/path/to/database/data` is the directory containing tables, 
WIsH models and CRISPR blast [databases](#data-dependencies).

* The `-j` flag controls the number of jobs (cores) to be run in parallel.
Change this according to your setup.
* The `-p` flag prints commands that are scheduled for execution.
* Binding the data dir with the `--signularity-args` is required. 
You **must also provide this path as a value** for the `data_dir` option
in the `config.yaml`.

