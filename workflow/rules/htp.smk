rule run_htp:
    input:
        reflist = rules.split_multifasta.output.reflist
    output:
        htp_raw = "results/{sample}/htp/raw.txt"
    log:
        stderr = "logs/{sample}/htp.stderr"
    params:
        fasta_dir = "./results/{sample}/tmp/genomes",
        classifier = config['htp'].get('classifier')
    container:
        config['htp'].get('container',
                "library://papanikos_182/default/htp:1.0.2")
    shell:
        """
        printf "contig\traw_pred\n" > {output.htp_raw}
        for f in $(find {params.fasta_dir} -wholename "*.fasta");
        do
            contig_id=$(basename ${{f}} | sed -e 's/\.fasta//' )
            pred=$(viruses_classifier \
                    --classifier {params.classifier} \
                    --nucleic_acid dna \
                    -p ${{f}} 2>{log.stderr})
            echo -e $contig_id\t$pred >> {output.htp_raw}
        done
        """

rule process_htp:
    input:
        htp_raw = rules.run_htp.output.htp_raw
    output:
        predictions_tsv = "results/{sample}/htp/predictions.tsv"
    params:
        ob = "{"
    log:
        "logs/{sample}/process_htp.log"
    conda:
        "../envs/phap_utils.yaml"
    shell:
        """
        tail -n +2 results/{wildcards.sample}/htp/raw.txt | cut -f1 -d','| \
                sed -r "s/ \{params.ob}'phage'\: /\t/" | sort -k1 \
                >{output.predictions_tsv} 2>{log}
        """

