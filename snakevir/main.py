#!/usr/bin/env python3

# Module import
import rich_click as click
from pathlib import Path
from .function.edit_cluster import __edit_cluster
from .function.install import __install
from .function.make_config import __make_config
from .function.run import __run

version = Path(__file__).parent.resolve().joinpath("VERSION").open("r").readline().strip()

click.rich_click.COMMAND_GROUPS = {
    "snakevir": [
        {
            "name": "Install",
            "commands": ["install_cluster", "make_config", "edit_cluster"],
        },
        {
            "name": "Run snakevir workflow",
            "commands": ["run"],
        },
    ]
}

@click.group(name=f"snakevir", invoke_without_command=True, no_args_is_help=True)
@click.version_option(version)
def main():
    """
    Documentation :  https://snakevir.readthedocs.io/en/latest/
    """

@click.command("install_cluster", short_help=f'Install snakevir on HPC cluster',
               context_settings=dict(max_content_width=800))
@click.option('--path', '-p',type=click.Path(exists=True, resolve_path=True), required=True,
              help="Give the installation PATH for conda environment that contains all the necessary tools for snakevir.")
@click.option('--skip', '-s', is_flag=True,
              help="Skip all install and download if it's already existing")
@click.option('--tool', '-t', is_flag=True,
              help=" Update conda environment (Re-install conda environment even if it's already install)")
@click.option('--database', '-d', is_flag=True,
              help="Update database (Re-download files even if it's already download)")
def install_cluster(path, tool, database, skip):
    """
    This function allow to install tools with conda and dowload database needed by snakevir except nt & nr database
    """
    __install(path, tool, database, skip)


click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.OPTION_GROUPS = {
    "snakevir make_config": [
        {
            "name": "Mandatory options",
            "options": ["--output"],
        },
        {
            "name": "PATH options",
            "options": ["--fastq", "--path_diamond_nr", "--path_blast_nt", "--host_genome"],
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
@click.command("make_config", short_help=f'Create config file at yaml format',
               context_settings=dict(max_content_width=800))
@click.option('--output', '-o', type=click.Path(resolve_path=True), required=True,
              help="Path of the output file with '.yaml' extension (config.yml needed for snakevir.")
@click.option('--name', '-n', default="RUN_NAME",
              help="Name of run (ex : HNXXXXXX)")
@click.option('--fastq', '-f',  default="/PATH/TO/FASTQ/DIRECTORY/", type=click.Path(resolve_path=True),
              help="Path to the fastq directory")
@click.option('--host_genome', '-g',  default="/PATH/TO/FASTA/GENOME/", type=click.Path(resolve_path=True),
              help="Path to the genome host at fasta format")
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
def make_config(name, fastq, r1, r2, ext, path_diamond_nr, path_blast_nt, a3, a5, output, host_genome):
    """
    The command make_config is used for create config fime at yaml format for snakevir. You have 2 choice, you can use arguement
    for write all information needed in config or you can only use some argument (-o is mandatory) and wirte in the file after
    the missing information.
    """
    __make_config(name, fastq, r1, r2, ext, path_diamond_nr, path_blast_nt, a3, a5, output, host_genome)

@click.command("edit_cluster", short_help=f'Create cluster config file',
               context_settings=dict(max_content_width=800))
@click.option('--partition', '-p', default="False", type=str,
              help="Name of the default partition.")
@click.option('--account', '-a',  default="False", type=str,
              help="Name of you're account for launch job in cluster")
@click.option('--edit', '-e', is_flag=True,
              help="Edit cluster config for less/more ressources")
def edit_cluster(partition, account, edit):
    """
    The command make_config is used for create config fime at yaml format for snakevir. You have 2 choice, you can use arguement
    for write all information needed in config or you can only use some argument (-o is mandatory) and wirte in the file after
    the missing information.
    """
    __edit_cluster(partition, account, edit)

@click.command("run", short_help=f'Create cluster config file',
               context_settings={"ignore_unknown_options": True,"max_content_width" : 800})
@click.option('--config', '-c',  type=str, required=True,
              help="Path of config file")
@click.argument('other_snakemake_option', nargs=-1, type=click.UNPROCESSED)
def run(config, other_snakemake_option):
    """
    Run the snbakevir workflow.
    """
    __run(config, other_snakemake_option)


if Path(f'{Path(__file__).resolve().parent}/install_files/.install').exists():
    main.add_command(run)

main.add_command(install_cluster)
main.add_command(make_config)
main.add_command(edit_cluster)

if __name__ == '__main__':
    main()
