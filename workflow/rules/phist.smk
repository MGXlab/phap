rule run_phist:
    input:
        reflist = rules.split_multifasta.output.reflist
    output:
        raw_predictions = "results/{sample}/phist/raw_predictions.tsv",
        kmers_table = "results/{sample}/phist/kmers_table.txt"
    log:
        stderr = "logs/{sample}/phist.stderr"
    params:
        genomes_dir = "results/{sample}/tmp/genomes",
        hosts_db_genomes = "/data3",

    container:
        config['phist'].get('container')
    threads:
        config['phist'].get('threads', 8)
    shell:
        """
        python /PHIST/phist.py \
            -t {threads} \
            {params.genomes_dir} \
            {params.hosts_db_genomes} \
            {output.kmers_table} \
            {output.raw_predictions} 2> {log.stderr}
        """

rule process_phist:
    input:
        prediction_list = rules.run_phist.output.raw_predictions,
        reflist = rules.split_multifasta.output.reflist
    output:
        predictions_tsv = "results/{sample}/phist/predictions.tsv"
    params:
        hosts_db_taxonomy = config["phist"].get("taxids_file"),
        scrpt = srcdir("../scripts/phist_add_taxonomy.py")
    log:
        "logs/{sample}/process_phist.log"
    conda:
        "../envs/phap_utils.yaml"

    shell:
        "python {params.scrpt} "
        "-i {input.prediction_list} -t {params.hosts_db_taxonomy} "
        "-r {input.reflist} -o {output.predictions_tsv} 2>{log}"
