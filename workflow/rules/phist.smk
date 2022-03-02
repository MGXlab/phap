rule run_phist:
    input:
        genomes_dir = rules.split_multifasta.output.genomes_dir
    output:
        raw_predictions = "results/{sample}/phist/raw_predictions.tsv",
        kmers_table = "results/{sample}/phist/kmers_table.txt"
    log:
        stderr = "logs/{sample}/phist.stderr"
    params:
        hosts_db_genomes = "/data3/hosts_genomes",

    container:
        config['phist'].get('container')
    threads:
        config['phist'].get('threads', 8)
    shell:
        """
        python /PHIST/phist.py \
            -t {threads} \
            {input.genomes_dir} \
            {params.host_db_genomes} \
            {output.phist_raw_pred} \
            {output.phist_raw_table}
        """

rule process_phist:
    input:
        prediction_list = rules.run_phist.output.raw_predictions
    output:
        predictions_tsv = "results/{sample}/phist/predictions.tsv"
    params:
        hosts_db_taxonomy = "/data3/hosts_taxonomy.txt",
        scrpt = srcdir("../scripts/phist_add_taxonomy.py")
    log:
        "logs/{sample}/process_wish.log"
    conda:
        "../envs/phap_utils.yaml"
    shell:
        "python {params.scrpt} "
        "-i {input.prediction_list} -t {params.hosts_db_taxonomy} "
        "-o {output.predictions_tsv} 2>{log}"
