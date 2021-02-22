# phap - Phage Host Analysis Pipeline

A snakemake workflow that wraps various phage-host prediction tools.

[![Snakemake](https://img.shields.io/badge/snakemake-≥5.30-brightgreen.svg?style=flat)](https://snakemake.readthedocs.io)


* Uses 
[Singularity](https://sylabs.io/) containers for execution of all tools.
When possible (i.e. the image is not larger than a few `G`s), 
tools **and** their dependencies are bundled in the same container. This means
you do not need to get models or any other external databases.
* Calculates Last Common Ancestor of all tools per contig.

##### Contents
-----

* [Installation](#installation)
  - [Software dependencies](#software-dependencies)
  - [Conda environment](#conda-environment)
* [Data dependencies](#data-dependencies)
  - [NCBI Taxonomy](#ncbi-taxonomy)
  - [Singularity containers](#singularity-containers)
* [Configuration](#configuration)
  - [Input](#input-data)
  - [Samplesheet](#sample-sheet)
* [Usage](#usage)
* [Output](#output)
* [Logs](#logs)
* [Report](#report)


## Current tools

|Tool (source) | Publication/Preprint | Comments |
|:------|:------|:------:|
[HTP](https://github.com/wojciech-galan/viruses_classifier)|[Gałan W. et al., 2019](https://www.nature.com/articles/s41598-019-39847-2)|ok
[RaFAh](https://sourceforge.net/projects/rafah/)|[Coutinho F. H. et al., 2020](https://www.biorxiv.org/content/10.1101/2020.09.25.313155v1?rss=1)|ok
[vHuLK](https://github.com/LaboratorioBioinformatica/vHULK)|[Amgarten D. et al., 2020](https://www.biorxiv.org/content/10.1101/2020.12.06.413476v1)|ok
[VirHostMatcher-Net](https://github.com/WeiliWw/VirHostMatcher-Net)|[Wang W. et al., 2020](https://doi.org/10.1093/nargab/lqaa044)|ok
[WIsH](https://github.com/soedinglab/WIsH)|[Galiez G. et al., 2017](https://academic.oup.com/bioinformatics/article/33/19/3113/3964377)|ok (unnecessary?)

## Installation

### Software dependencies

To run the workflow your will need
- `snakemake > 5.x` (developed with `5.30.1`)
- `singularity >= 3.6` (developed with `3.6.3`)

The following python packages are also required to be installed and available 
in the execution environment
- `biopython >= 1.78` (developed with `1.78`)
- `ete3 >= 3.1.2` (developed with `3.1.2`)


### Conda environment

It is recommended to use a 
[conda environment](https://docs.conda.io/projects/conda/en/latest/).
The file `environment.txt` can be used to recreate the complete environment 
used during development.

> The provided `environment.txt` contains an explicit list of all packages,
> produced with 
>
> `conda list -n phap --explicit > environment.txt`
> 
> This ensures all packages are exactly the same versions/builds, so we 
> minimize the risk of running into dependencies issues

To get a working environment
```
# Clone this repo and get in there
$ git clone https://git.science.uu.nl/papanikos/phap.git
$ cd phap

# Note the long notation --file flag; -f will not work.
$ conda create -n phap --file=environment.txt

# Activate it - use the name you gave above, if it is different
$ conda activate phap

# The (phap) prefix shows we have activated it
# Check the snakemake version
(phap) $ snakemake --version
5.30.1
```

## Data dependencies

* RaFaH, vHULK, HTP

For these tools there is no need to pre-download and setup anything - all 
data and software dependencies required for running them are bundled within 
their respective singularity image.

* VirHostMatcher-Net

Databases and models need to be downloaded from the VirHostMatcher data repo
([see here](https://github.com/WeiliWw/VirHostMatcher-Net#downloading)). The 
[both_models](https://github.com/WeiliWw/VirHostMatcher-Net#complete-genome-mode-and-short-viral-contig-mode)
option was used during development.

The unpacked data must be used with the `data_dir` option within the 
[config.yaml](#configuration).

* WIsH

VirHostMatcher-Net authors also provide models for WIsH predictions.
The unpacked archive from above comes with a `host_wish_model` directory, which
contains 62,493 WIsH models for all genomes used in the
VirHostMatcher-Net paper. These are used here.

The location of the unpacked `data` archive - and **not** the path to 
`data/host_wish_model` - must be used with the `data_dir`
option within the [config.yaml](#configuration).

### NCBI Taxonomy

The `ete3.NCBITaxa` class is used to get taxonomy information and calculate
the LCA of all predictions, when possible. This requires a `taxa.sqlite` 
to be available either in its default location
( `$HOME/.ete3toolkit/taxa.sqlite` ) or provided in the config. See more about
that on
[http://etetoolkit.org/docs/latest/tutorial/tutorial_ncbitaxonomy.html]()

### Singularity containers

Definition files, along with documentation of how to use them to build 
the containers are in [resources/singularity](./resources/singularity).

The pre-built containers are all available through the 
[standard singularity library](https://cloud.sylabs.io/library/papanikos_182).

These are pulled at runtime (or used from cache).

Alternatively, you can pull all `.sif` files from the cloud, store them locally 
and use these in an offline mode (see below).

## Configuration

The `config_template.yaml` file provided with this repo has all available 
configurable options. Short explanations are provided as commented blocks for 
each option.

A configuration for the workflow must be available as a `config.yaml` 
within the `config` directory. A separate `my_config.yaml` overriding the
options in the default config.yaml can be supplied at runtime, e.g.

```
$ snakemake --configfile=path/to/my_config.yaml \
<rest of snakemake options>
```

You can either copy the `config_template.yaml` and rename it to
`config.yaml` or make your edits straight on the template and rename it to
`config.yaml`.

All fields included in the template must be specified, unless otherwise stated
in the comment.


### Input data

The tools wrapped in this workflow expect phage sequences as input.
You should try to make sure that the input sequences you want to analyze 
correspond to phage genomes/contigs (or at least viruses).

You can probably input any valid fasta file but the 
[GIGO concept](https://en.wikipedia.org/wiki/Garbage_in,_garbage_out) 
is probably applicable.


A separate workflow to identify phage/viral genomes/contigs is 
[What the Phage](https://github.com/replikation/What_the_Phage).

The current workflow can handle multiple samples. 
For each sample, **all viral contigs to be analyzed should be provided as a 
single multifasta** (can be `gz`ipped). 
A mapping between sample ids and their corresponding fasta file is provided as
a samplesheet (see below).

### Sample sheet

You must define a samplesheet with two tab (`\t`) separated columns. The
header line must contain two fields, `sample    fasta`. 
Values from the `sample` column must be unique and
are used as sample identifiers. Their corresponding `fasta` values must be
valid paths to (multi)fasta files with the phage sequences for that sample.

An example
```
$ cat samples.tsv
sample	fasta
s01	/path/to/s01.fna
s02	/path/to/another.fna.gz
```

> Note
>
> There is no need to follow any convention for the fasta file name to 
> reflect the sample id. The values in the sample column are the ones to worry
> about, as these are the ones used as wildcards within the Snakefile.

You can
- Fill in the location of the samplesheet within the `config/config.yaml`.
- Use `snakemake`'s `--config samplesheet=/path/to/my_samples.tsv` when
executing the wofkflow.


## Usage

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


## Output

All output is stored under a `results` directory within the main workdir.
Results are stored per sample according to the sample ids you provided in the
sample sheet.
For each sample, results for each tool are stored in directories named after 
the tool. An example looks like this:

```
$ tree -L2 results/A
results/A
├── all_predictions.tsv
├── lca.tsv 
├── htp
│   ├── predictions.tsv
│   └── raw.txt
├── rafah
│   ├── A_CDS.faa
│   ├── A_CDS.fna
│   ├── A_CDS.gff
│   ├── A_CDSxMMSeqs_Clusters
│   ├── A_Genomes.fasta
│   ├── A_Genome_to_Domain_Score_Min_Score_50-Max_evalue_1e-05.tsv
│   ├── A_Ranger_Model_3_Predictions.tsv
│   ├── A_Seq_Info.tsv
│   └── predictions.tsv
├── tmp
│   ├── filtered.fa.gz 
│   ├── genomes
│   └── reflist.txt
├── vhmnet
│   ├── feature_values
│   ├── predictions
│   ├── predictions.tsv
│   └── tmp
├── vhulk
│   ├── predictions.tsv
│   └── results
└── wish
    ├── llikelihood.matrix
    ├── prediction.list
    └── predictions.tsv
```

### Per sample
---

<details>
<summary><code>all_predictions.tsv</code></summary>
Contains the best prediction per contig (rows) for 
each tool along with its confidence/p-value/whatever-single-value each tool 
uses to evaluate its confidence in the prediction.

An example for three genomes:

```
contig  htp_proba       vhulk_pred      vhulk_score     rafah_pred      rafah_score     vhmnet_pred     vhmnet_score    wish_pred       wish_score
NC_005964.2     0.8464285626352002      None    4.068828        Mycoplasma      0.461   Mycoplasma fermentans   0.9953  Bacteria;Tenericutes;Mollicutes;Mycoplasmatales;Mycoplasmataceae;Mycoplasma;Mycoplasma fermentans;Mycoplasma fermentans MF-I2   -1.2085700000000001
NC_015271.1     0.995161392517451       Escherichia_coli        1.0301523       Salmonella      0.495   Muricauda pacifica      0.9968  Bacteria;Proteobacteria;Gammaproteobacteria;Enterobacterales;Enterobacteriaceae;Raoultella;Raoultella sp. NCTC 9187;Raoultella sp. NCTC 9187       -1.3869200000000002
NC_023719.1     0.9999957241187084      Bacillus        0.0012575098    Bacillus        0.55    Clostridium sp. LS      1.0000  Bacteria;Firmicutes;Clostridia;Clostridiales;Clostridiaceae;Clostridium;Clostridium beijerinckii;Clostridium beijerinckii       -1.29454
```
</details>

<details>
<summary><code>lca.tsv</code></summary> 

Last Common Ancestor of predictions, based on taxonomy

An example for the genomes above:
```
contig  name    rank    lca
NC_005964.2	Mycoplasma	genus	2093
NC_015271.1	Enterobacteriaceae	family	543
NC_023719.1	Firmicutes	phylum	1239
```
</details>

<details>
<summary><code>tmp</code> (dir)</summary>

  * Directory `genomes`: Contains one fasta file per input genome
  * File `reflist.txt`: An intermediate file that holds paths to all produced 
genome fastas (used as intermediate file to ensure smooth execution)
  * File `filtered.fa.gz`: Fasta files containing sequences > 5000 bp.
</details>

### Per tool

<details>
<summary><code>htp</code></summary>

  * File `raw.txt`: The raw output of `htp` per contig
  * File `predictions.tsv`: **Two**-column separated tsv with contig id and
probability of host being a phage.
</details>

<details>
<summary><code>rafah</code></summary>

  * Files prefixed with `<sample_id>_` are the rafah's raw output
  * `predictions.tsv`: A selection of the 1st (`Contig`) , 6th 
(`Predicted_Host`) and 7th (`Predicted_Host_Score`) columns from file 
`<sample_id>_Seq_Info.tsv`
</details>

<details>
<summary><code>vhulk</code></summary>

  * File `results.csv`: Copy of the `results/sample/tmp/genomes/results/results.csv`
  * File `predictions.tsv`: A selection of the 1st (`BIN/genome`), 10th (`final_prediction`) 
11th (`entropy`) columns from file `results.csv`.
</details>

<details>
<summary><code>vhmnet</code></summary>

  * Directories `feature_values` and `predictions` are the raw output
  * Directory `tmp` is a temporary dir written by `VirHostMatcher-Net` for 
doing its magic.
  * File `predictions.tsv` contains contig, host taxonomy and scores.
</details>

<details>
<summary><code>wish</code></summary>

  * Files `llikelihood.matrix` and `prediction.list` are the raw output
  * File `predictions.tsv` has contig, host taxonomy and **llikelihood** scores.
</details>


## Logs

Logs capturing stdout and stderr during execution of each rule can be found in
`workdir/logs/<sample_id>/*.log` files.

## Report

**After successful execution** of the workflow, a (basic) html report with 
summary statistics can be produced with 

```
(phap)$ snakemake --use-singularity \
--singularity-args "-B path/to/data_dir:/data" --report phap.html
```

This will produce a `phap.html` file, making use of the information in the
`report` directory. 

The `report` directory contains the two main aggregated tables from
[the per sample results directory](#per-sample) rendered as html documents.
These are accessible under the Results category of the main `phap.html`.

