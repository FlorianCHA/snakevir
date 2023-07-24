#!/usr/bin/env python3

# Module import
import rich_click as click
from pathlib import Path
import sys
import subprocess
import yaml
### Decorative code for argument parser ###
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.OPTION_GROUPS = {
    "make_config.py": [
        {
            "name": "Mandatory options",
            "options": ["--output"],
        },
        {
            "name": "PATH options",
            "options": ["--fastq", "--path_diamond_nr", "--path_blast_nt"],
        },
        {
            "name": "Advanced options",
            "options": ["--name", "--R1", "--R2", "--ext"],
        },
        {
            "name": "Adpater options",
            "options": ["--A3", "--A5"],
        },
    ]
}


@click.command("make_config", short_help=f'Create config file at yaml format for snakevir',
               context_settings=dict(max_content_width=800))
@click.option('--output', '-o', type=click.Path(resolve_path=True), required=True,
              help="Path of the output file with '.yaml' extension (config.yml needed for snakevir.")
@click.option('--name', '-n', default="RUN_NAME",
              help="Name of run (ex : HNXXXXXX)")
@click.option('--fastq', '-f',  default="/PATH/TO/FASTQ/DIRECTORY/", type=click.Path(resolve_path=True),
              help="Path to the fastq directory")
@click.option('--r1', default="_1", show_default=True,
              help="Type of your R1 fastq files contains in FASTQ directory (for exemple : '_R1' or '_1', etc. )")
@click.option('--r2', default="_2", show_default=True,
              help="Type of your R2 fastq files contains in FASTQ directory (for exemple : '_R2' or '_2', etc. )")
@click.option('--ext', default=".fastq.gz", show_default=True,
              help=" Etension of your reads files in the FASTQ directory (for exemple : '.fastq.gz' or '.fq', etc.)")
@click.option('--path_diamond_nr', default="/PATH/TO/DIAMOND/NR/DATABASE", type=click.Path(resolve_path=True),
              help="Path to the diamond nr database")
@click.option('--path_blast_nt', default="/PATH/TO/BLAST/NT/DATABASE", type=click.Path(resolve_path=True),
              help="Path to the blast nt database")
@click.option('--A3', default="CAGCGGACGCCTATGTGATG", show_default=True,
              help="Sequence of Adapter in 3'")
@click.option('--A5', default="CATCACATAGGCGTCCGCTG", show_default=True,
              help="Sequence of Adapter in 5'")
def install(name, fastq, r1, r2, ext, path_diamond_nr, path_blast_nt, a3, a5, output):
    """
    The command make_config is used for create config fime at yaml format for snakevir. You have 2 choice, you can use arguement
    for write all information needed in config or you can only use some argument (-o is mandatory) and wirte in the file after
    the missing information.
    """
    # Path to install file (directory which contain the default config file
    install_path = f'{Path(__file__).resolve().parent.parent}/install_files'
    new_config = list()
    with open(f'{install_path}/config.yaml', 'r') as config_file:
        for line in config_file:
            if line.startswith("run:"):
                line = f"run: {name}\n"
            if line.startswith("fastq:"):
                line = f"fastq: {fastq}\n"
            if line.startswith("ext_R1:"):
                line = f"ext_R1: {r1}\n"
            if line.startswith("ext_R2:"):
                line = f"ext_R2: {r2}\n"
            if line.startswith("ext:"):
                line = f"ext: {ext}\n"
            if line.startswith("base_nr:"):
                line = f"base_nr: {path_diamond_nr}\n"
            if line.startswith("base_nt:"):
                line = f"base_nt: {path_blast_nt}\n"
            if line.startswith("A3:" ):
                line = f"A3: {a3}\n"
            if line.startswith("A5:"):
                line = f"A5: {a5}\n"
            new_config.append(line)

    with open(f'{output}', 'w') as new_file:
        new_file.write("".join(new_config))

if __name__ == '__main__':
    install()
