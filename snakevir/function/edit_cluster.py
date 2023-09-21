#!/usr/bin/env python3

# Module import
import rich_click as click
from pathlib import Path


def __edit_cluster(partition, account, edit):
    """
    The command make_config is used for create config fime at yaml format for snakevir. You have 2 choice, you can use arguement
    for write all information needed in config or you can only use some argument (-o is mandatory) and wirte in the file after
    the missing information.
    """
    # Path to install file (directory which contain the default config file
    install_path = f'{Path(__file__).resolve().parent.parent}/install_files'
    # Change partition names
    new_cluster = list()
    with open(f'{install_path}/cluster.yaml', 'r') as cluster_file:
        for line in cluster_file:
            if line.strip().startswith("partition:"):
                old_partition = line.strip().split(':')[-1].strip()
                line = line.replace(old_partition,partition)
            if line.strip().startswith("account:"):
                old_account = line.strip().split(':')[-1].strip()
                line = line.replace(old_account,account)
            new_cluster.append(line)

    with open(f'{install_path}/cluster.yaml', 'w') as new_file:
        new_file.write("".join(new_cluster))

    # Open editor to modify ressources
    if edit:
        click.edit(require_save=True, extension='.yaml', filename=f'{install_path}/cluster.yaml')

    # Check account (with groups shell command)
    available_account = subprocess.check_output("groups", shell=True).decode("utf8").strip().split()
    if account not in available_account:
        raise click.secho(
            f"ERROR: You'r account '{account}' doesn't exist, please check you're account.",
            fg='red', bold=True, err=True)

    available_partition = subprocess.check_output(r"""sinfo -s | cut -d" " -f1""", shell=True).decode("utf8").strip().replace('*','').split("\n")[1:]
    if partition not in available_partition:
        raise click.secho(
            f"ERROR: You'r partition '{partition}' doesn't exist in this cluster , please check the partition available with sinfo command.",
            fg='red', bold=True, err=True)