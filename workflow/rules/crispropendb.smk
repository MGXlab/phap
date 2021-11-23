rule run_crispropendb:
    input:
        reflist = rules.split_multifasta.output.reflist
    output:
        crispropendb_raw = "results/{sample}/crispropendb/raw.txt"
    log:
        stderr = "logs/{sample}/crispropendb.stderr"
    params:
        fasta_dir = "./results/{sample}/tmp/genomes",
        sqlite_db = "/data2/CrisprOpenDB.sqlite",
        blast_db  = "/data2/SpacersDB"
    container:
        config['crispropendb'].get('container')
    threads:
        config['crispropendb'].get('threads', 8)
    shell:
        """
        printf "contig\traw_pred\n" > {output.crispropendb_raw}
        for f in $(find {params.fasta_dir} -wholename "*.fasta");
        do
            contig_id=$(basename ${{f}} | sed -e 's/\.fasta//' )
            pred=$(python /CrisprOpenDB/CL_Interface.py \
                    -q {params.sqlite_db} \
                    -b {params.blast_db} \
                    -n {threads} \
                    -i ${{f}} 2>{log.stderr})
            fmt_pred=$(echo ${{pred}} | sed -e 's/\\n//')
            echo -e "$contig_id\t$fmt_pred" >> {output.crispropendb_raw}
        done
        """

rule process_crispropendb:
    input:
        crispropendb_raw = rules.run_crispropendb.output.crispropendb_raw
    output:
        predictions_tsv = "results/{sample}/crispropendb/predictions.tsv"
    run:
        lines = [line.strip().split("\t") for line in open(input.crispropendb_raw).readlines()]
        with open(output.predictions_tsv, "w") as fout:
            for line in lines[1:]: # discard header
                # no hits were found
                if "Sorry" in line[1]:
                    fout.write(f"{line[0]}\tNone\t0\n")
                # hits were found
                else:
                    fields   = line[1].replace("'", "").split(", ")
                    taxa     = fields[1]
                    criteria = fields[2][:-1] # exclude last parenthesis
                    fout.write(f"{line[0]}\t{taxa}\t{criteria}\n")
