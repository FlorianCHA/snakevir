#!/usr/bin/env python3

# Module import
import rich_click as click
from pathlib import Path
import sys
import subprocess

def create_directory(path):
    '''
    This function create a directory at path given if directory does'nt exist
    '''
    if not Path(f'{path}').exists():
        subprocess.run(f'mkdir {path}', shell=True, check=False, stdout=sys.stdout, stderr=sys.stderr)


def install_conda_env(path, install_path, force):
    '''
    This function take the path of you're installation (path) and the path of yml file fon conda env (install_path) and
    create the conda environment for snakevir workflow.The force argument allow to install even the conda env is already
    create.
    '''
    # Path to directory install
    path_conda = f'{path}/snakevir_env'
    # Command for conda installation of snakevire env
    cmd = f'conda env create --prefix {path_conda} -f {install_path}/snakevir_environment.yml'
    # If conda env already exist, check if we re-install it or no
    if Path(path_conda).exists():
        value = click.prompt(f'\nThe env "{path_conda}" already exists, do you want to re-install it ?',
                             type=click.Choice(['y', 'n']))
        if value == 'y' or force:
            command = f'conda env remove -p {path_conda}'
            subprocess.run(command, shell=True, check=False, stdout=sys.stdout, stderr=sys.stderr)
        # If no, the new command line is nothing.
        else:
            click.secho(f'\nThe conda env "{path_conda}" already exist, skip conda installation.\n',
                        fg='green', bold=True)
            cmd = ''
    # Launch command for install or do nothing
    if cmd != '':
        click.secho(f'\n* Installation of conda environment at "{path_conda}"\n', fg='green', bold=True)

    install_conda = subprocess.run(cmd, shell=True, check=False, stdout=sys.stdout, stderr=sys.stderr)
    if int(install_conda.returncode) != 0: # install_conda.returncode !=0 means that they have error in installation
        click.secho('')
        click.secho(f'Error : They have some problems with conda env installation.', fg='white', bg='red', bold=True)
        click.secho('')
        sys.exit(1)



@click.command("install_cluster", short_help=f'Install snakevir on HPC cluster',
               context_settings=dict(max_content_width=800))
@click.option('--path', '-p',type=click.Path(exists=True, resolve_path=True),
              prompt='Choose your PATH for conda environment installation', required=True,
              help="Give the installation PATH for conda environment that contains all the necessary tools for snakevir.")
@click.option('--force', '-f', is_flag=True,
              help="If you use this option, you install conda environment even if it's already install")
def install(path,force):
    # Path to install file
    install_path = f'{Path(__file__).resolve().parent.parent}/install_files'
    install_conda_env(path, install_path, force)

    #Install database
    # Check if conda env has been already create (we use diamond for upload database)
    if Path(f'{path}/snakevir_env').exists():
        path_database = f'{path}/database/'
        create_directory(path_database)
        cmd = f'cd {path_database}; {path}/snakevir_env/bin/perl ' \
              f'{path}/snakevir_env/bin/update_blastdb.pl --decompress --source ncbi --blastdb_version 5 nr'
        subprocess.run(cmd, shell=True, check=False, stdout=sys.stdout, stderr=sys.stderr)

if __name__ == '__main__':
    install()
