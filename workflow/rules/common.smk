from pathlib import Path


def parse_samplesheet(samples_tsv):
    samples_dic = {}
    with open(samples_tsv, 'r') as fin:
        header_line = fin.readline()
        header_fields = [f.strip() for f in header_line.split('\t')]
        assert header_fields == ['sample', 'fasta'], "Malformatted samplesheet"
        for line in fin:
            if line.startswith('#'):
                pass
            else:
                fields = [f.strip() for f in line.split('\t')]
                samples_dic[fields[0]] = fields[1]
    return samples_dic


def get_sample_fasta(wc):
    return samples_dic[wc.sample]


def collect_prediction_tsvs(wc):
    tsvs = []
    for tool in TOOLS:
        tool_tsv = "results/{}/{}/predictions.tsv".format(wc.sample, tool)
        tsvs.append(tool_tsv)
    return tsvs

# This doesn't work with the sif files
# Need to bind mount the data directory on the containers
# with --singularity-args "-B path/to/data_dir:/data"
# It is required to get taxonomy for wish though
DATA_DIR = Path(config.get("data_dir"))

# Set the taxa.sqlite db path
# Used in rule lca
if config.get('taxa_sqlite'):
    TAXA_SQLITE = Path(config.get('taxa_sqlite'))
else:
    TAXA_SQLITE= Path.home() / Path(".etetoolkit/taxa.sqlite")

samples_dic = parse_samplesheet(config.get('samplesheet'))

SAMPLES = list(samples_dic.keys())
TOOLS = [
        "vhulk",
        "rafah",
        "vhmnet",
        "wish",
        "htp",
        #"crispropendb"
        ]


rule split_multifasta:
    input:
        get_sample_fasta
    output:
        reflist = "results/{sample}/tmp/reflist.txt"
    log:
        "logs/{sample}/split_multifasta.log"
    params:
        genomes_dir = "results/{sample}/tmp/genomes",
        scrpt = srcdir("../scripts/split_multifasta.py")
    conda:
        "../envs/phap_utils.yaml"
    shell:
        "mkdir -p {params.genomes_dir} && "
        "python {params.scrpt} "
        "-i {input} "
        "-o {params.genomes_dir} "
        "--write-reflist &>{log}"

# Aggregate
rule collect_hosts:
    input:
        collect_prediction_tsvs
    output:
        sample_tsv = "results/{sample}/all_predictions.tsv"
    params:
        scrpt = srcdir("../scripts/cat_predictions.py")
    log:
        "logs/{sample}/cat_predictions.log"
    conda:
        "../envs/phap_utils.yaml"
    shell:
        "python {params.scrpt} "
        "-i {input} -o {output.sample_tsv} "
        "2>{log}"


rule lca:
    input:
        predictions_tsv = rules.collect_hosts.output.sample_tsv
    output:
        lca_tsv = "results/{sample}/lca.tsv"
    params:
        scrpt = srcdir("../scripts/get_lca.py"),
        taxa_sqlite = TAXA_SQLITE
    log:
        "logs/{sample}/get_lca.log"
    conda:
        "../envs/phap_utils.yaml"
    shell:
        "python {params.scrpt} "
        "-d {params.taxa_sqlite} "
        "-i {input.predictions_tsv} "
        "-o {output.lca_tsv} 2>{log}"

# Report
rule predictions_html:
    input:
        rules.collect_hosts.output.sample_tsv
    output:
        html = report("report/{sample}_all.html",
                caption="report/all_table.rst",
                category="{sample}"
                )

    params:
        scrpt = srcdir("../scripts/tsv_to_html.py")
    log:
        "logs/{sample}/predictions_html.log"
    conda:
        "../envs/phap_utils.yaml"
    shell:
        "python {params.scrpt} {input} {output.html} 2>{log}"


rule lca_html:
    input:
        rules.lca.output.lca_tsv
    output:
        html = report("report/{sample}_lca.html",
                caption="report/lca_table.rst",
                category="{sample}"
                )

    params:
        scrpt = srcdir("../scripts/tsv_to_html.py")
    log:
        "logs/{sample}/lca_html.log"
    conda:
        "../envs/phap_utils.yaml"
    shell:
        "python {params.scrpt} {input} {output.html} 2>{log}"


onsuccess:
        print(2*'\n' + '\t' + 76*'#')
        print('\n\tWorkflow finished successfully!\n')
        print('\t' + 76*'#')

        print('\t## CLEANUP ##\n')
        print('\tRemoving the per sample `tmp` directory...\n')
        shell('rm -rf results/*/tmp')
        print('\t' + 76*'#')

        print('\t## REPORT ## \n')
        print('\tA report with summary statistics for the execution of the ')
        print('\tpipeline and aggregated results per sample can be created '\
            'with\n')
        print('\t\t$ snakemake -j2 --report phap.html\n')
        print('\tYou can view the resulting phap.html report with any ')
        print('\tbrowser.\n')

#rule size_filter:
#    input:
#        multifasta_fp = get_sample_fasta
#    output:
#        filtered_fasta = "results/{sample}/tmp/filtered.fa.gz"
#    threads: 4
#    log:
#        "logs/{sample}/size_filter.log"
#    params:
#        min_size = 5000
#    shell:
#        "seqkit seq -g -j {threads} -m {params.min_size} "
#        "{input.multifasta_fp} | gzip -c >{output.filtered_fasta} 2>{log}"
