# phap - Phage Host Analysis Pipeline

A snakemake workflow that wraps various phage-host prediction tools.

When possible, tools **and** their dependencies are bundled in 
[Singularity](https://sylabs.io/) containers.

## Current tools

|Tool name (links to source) | Publication/Preprint |
|:------|:------|
[RaFAh](https://sourceforge.net/projects/rafah/)|[Coutinho FH. et al. 2020](https://www.biorxiv.org/content/10.1101/2020.09.25.313155v1?rss=1)
[vHuLK](https://github.com/soedinglab/wish)|[Amgarten D, et al., 2020](https://www.biorxiv.org/content/10.1101/2020.12.06.413476v1)


## Installation

### Dependencies

To run the workflow your will need
- `snakemake > 5.x` (developed with `5.30.1`)
- `singularity >= 3.6` (developed with `3.6.3`)
- `biopython >= 1.78` (developed with `1.78`)

### Conda environemnt

It is recommended to use a [conda environment](https://docs.conda.io/projects/conda/en/latest/).
The file `environment.txt` can be used to recreate the complete environment 
used during development.

> The provided `environment.txt` contains an explicit list of all packages,
> produced with `conda list -n hp --explicit > environment.txt` .
> This ensures all packages are exactly the same versions/builds, so we 
> minimize the risk of running into dependencies issues

To get a working environment
```
# Clone this repo
$ git clone https://git.science.uu.nl/papanikos/phap.git

# Get in the dir
$ cd phap

# I am naming the environment `phap` here, you can call it whatever you like
# Note the long notation --file flag; -f will not work.
$ conda create -n phap --file=environment.txt

# Activate it - use the name you gave above, if it is different
$ conda activate phap

# The (hp) prefix shows we have activated it
# Check the snakemake version
(phap) $ snakemake --version
5.30.1
```

## Configuration

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

You must define a samplesheet with two comma (`,`) separated columns and the
header `sample,fasta`. Values from the `sample` column must be unique and
are used as sample identifiers. Their corresponding `fasta` values must be
valid paths to multifasta files with the phage sequences for that sample.

An example
```
$ cat samples.csv
sample,fasta
s01,/path/to/s01.fna
s02,/path/to/another.fna.gz
```

> Note
> There is no need to follow any convention for the fasta file name to 
> reflect the sample id. The values in the sample column are the ones to worry
> about, as these are the ones used as wildcards within the Snakefile.

You can
- Fill in the location of the samplesheet within the `config.yml`.
- Drop the file in the workdir - **Attention**: It should be named `samples.csv`
- Use `snakemake`'s `--config samplesheet=/path/to/my_samples.csv` when
executing the wofkflow.

### Models and other data dependencies

For these tools there is no need to pre-download and setup anything - all 
data and software dependencies are pulled with the singularity image.

* RaFaH
* vHuLK

## Usage

Basic:
```
# From within this directory
# Make sure you have defined a samplesheet
(hp)$ snakemake --use-singularity -j16
```

## Output

All output is stored under a `results` directory within the main workdir.
Results are stored per sample according to the sample ids you provided in the
sample sheet.
For each sample, results for each tool are stored in directories named after 
the tool. An example looks like this:
```
results/
├── A
│   ├── all_predictions.tsv
│   ├── rafah
│   │   ├── A_CDS.faa
│   │   ├── A_CDS.fna
│   │   ├── A_CDS.gff
│   │   ├── A_CDSxMMSeqs_Clusters
│   │   ├── A_Genomes.fasta
│   │   ├── A_Genome_to_Domain_Score_Min_Score_50-Max_evalue_1e-05.tsv
│   │   ├── A_Ranger_Model_3_Predictions.tsv
│   │   ├── A_Seq_Info.tsv
│   │   └── predictions.tsv
│   ├── tmp
│   │   ├── genomes
│   │   └── reflist.txt
│   └── vhulk
│       ├── predictions.tsv
│       └── results.csv

```

* `all_predictions.tsv`: Contains the best prediction per contig (rows) for 
each tool along with its confidence/p-value/whatever single value each tool 
uses to evaluate its confidence in the prediction.
An example for three genomes:
```
contig  vhulk_pred      vhulk_score     rafah_pred      rafah_score
NC_005964.2     None    4.068828        Mycoplasma      0.461
NC_015271.1     Escherichia_coli        1.0301523       Salmonella      0.495
NC_023719.1     Bacillus        0.0012575098    Bacillus        0.55
```

### Per tool
* `tmp` directory
  * Contains one fasta file per input genome, along with other intermediate 
files necessary for a smooth execution of the workflow **and the raw output 
of vhulk (under genomes/results/)**.

* `rafah`
  * All files prefixed with `<sample_id>_` are the rafah's raw output
  * `predictions.tsv`: A selection of the 1st (`Contig`) , 6th 
(`Predicted_Host`) and 7th (`Predicted_Host_Score`) columns from file 
`<sample_id>_Seq_Info.tsv`

* `vhulk`
  * `results.csv`: Copy of the `results/sample/tmp/genomes/results/results.csv`
  * `predictions.tsv`: A selection of the 1st (`BIN/genome`), 10th (`final_prediction`) 
11th (`entropy`) columns from file `results.csv`.

### Logs

Logs capturing stdout and stderr during execution of each rule are located in
`workdir/logs/<sample_id>/*.log` files.

