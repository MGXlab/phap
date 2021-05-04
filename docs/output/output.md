# Output

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

## Per sample
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

## Per tool

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

Log files capturing stdout and stderr during execution of each rule can be 
found in `workdir/logs/<sample_id>/*.log` files.

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

