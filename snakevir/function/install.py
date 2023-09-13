#!/usr/bin/env python3

# Module import
import rich_click as click
from pathlib import Path
import sys
import subprocess
from cookiecutter.main import cookiecutter

def create_directory(path):
    '''
    This function create a directory at path given if directory does'nt exist
    '''
    if not Path(f'{path}').exists():
        subprocess.run(f'mkdir {path}', shell=True, check=False, stdout=sys.stdout, stderr=sys.stderr)

def download(file,command, database, skip):
    """
    This function check if file already exist or not and ask at user if re-download is needed.
    """
    value = ""
    # Chek if file already exist
    if Path(file).exists() and not database:
        # Check if we need to skip this function
        if skip:
            return (f"{Path(file).name}")
        # Ask at user if we need to re-download file
        value = click.prompt(f'\nThe file {Path(file).name} already exists, do you want to re-download it ?',
                             type=click.Choice(['y', 'n']))
    # Launch download if file doesn't exist or user want to re-download.
    if not Path(f'{file}').exists() or value == "y" or database:
        subprocess.run(command, shell=True, check=False, stdout=sys.stdout, stderr=sys.stderr)
    else:
        return (f"{Path(file).name}")

def install_conda_env(path, install_path, tool, skip):
    '''
    This function take the path of you're installation (path) and the path of yml file fon conda env (install_path) and
    create the conda environment for snakevir workflow.The force argument allow to install even the conda env is already
    create.
    '''
    # Check if we need to skip this function
    # Path to directory install
    path_conda = f'{path}/snakevir_env'
    # Command for conda installation of snakevire env
    cmd = f'mamba env create --prefix {path_conda} -f {install_path}/snakevir_environment.yml'
    # If conda env already exist, check if we re-install it or no
    if Path(path_conda).exists():
        # Check if we need to skip this function
        if skip:
            click.secho(f'\nThe conda env "{Path(path_conda).stem}" already exist, skip conda installation.\n', fg='green', bold=True)
            return()
        if not tool:
            value = click.prompt(f'\nThe env "{path_conda}" already exists, do you want to re-install it ?',
                             type=click.Choice(['y', 'n']))
        else:
            value = "y"
        if value == 'y':
            command = f'mamba env remove -p {path_conda}'
            subprocess.run(command, shell=True, check=False, stdout=sys.stdout, stderr=sys.stderr)
        # If no, the new command line is nothing.
        else:
            click.secho(f'\nThe conda env "{Path(path_conda).stem}" already exist, skip conda installation.\n',
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

def install_database(path, database_path, install_path, database, skip):
    '''
     This function take the path of you're installation (path) and the path of the directory install_path and
     install all database needed by snakevir except diamond nr and nt database.
     '''
    # Check if conda env has been already create (we use diamond for upload database)
    if Path(f'{path}/snakevir_env').exists():
        create_directory(database_path)
        # Download accession2taxid
        list_skip = list() # Init list which contain all fils skiped
        ## for nucleotide
        command = f'wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz -O {database_path}nucl_gb.accession2taxid.gz;' \
                  f'gunzip {database_path}nucl_gb.accession2taxid.gz'
        list_skip.append(download(f'{database_path}nucl_gb.accession2taxid',command, database, skip))
        ## for portein
        command = f'wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz -O {database_path}prot.accession2taxid.gz;' \
                  f'gunzip {database_path}prot.accession2taxid.gz'
        list_skip.append(download(f'{database_path}prot.accession2taxid', command, database, skip))
        # Donwload virust host database
        command = f'wget https://www.genome.jp/ftp/db/virushostdb/virushostdb.tsv -O {database_path}virushostdb.tsv'
        list_skip.append(download(f'{database_path}virushostdb.tsv', command, database, skip))
        # Prepare silva database
        command = f'echo "\n\t* Extract Archive";' \
                  f'wget https://github.com/FlorianCHA/snakevir/raw/master/snakevir/install_files/silva_db.tar.gz -O {database_path}silva_db.tar.gz;' \
                  f'tar zxvf {database_path}silva_db.tar.gz -C {database_path} > stdout;' \
                  f'gunzip {database_path}silva_db/*.fasta.gz;' \
                  f'echo "\t* Create index for bwa tools";' \
                  f'for fasta in {database_path}silva_db/*.fasta; do {path}/snakevir_env/bin/bwa index $fasta 1> stdout 2> stdout;done;' \
                  f'rm stdout {database_path}silva_db.tar.gz'
        list_skip.append(download(f'{database_path}silva_db/silva_138.1_bacteria.fasta.amb', command, database, skip))

        # Check if some files aren't download because they already exist
        if len([file_skiped for file_skiped in list_skip if file_skiped != None]) != 0:
            click.secho(f'\nSome file already exist, skip this file for download : \n', fg='green', bold=True)
            for file_skiped in list_skip:
                # Skipe None value from re-download file
                if file_skiped != None:
                    click.secho(f'\t* {file_skiped}\n', fg='green', bold=True)

def config_yml(path, database_path, install_path):
    """
    This function modify config.yaml with path of database install by install_database fuction
    """
    new_config = list()
    with open(f'{install_path}/config.yaml', 'r') as config:
        for line in config:
            if "rRNA_bact:" in line :
                line = f'rRNA_bact: "{database_path}silva_db/silva_138.1_bacteria.fasta"\n'
            if "rRNA_host:" in line:
                line = f'rRNA_host: "{database_path}silva_db/silva_138.1_insecta.fasta"\n'
            if "base_taxo:" in line:
                line = f'base_taxo: "{database_path}prot.accession2taxid"\n'
            if "base_taxo_nt:" in line:
                line = f'base_taxo_nt: "{database_path}nucl_gb.accession2taxid"\n'
            if "host_db:" in line:
                line = f'host_db: "{database_path}virushostdb.tsv"\n'
            if "Scripts:" in line:
                line = f'Scripts: "{Path(__file__).resolve().parent.parent}/script/"\n'
            if "module_file:" in line:
                line = f'module_file: "{path}/snakevir_module"\n'
            new_config.append(line)

    with open(f'{install_path}/config.yaml', 'w') as new_file:
        new_file.write("".join(new_config))

def module_file(path,install_path):
    """
    This function create module file for conda env
    """
    new_module = list()
    with open(f'{install_path}/snakevir_module','r') as module_file:
        for line in module_file:
            if "prepend-path PATH" in line:
                line = f"prepend-path PATH {path}/snakevir_env/bin\n"
            if "prepend-path LD_LIBRARY_PATH" in line:
                line = f"prepend-path LD_LIBRARY_PATH {path}/snakevir_env/lib\n"
            if "prepend-path CPATH" in line:
                line = f"prepend-path CPATH {path}/snakevir_env/include"
            new_module.append(line)

    with open(f'{path}/snakevir_module', 'w') as new_file:
        new_file.write("".join(new_module))

def __install(path, tool, database, skip):
    """
    This function allow to install tools with conda and download database needed by snakevir except nt & nr database
    """
    ### Install tools ###
    # Path to install file
    install_path = f'{Path(__file__).resolve().parent.parent}/install_files'
    # Function that install all tools with conda
    install_conda_env(path, install_path, tool, skip)

    ### Install database ###
    # Path to database file
    database_path = f'{path}/database/'
    install_database(path, database_path, install_path, database, skip)

    ### Create module file for cluster ###
    module_file(path,install_path)

    ### Modify config.yaml ###
    config_yml(path, database_path, install_path)

    ### Create profile for slurm cluster ###
    cookiecutter(template = f'https://github.com/Snakemake-Profiles/slurm.git',
                 no_input=True,
                 extra_context={ "sbatch_defaults": "--export=ALL",
                                "cluster_config": f"{install_path}/cluster.yaml",
                                },
                 overwrite_if_exists=True,
                 output_dir=f'{install_path}/profile/',
                 skip_if_file_exists=True)
    add_config_slurm = 'cluster-cancel: "scancel"\n' \
                       'restart-times: 0\n' \
                       'jobscript: "slurm-jobscript.sh"\n' \
                       'cluster: "slurm-submit.py"\n' \
                       'cluster-status: "slurm-status.py"\n' \
                       'max-jobs-per-second: 1\n' \
                       'max-status-checks-per-second: 10\n' \
                       'local-cores: 1\n' \
                       'jobs: 200\n' \
                       'use-envmodules: true\n' \
                       'latency-wait: 1296000\n' \
                       'printshellcmds: true'
    with open(f'{install_path}/profile/slurm/config.yaml', 'w') as f:
        f.write(add_config_slurm)

    ### Write file for verif installation in main command ###
    with open(f'{install_path}/.install',"w") as f:
        f.write('DONE')

