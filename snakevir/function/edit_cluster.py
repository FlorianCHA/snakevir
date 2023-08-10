#!/usr/bin/env python3

# Module import
import rich_click as click
from pathlib import Path


def __edit_cluster(partition):
    """
    The command make_config is used for create config fime at yaml format for snakevir. You have 2 choice, you can use arguement
    for write all information needed in config or you can only use some argument (-o is mandatory) and wirte in the file after
    the missing information.
    """
    # Path to install file (directory which contain the default config file
    install_path = f'{Path(__file__).resolve().parent.parent}/install_files'
    # Change partition name
    if partition != "False":
        new_cluster = list()
        with open(f'{install_path}/cluster.yaml', 'r') as cluster_file:
            for line in cluster_file:
                if line.strip().startswith("partition:"):
                    old_partition = line.strip().split(':')[-1].strip()
                    line = line.replace(old_partition,partition)
                new_cluster.append(line)

        with open(f'{install_path}/cluster.yaml', 'w') as new_file:
            new_file.write("".join(new_cluster))

    # Open editor to modify ressources
    click.edit(require_save=True, extension='.yaml', filename=f'{install_path}/cluster.yaml')
