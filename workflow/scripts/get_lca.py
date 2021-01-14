#!/usr/bin/env python
import argparse
import pandas as pd
from pathlib import Path
from ete3 import NCBITaxa
import itertools


def parse_arguments():
    parser = argparse.ArgumentParser(
               description="Parse all_predictions.tsv to get LCA"
    )
    optionalArgs = parser._action_groups.pop()
    optionalArgs.title = "Optional Arguments"

    requiredArgs = parser.add_argument_group("Required arguments")

    requiredArgs.add_argument(
        "-i",
        "--input",
        dest="input_fp",
        required=True,
        type=lambda p: Path(p).resolve(strict=True),
        help="Input all_predictions.tsv",
    )
    requiredArgs.add_argument(
        "-o",
        "--output",
        dest="output_fp",
        type=lambda p: Path(p).resolve(),
        required=True,
        help="File to write LCA info",
    )

    optionalArgs.add_argument(
        '-d',
        '--db-file',
        dest='db',
        type=lambda p: Path(p).resolve(),
        required=False,
        help="Path to taxa.sqlite produced by ete3"
    )

    parser._action_groups.append(optionalArgs)

    return parser.parse_args()

def get_taxid(name):
    """
    Get a list of full taxonomy for a given name

    Args:
      name: str: A string of the name to search for e.g.
        'Escherichia coli' or 'Firmicutes'.
    Return:
      full_taxonomy: list: A list of the full lineage taxids

        If the given `name` is 'None` returns 'None'
    """
    if len(name.split()) > 2:
        name = ' '.join(name.split()[:2])
    if name == 'None':
        full_taxonomy = 'None'
    else:
        tax_dic = ncbi.get_name_translator([name])
        taxid = tax_dic[name][0]
        full_taxonomy = ncbi.get_lineage(taxid)
    return full_taxonomy

def translate_row(name_row):
    """
    Helper function to apply get_taxid on all columns
    of a row in a pd.DataFrame

    Args:
      name_row: pd.Series: A row of taxon identifiers

    Return:
      -: list: A list where all given human readable
        columns have been converted to lists of full
        taxonomy NCBI integers
    """
    return [get_taxid(i) for i in name_row]


def all_equal(iterable):
    # https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    Returns True if all the elements are equal to each other
    """
    g = itertools.groupby(iterable)
    return next(g, True) and not next(g, False)


def get_lca_dic(hosts_df, ncbi):
    """
    Get the LCA of all entries in a row from pd.DataFrame

    Input `hosts_df` has contig ids as index, with each
    column corresponding to full taxonomy lists.

    Args:
      hosts_df: pd.DataFrame: Contigs as index, columns 
        lists of full taxonomies
      ncbi: ete3.NCBITaxa instance:

    Return:
      lca_dic: dict: A dictionary of the form
        { contig_id: [ name , rank, lca ], ...}
        name is the human readable name of the taxon,
        rank is the human readable name of the rank,
        lca is the taxid number of the lca

    """
    lca_dic = {}
    for contig in hosts.index.values:
        # E.g. [[1,2,3,4], [1,2,3], 'None']
        all_lineages = [i for i in hosts_df.loc[contig,] if i != "None"]
        # [[1,2,3,4], [1,2,3]]
        per_level = [i for i in itertools.zip_longest(*all_lineages)]
        # [[1,1], [2,2], [3,3], [4, None]]
        for i in range(len(per_level)):
            lca = per_level[i][0] # First iteration, grab the root
            if all_equal(per_level[i+1]): # True until index 3 (last)
                lca = per_level[i+1][0] # 2
            else: # When we reach the first list where all_equal fails
                break
        # Following the example LCA = 3
        name_dic = ncbi.get_taxid_translator([lca]) # Translate to name
        name = name_dic[lca] # Get the name
        rank_dic = ncbi.get_rank([lca]) # Translate to rank
        rank = rank_dic[lca] # Get the rank
        lca_dic[contig] = [name, rank, lca] # Put them in a leas
    return lca_dic

if __name__ == '__main__':
    args = parse_arguments()

    ncbi = NCBITaxa(dbfile=args.db)

    # Read in the data
    data = pd.read_csv(args.input_fp,
                       sep='\t',
                       index_col='contig'
                       )
    prediction_cols = [c for c in data.columns if c.endswith('_pred')]

    # Slice and make a copy to supress SettingWithCopyWarning
    hosts = data[prediction_cols].copy()
    # Set the data type to string so the sanitizing will work
    for col in prediction_cols:
        hosts[col] = hosts[col].astype('string')

    # Sanitize columns to be able to query the taxonomy
    if 'vhulk_pred' in prediction_cols:
        hosts['vhulk_pred'] = hosts['vhulk_pred'].str.replace('_', ' ')

    if 'wish_pred' in prediction_cols:
        # Original is superkingdom;kingdom;...;species;name
        # This selects species
        hosts['wish_pred'] = hosts['wish_pred'].str.split(';').str.get(-2)
        # This splits the species and gets the first 2 elements
        # sometimes species contains strain info two
        hosts['wish_pred'] = hosts['wish_pred'].str.split().str[:2]
        # Rejoin the species in a single string `genus species`
        hosts['wish_pred'] = hosts['wish_pred'].str.join(' ')

    hosts = hosts.applymap(get_taxid)

    lca_data = get_lca_dic(hosts, ncbi)
    with open(args.output_fp, 'w') as fout:
        fout.write("{}\t{}\t{}\t{}\n".format('contig',
                                             'name',
                                             'rank',
                                             'lca')
                   )
        for i in lca_data:
            dstring = '\t'.join(map(str, lca_data[i]))
            fout.write("{}\t{}\n".format(i, dstring))

