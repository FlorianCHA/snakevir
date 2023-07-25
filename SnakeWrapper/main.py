#!/usr/bin/env python3

# Module import
import rich_click as click
from pathlib import Path
from edit_cluster import function_edit_cluster
from install import function_install
from make_config import function_make_config

version = "1.0.0"

click.rich_click.COMMAND_GROUPS = {
    "main.py": [
        {
            "name": "Install",
            "commands": ["install_cluster", "make_config","edit_cluster"],
        },
        {
            "name": "Run snakevir workflow",
            "commands": ["run"],
        },
    ]
}

@click.group(name=f"snakevir", invoke_without_command=True, no_args_is_help=True)
@click.version_option(version, "-v", "--version", message="%(prog)s, version %(version)s")
@click.pass_context
def main_command(ctx):
    """
    """

@click.command("install_cluster", short_help=f'Install snakevir on HPC cluster',
               context_settings=dict(max_content_width=800))
@click.option('--path', '-p',type=click.Path(exists=True, resolve_path=True),
              prompt='Choose your PATH for conda environment installation', required=True,
              help="Give the installation PATH for conda environment that contains all the necessary tools for snakevir.")
@click.option('--skip', '-s', is_flag=True,
              help="Skip all install and download if it's already existing")
@click.option('--tool', '-t', is_flag=True,
              help=" Update conda environment (Re-install conda environment even if it's already install)")
@click.option('--database', '-d', is_flag=True,
              help="Update database (Re-download files even if it's already download)")
@click.option('--database', '-d', is_flag=True,
              help="Update database (Re-download files even if it's already download)")
def install(path, tool, database, skip):
    """
    This function allow to install tools with conda and dowload database needed by snakevir except nt & nr database
    """
    function_install(path, tool, database, skip)


click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.OPTION_GROUPS = {
    "main.py make_config": [
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
@click.command("make_config", short_help=f'Create config file at yaml format',
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
def make_config(name, fastq, r1, r2, ext, path_diamond_nr, path_blast_nt, a3, a5, output):
    """
    The command make_config is used for create config fime at yaml format for snakevir. You have 2 choice, you can use arguement
    for write all information needed in config or you can only use some argument (-o is mandatory) and wirte in the file after
    the missing information.
    """
    function_make_config(name, fastq, r1, r2, ext, path_diamond_nr, path_blast_nt, a3, a5, output)

@click.command("edit_cluster", short_help=f'Create cluster config file',
               context_settings=dict(max_content_width=800))
@click.option('--partition', '-p', default="False", type=str,
              help="Name of the default partition.")
def edit_cluster(partition):
    """
    The command make_config is used for create config fime at yaml format for snakevir. You have 2 choice, you can use arguement
    for write all information needed in config or you can only use some argument (-o is mandatory) and wirte in the file after
    the missing information.
    """
    function_edit_cluster(partition)

@click.command("run", short_help=f'Create cluster config file',
               context_settings=dict(max_content_width=800))
@click.option('--partition', '-p', default="False", type=str,
              help="Name of the default partition.")
def run(partition):
    """
    The command make_config is used for create config fime at yaml format for snakevir. You have 2 choice, you can use arguement
    for write all information needed in config or you can only use some argument (-o is mandatory) and wirte in the file after
    the missing information.
    """
    function_edit_cluster(partition)

if Path(f'{Path(__file__).resolve().parent.parent}/install_files/.install').exists():
    print('True')
    main_command.add_command(run)

main_command.add_command(install)
main_command.add_command(make_config)
main_command.add_command(edit_cluster)


if __name__ == '__main__':
    main_command()
