#!/usr/bin/env python

import sys
import argparse
from pathlib import Path
import pandas as pd


def parse_arguments():
    parser = argparse.ArgumentParser(
               description="Concatenate all available prediction tsvs"
    )
    optionalArgs = parser._action_groups.pop()
    optionalArgs.title = "Optional Arguments"

    requiredArgs = parser.add_argument_group("Required arguments")

    requiredArgs.add_argument(
        "-i",
        "--input",
        dest="input_fp",
		nargs='*',
        required=True,
        help="The list of prediction tsvs to concatenate",
    )
    requiredArgs.add_argument(
        "-o",
        "--output",
        dest="output_fp",
        type=lambda p: Path(p).resolve(),
        required=True,
        help="The concatenated file path",
    )

    parser._action_groups.append(optionalArgs)

    return parser.parse_args()

def htp_to_df(htp_fp):
	htp_df = pd.read_csv(htp_fp, sep='\t', index_col = 0,
		names=['contig_id', 'htp_proba'])

	return htp_df


def predictions_tsv_to_df(predictions_fp, tool_name):
	pred_col = '_'.join([tool_name, 'pred'])
	score_col = '_'.join([tool_name, 'score'])
	pred_df = pd.read_csv(predictions_fp, sep = '\t', index_col = 0,
		names=['contig_id', pred_col, score_col],
		dtype={'contig_id' : 'string',
				pred_col : 'string',
				score_col : 'float64'
				}
				)
	return pred_df

if __name__ == '__main__':
	args = parse_arguments()

	tsvs = map(Path, args.input_fp)

	results_dfs = []
	for tsv in tsvs:
		if tsv.parent.name == 'htp':
			htp_df = htp_to_df(tsv)
			results_dfs.append(htp_df)
		elif tsv.parent.name in ['vhmnet', 'rafah', 'vhulk', 'wish']:
			tool_df = predictions_tsv_to_df(tsv, tsv.parent.name)
			results_dfs.append(tool_df)
#			tool_name = tsv.parent.name
#			predictions_dic = parse_predictions_tsv(tsv)
#			results.append({tool_name : predictions_dic})
		else:
			print("WTF?")

	if len(results_dfs) > 1:
		first_df = results_dfs.pop(0)
		final_df = first_df.join(results_dfs, sort=True)
	elif len(results_dfs) == 1:
		final_df = results_dfs[0]
	else:
		final_df = None

	if final_df is not None:
		final_df.to_csv(args.output_fp, sep='\t')
	else:
		print("THINGS WENT WRONG")
		sys.exit(1)
