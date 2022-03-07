import argparse, os
import pandas as pd
from pathlib import Path
from ete3 import NCBITaxa
from Bio import SeqIO

ncbi = NCBITaxa()

def parse_arguments():
    parser = argparse.ArgumentParser(
               description="Add taxonomy column to PHIST 'raw_predictions.tsv'"
    )
    optionalArgs = parser._action_groups.pop()
    optionalArgs.title = "Optional Arguments"

    requiredArgs = parser.add_argument_group("Required arguments")

    requiredArgs.add_argument("-i",
                              "--input",
                              dest="input_fp",
                              required=True,
                              type=lambda p: Path(p).resolve(strict=True),
                              help="Input 'raw_predictions.tsv'",
    )

    requiredArgs.add_argument("-r",
                              "--reflist",
                              dest="reflist",
                              required=True,
                              type=lambda p: Path(p).resolve(strict=True),
                              help="reflist to gather all the genomes_ids",
    )
    requiredArgs.add_argument("-t",
                              "--taxa-info",
                              dest="taxa_info",
                              required=True,
                              type=lambda p: Path(p).resolve(strict=True),
                              help="'hosts_taxonomies.txt' file from data3/",
                              )

    requiredArgs.add_argument("-o",
                              "--output",
                              dest="output_fp",
                              type=lambda p: Path(p).resolve(),
                              required=True,
                              help="File to write results in",
                              )
    optionalArgs.add_argument(
                            '-d',
                            '--db-file',
                            dest='db',
                            type=lambda p: Path(p).resolve(),
                            default=Path.home() / Path(".etetoolkit/taxa.sqlite"),
                            required=False,
                            help="Path to taxa.sqlite produced by ete3"
                            )

    parser._action_groups.append(optionalArgs)

    return parser.parse_args()

if __name__ == '__main__':

    args = parse_arguments()
    ncbi = NCBITaxa(dbfile=args.db)


    # iterate the FASTA genomes in the reflist. Store the pair
    # fasta_file_name - genome_id
    file_genome_ids = dict()
    with open(args.reflist, "r") as fin:
       for line in fin:
           file_name = os.path.basename(line.strip())
           with open(line.strip()) as handle:
                for record in SeqIO.parse(handle, "fasta"):
                    file_genome_ids[file_name] = record.id


    # init a dataframe with the file_name and the genome_id
    to_df = [[file_name, genome_id, None, 0] for file_name, genome_id in file_genome_ids.items()]
    to_write_df = pd.DataFrame(to_df, columns=["file_name", "genome_id", "host", "adjp"])
    to_write_df.set_index("file_name", inplace=True)


    # Read in the tabular taxonomy annotation
    taxa_df = pd.read_csv(args.taxa_info, sep="\t", header=0, index_col=0)
    # get scinames for all the taxids in the taxid column
    scinames = ncbi.get_taxid_translator(taxa_df["taxid"].tolist())

    for host_genome in taxa_df.index:
        taxid = taxa_df.loc[host_genome, "taxid"]
        if taxid in scinames:
            taxa_df.loc[host_genome, "sciname"] = scinames[taxid]


    # read virus-host predicted pairs
    preds_df = pd.read_csv(args.input_fp, header=0)
    # filter by adj.p-value < 0.05
    preds_df = preds_df[preds_df["adj-pvalue"] <= 0.05]

    # iterate the predictions, keep the first one for each viral genome
    for index in preds_df.index:
        viral_file_name = preds_df.loc[index, "phage"]
        host_file_name = preds_df.loc[index, "host"]
        # check there are no previous assignments
        if to_write_df.loc[viral_file_name, "host"] != "None":

            to_write_df.loc[viral_file_name, "host"] = taxa_df.loc[host_file_name, "sciname"]
            to_write_df.loc[viral_file_name, "adjp"] = preds_df.loc[index, "adj-pvalue"]


    # write to final output
    to_write_df.to_csv(args.output_fp,
                        sep = '\t',
                        header=False,
                        index=False,
                        na_rep="None"
                        )
