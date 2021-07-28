rule run_vhmnet:
    input:
        reflist = rules.split_multifasta.output.reflist,
    output:
        done = touch("results/{sample}/vhmnet/.done.txt")
    params:
        # use it with
        # snakemake --singularity-args "-B /path/to/data/:/data" ...
        data_dir = "/data",
        tmp_dir = "results/{sample}/vhmnet/tmp",
        output_dir = "results/{sample}/vhmnet",
        fasta_dir = "results/{sample}/tmp/genomes",
        short_contig = "--short-contig"
            if config['vhmnet']['short_contig'] else ''
    threads:
        config['vhmnet'].get('threads', 12)
    container:
        config['vhmnet'].get('container')
    log:
        "logs/{sample}/vhmnet.log"
    shell:
        "VirHostMatcher-Net.py -q {params.fasta_dir} "
        "-t {threads} "
        "{params.short_contig} "
        "-i {params.tmp_dir} "
        "-d {params.data_dir} "
        "-q {params.fasta_dir} "
        "-o {params.output_dir} "
        "&>{log}"

rule process_vhmnet:
    input:
        rules.run_vhmnet.output.done
    output:
        vhmnet_tsv = "results/{sample}/vhmnet/predictions.tsv"
    params:
        predictions_dir = "./results/{sample}/vhmnet/predictions"
    shell:
        """
        for f in $(find -wholename "{params.predictions_dir}/*.csv" -type f);
        do
            contig_id=$(basename ${{f}} | sed -e 's/_prediction.csv//')
            host_score=$(tail -n1 ${{f}} | cut -f8,10 -d',' | tr ',' '\t')
            echo -e "$contig_id\t$host_score" >> {output.vhmnet_tsv}.tmp;
        done
        sort -k1 {output.vhmnet_tsv}.tmp > {output.vhmnet_tsv}
        rm -f {output.vhmnet_tsv}.tmp
        """

