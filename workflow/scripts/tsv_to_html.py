#!/usr/bin/env python
import sys
import pandas as pd

df = pd.read_csv(sys.argv[1], sep='\t')

html_header = """<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.23/css/jquery.dataTables.min.css">
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.5.1.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.10.23/js/jquery.dataTables.min.js"></script>
</head>

<body>

"""

table_str = df.to_html(
    classes="datatable display", 
    table_id="tableone",
    border=0
    ) + '\n'

after_table = """\t<script class="init" type=text/javascript>

$(document).ready( 
function() { 
        $('#tableone').DataTable(); 
            } 
            );

  </script>
</body>
"""

full_html = html_header + table_str + after_table

with open(sys.argv[2], 'w') as fout:
    fout.write(full_html)
