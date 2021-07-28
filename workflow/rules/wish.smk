rule run_wish:
    input:
        reflist = rules.split_multifasta.output.reflist,
    output:
        prediction_list = "results/{sample}/wish/prediction.list",
        ll_mat = "results/{sample}/wish/llikelihood.matrix"
    log:
        "logs/{sample}/wish.log"
    threads:
        config['wish'].get('threads', 8)
    container:
        config['wish'].get('container')
    params:
        # snakemake --singularity-args binds the whole data dir to /data
        # see run_vhmnet rule
        models_dir = "/data/host_wish_model",
        output_dir = "results/{sample}/wish",
        fasta_dir = "results/{sample}/tmp/genomes"
    shell:
        "mkdir -p {params.output_dir} && "
        "WIsH -c predict -g {params.fasta_dir} "
        "-t {threads} -b "
        "-m {params.models_dir} -r {params.output_dir} "
        "&>{log}"

rule process_wish:
    input:
        prediction_list = rules.run_wish.output.prediction_list
    output:
        predictions_tsv = "results/{sample}/wish/predictions.tsv"
    params:
        hostTaxa_pkl = DATA_DIR.joinpath("tables/hostTaxa.pkl"),
        scrpt = srcdir("scripts/wish_add_taxonomy.py")
    log:
        "logs/{sample}/process_wish.log"
    conda:
        "../envs/phap_utils.yaml"
    shell:
        "python {params.scrpt} "
        "-i {input.prediction_list} -t {params.hostTaxa_pkl} "
        "-o {output.predictions_tsv} 2>{log}"
