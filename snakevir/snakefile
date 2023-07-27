import re
import sys
import os
from os.path import join
import shutil


def message(mes):
    sys.stderr.write("|---- " + mes + "\n")

def errormes(mes):
    sys.stderr.write("| ERROR ----" + mes + "\n")

configfile : "config.yaml"
cconfigfile : "config.yaml"
datadir = config["fastq"]
scriptdir = config["Scripts"]
host_db = config["host_db"]
rRNA_bact=config["rRNA_bact"]
rRNA_host=config["rRNA_host"]
base_nr = config["base_nr"]
base_taxo = config["base_taxo"]
base_nt = config["base_nt"]
base_taxo_nt=config["base_taxo_nt"]
ext=config["ext"]
ext_R1=config["ext_R1"]
ext_R2=config["ext_R2"]
threads_default= config["threads_default"]
threads_Map_On_host= config["threads_Map_On_host"]
threads_Map_On_bacteria= config["threads_Map_On_bacteria"]
threads_Megahit_Assembly= config["threads_Megahit_Assembly"]
threads_Map_On_Assembly= config["threads_Map_On_Assembly"]
threads_Blast_contigs_on_nr= config["threads_Blast_contigs_on_nr"]
threads_Blast_contigs_on_nt= config["threads_Blast_contigs_on_nt"]

logclust  = os.getcwd()+"/logsclust/"

message(str(logclust))

READS, =  glob_wildcards(datadir+"{readfile}"+ext)
SAMPLES, = glob_wildcards(datadir+"{sample}"+ ext_R1+ext)


SNAKEMAKE_DIR = os.path.dirname(workflow.snakefile)
snakemake.utils.makedirs("cluster_log/")


NBSAMPLES = len(SAMPLES)
NBREADS = len(READS)
RUN = config["run"]
#message(str(READS))
message(str(NBSAMPLES)+" samples  will be analysed")
message(str(len(READS))+" fastq files  will be processed")
message("Run name: "+RUN)
if NBREADS != 2*NBSAMPLES:
    errormes("Please provide two reads file per sample")
    sys.exit()

rule final:
    input:
        expand("logs/logs_contaminent/Stats_contaminent_{smp}.txt", smp=SAMPLES),
        f"logs/logsAssembly/{RUN}_assembly_stats.txt",
        expand(f"logs/insert_size/{{smp}}_insert_size_metrics_{RUN}.txt", smp=SAMPLES),
        expand(f"logs/logs_coverage/{{smp}}_coverage_{RUN}.txt", smp=SAMPLES),
        f"Coverage/count_contigs_raw_{RUN}.csv",
        expand(f"logs/logs_coverage_raw/{{smp}}_coverage_{RUN}.txt", smp=SAMPLES),
        f"intergreted_vir_check_{RUN}.csv",
        f"results/hosts_lineage_{RUN}.csv",
        f"logs/stats_run_{RUN}.csv",
        f"{RUN}/results/range_10x_coverage.cov"

############################### Read processing #################################################
include: f"snakefiles/read_processing.snake"

############################### Read processing #################################################
include: f"snakefiles/assembly.snake"

############################ blast information & extract viral contig ###########################
include: f"snakefiles/map_on_assembly.snake"

############################ blast information & extract viral contig ###########################
include: f"snakefiles/blast_taxid.snake"

############################ Calculate depth for count table ####################################
include: f"snakefiles/depth.snake"


rule Create_logs_report:
    input:
        lin = rules.get_nt_lineage_from_taxids.output.lin,
        lineage = rules.complete_taxo.output.lineage,
        by_seq = rules.Join_seq_acc_taxo_nr.output.taxo,
        count_t = rules.Build_array_coverage_nr.output.by_seq
    output:
        "logs/stats_run_{RUN}.csv"
    params:
        files=datadir,
        ext=ext_R1+ext,
        script=scriptdir+"create_results_doc_new.py"
    shell:
        """
        python {params.script} {params.files} {ext_R1} {ext_R2} {ext} {RUN} {input.by_seq}   {input.lineage}    {input.count_t}  {output}
        """
