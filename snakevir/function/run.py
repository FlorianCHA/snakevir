#!/usr/bin/env python3

# Module import
import rich_click as click
from pathlib import Path
import subprocess
import sys
# import pyyaml module
import yaml


def verif_config(config):
    '''
    This function check each variable give by user in config.yaml
    '''
    ### Open the file and load the file (return a dict) ###
    try:  # Check if config is at yaml format.
        with open(config) as f:
            data = yaml.safe_load(f)
    except:  # If not at yaml format return a error.
        click.secho(f"ERROR: you'r config file {config} is not at Yaml format, please check it.", fg='red', bold=True, err=True)
        exit()

    ### Check fastq directory ###
    # Check if is a directory
    directory_fastq = Path(data['fastq'])
    if not directory_fastq.is_dir():
        click.secho(f"ERROR: You'r fastq directory {directory_fastq} is not a directory, please check it.", fg='red', bold=True, err=True)
        exit()
    # Check if they have fastq (with ext_R1 and ext) and if number R1 = number R2
    nb_R1 = len(sorted(directory_fastq.rglob(f'*{data["ext_R1"]}{data["ext"]}')))
    nb_R2 = len(sorted(directory_fastq.rglob(f'*{data["ext_R2"]}{data["ext"]}')))
    if nb_R1 == 0:
        click.secho(f"ERROR: You'r fastq directory {directory_fastq} doesn't contains fasta with '{data['ext_R1']}{data['ext']}' or '{data['ext_R2']}{data['ext']}' extension",
            fg='red', bold=True, err=True)
        exit()
    elif nb_R1 != nb_R2:
        click.secho(
            f"ERROR: You'r fastq directory {directory_fastq} doesn't two reads file per sample, please check it",
            fg='red', bold=True, err=True)
        exit()

    ### Check path_diamond ###
    # Check if file exist ( name* )
    diamond_nr = Path(data['base_nr'])
    diamond_directory = diamond_nr.parent
    name_database = diamond_nr.name
    # Count file from diamond database give by user
    nb_file = len(sorted(diamond_directory.rglob(f'{name_database}*')))
    # Check if they have at least 1 file in database
    if nb_file == 0:
        click.secho(
            f"ERROR: You'r diamond nr database '{diamond_nr}' doesn't exist, please check you're path",
            fg='red', bold=True, err=True)
        exit()

    ### Check blast nr path ###
    blast_nt = Path(data['base_nt'])
    blast_directory = blast_nt.parent
    name_database = blast_nt.name
    # Count file from diamond database give by user
    nb_file = len(sorted(blast_directory.rglob(f'{name_database}*')))
    # Check if they have at least 8 file in database ( 8 extension of makeblastdn) here name* , for name.00, name .01 of makeblastdb output
    if nb_file < 8:
        raise click.secho(
            f"ERROR: You'r blast nt database '{blast_nt}' doesn't exist, please check you're path",
            fg='red', bold=True, err=True)

def __run(config, add_option):
    """
    Run the snbakevir workflow.
    """
    path_snakevir = Path(__file__).resolve().parent.parent
    verif_config(config)
    add_option = " ".join(add_option)
    cmd = f"snakemake  -s {path_snakevir}/snakefile --configfile {config} --profile {path_snakevir}/install_files/profile/slurm --cluster-config {path_snakevir}/install_files/cluster.yaml --show-failed-logs {add_option}"
    process = subprocess.run(cmd, shell=True, check=False, stdout=sys.stdout, stderr=sys.stderr)
    if int(process.returncode) >= 1:
        raise

if __name__ == '__main__':
    __run()
