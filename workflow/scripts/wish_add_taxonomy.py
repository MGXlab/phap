#!/usr/bin/env python

import argparse
import pandas as pd
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(
               description="Add taxonomy column to WIsH predictions.list"
    )
    optionalArgs = parser._action_groups.pop()
    optionalArgs.title = "Optional Arguments"

    requiredArgs = parser.add_argument_group("Required arguments")

    requiredArgs.add_argument("-i",
                              "--input",
                              dest="input_fp",
                              required=True,
                              type=lambda p: Path(p).resolve(strict=True),
                              help="Input predictions.list",
    )
    requiredArgs.add_argument("-t",
                              "--taxa-info",
                              dest="taxa_info",
                              required=True,
                              type=lambda p: Path(p).resolve(strict=True),
                              help="hostTaxa.pkl file from data",
                              )

    requiredArgs.add_argument("-o",
                              "--output",
                              dest="output_fp",
                              type=lambda p: Path(p).resolve(),
                              required=True,
                              help="File to write results in",
                              )

    parser._action_groups.append(optionalArgs)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    # Read in the pkl taxonomy
    taxa_info = pd.read_pickle(args.taxa_info)

    # Read in the predictions file
    preds = pd.read_csv(args.input_fp,
                        sep='\t',
                        index_col = "Phage",
                        )
    # Create the values of the column to be appended
    taxa_col = []
    for phage in preds.index.values:
        # Get the GCF_ id for this prediction
        host_id = preds.loc[phage, "Best hit among provided hosts"]
        # Get its value from the taxonomy table
        taxon = ';'.join(taxa_info.loc[host_id].values)
        taxa_col.append(taxon)

    # Append the column to the original df
    preds['taxonomy'] = taxa_col
    # Slice only the host taxonomy and its ll score
    preds = preds[['taxonomy', 'LogLikelihood']]

    # Sort index
    preds.sort_index(inplace=True)
    # Write the modified df to the specified file
    preds.to_csv(args.output_fp,
                 sep = '\t',
                 header=False
                 )

