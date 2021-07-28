# vHULK
rule run_vhulk:
    input:
        rules.split_multifasta.output.reflist
    output:
        results_csv = "results/{sample}/vhulk/results.csv"
    params:
        fasta_dir = "results/{sample}/tmp/genomes",
        output_dir = "results/{sample}/vhulk"
    log:
        "logs/{sample}/vhulk.log"
    container:
        config['vhulk'].get('container')
    threads:
        config['vhulk'].get('threads', 8)
    shell:
        "vHULK.py -i {params.fasta_dir} "
        "-o {params.output_dir} "
        "-t {threads} --all &>{log}"

rule process_vhulk:
    input:
        vhulk_csv = rules.run_vhulk.output.results_csv
    output:
        vhulk_tsv = "results/{sample}/vhulk/predictions.tsv"
    log:
        "logs/{sample}/process_vhulk.log"
    conda:
        "../envs/phap_utils.yaml"
    shell:
        "tail -n+2 {input.vhulk_csv} | cut -d ',' -f 1,10,11 "
        "| tr ',' '\t' | sort -k1 1>{output.vhulk_tsv} 2>{log}"
