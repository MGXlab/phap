rule run_rafah:
    input:
        reflist = rules.split_multifasta.output.reflist,
    output:
        seq_info = "results/{sample}/rafah/{sample}_Seq_Info.tsv"
    params:
        prefix = "results/{sample}/rafah/{sample}",
        fasta_dir = "results/{sample}/tmp/genomes"
    log:
        "logs/{sample}/rafah.log"
    container:
        config['rafah'].get('container')
    threads:
        config['rafah'].get('threads', 8)
    shell:
        "RaFAH_v0.1.pl --genomes_dir {params.fasta_dir}/ "
        "--extension fasta --threads {threads} "
        "--file_prefix {params.prefix} "
        "&>{log}"


rule process_rafah:
    input:
        seq_info = rules.run_rafah.output.seq_info
    output:
        rafah_tsv = "results/{sample}/rafah/predictions.tsv"
    log:
        "logs/{sample}/process_rafah.log"
    conda:
        "envs/phap_utils.yaml"
    shell:
        "tail -n+2 {input.seq_info} | cut -f1,6,7 | sort -k1 "
        "> {output.rafah_tsv}"
