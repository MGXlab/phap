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
    if name == 'None':
        full_taxonomy = 'None'
    else:
        tax_dic = ncbi.get_name_translator([name])
        taxid = tax_dic[name][0]
        full_taxonomy = ncbi.get_lineage(taxid)
    return full_taxonomy

def translate_row(name_row):
    return [get_taxid(i) for i in name_row]

def all_equal(iterable):
    "Returns True if all the elements are equal to each other"
    g = itertools.groupby(iterable)
    return next(g, True) and not next(g, False)

def get_lca_dic(hosts_dic, ncbi):
    lca_dic = {}
    for contig in hosts.index.values:
        all_lineages = [i for i in hosts.loc[contig,] if i != "None"]
        per_level = [i for i in itertools.zip_longest(*all_lineages)]
        for i in range(len(per_level)):
            lca = per_level[i][0]
            if all_equal(per_level[i+1]):
                lca = per_level[i+1][0]
            else:
                break
        name_dic = ncbi.get_taxid_translator([lca])
        name = name_dic[lca]
        rank_dic = ncbi.get_rank([lca])
        rank = rank_dic[lca]
        lca_dic[contig] = [name, rank, lca]
        
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
    # Sanitize columns to be able to query the taxonomy
    hosts = data[prediction_cols]
    if 'vhulk_pred' in prediction_cols:
       hosts['vhulk_pred'] = hosts['vhulk_pred'].str.replace('_', ' ')

    if 'wish_pred' in prediction_cols:
        hosts['wish_pred'] =  [' '.join(i.split(';')[-2].split()[:2]) 
                              for i in data['wish_pred'].values]

    hosts = hosts.apply(translate_row)

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

