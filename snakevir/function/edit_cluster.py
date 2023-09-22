#!/usr/bin/env python3

# Module import
import rich_click as click
from pathlib import Path
import subprocess
from collections import defaultdict
# import pyyaml module
import yaml

def __edit_cluster(partition, account, edit):
    """
    The command make_config is used for create config fime at yaml format for snakevir. You have 2 choice, you can use arguement
    for write all information needed in config or you can only use some argument (-o is mandatory) and wirte in the file after
    the missing information.
    """
    # Path to install file (directory which contain the default config file
    install_path = f'{Path(__file__).resolve().parent.parent}/install_files'
    # Change partition & account names
    new_cluster = list()
    with open(f'{install_path}/cluster.yaml', 'r') as cluster_file:
        for line in cluster_file:
            if line.strip().startswith("partition:"):
                if partition == "False": # Check if partition is give by user or not
                    partition_default = line.strip().split(':')[-1].strip() # Retrieve partition from config if partition is not provide by user
                else :
                    old_partition = line.strip().split(':')[-1].strip()
                    line = line.replace(old_partition,partition)
            if line.strip().startswith("account:") :
                if account == "False": # Check if account is give by user or not
                    account_default = line.strip().split(':')[-1].strip() # Retrieve account from config if account is not provide by user
                else :
                    old_account = line.strip().split(':')[-1].strip()
                    line = line.replace(old_account,account)
            new_cluster.append(line)

    with open(f'{install_path}/cluster.yaml', 'w') as new_file:
        new_file.write("".join(new_cluster))

    # Open editor to modify ressources
    if edit:
        click.edit(require_save=True, extension='.yaml', filename=f'{install_path}/cluster.yaml')

    # Check parititon & account in config file after editing
    partition_default = defaultdict(list) # For check all parition for each rules.
    account_default = defaultdict(list) # For check all account for each rules.

    with open(f'{install_path}/cluster.yaml') as f:
        data = yaml.safe_load(f)
    for rule in data:
        if "partition" in data[rule]:
            partition_rule = data[rule]["partition"]
            partition_default[partition_rule].append(rule)
    for rule in data:
        if "account" in data[rule]:
            account_rule = data[rule]["account"]
            account_default[account_rule].append(rule)

    # Check account (with groups shell command)
    available_account = subprocess.check_output("groups", shell=True).decode("utf8").strip().split()
    for account in account_default:
        if account not in available_account:
            txt_rule = ", ".join(partition_default[account])
            raise click.secho(
                f"ERROR: You'r account '{account_default}' for {txt_rule} doesn't exist, please check you're account.",
                fg='red', bold=True, err=True)

    # Check partition (with sinfo shell command)
    available_partition = subprocess.check_output(r"""sinfo -s | cut -d" " -f1""", shell=True).decode("utf8").strip().replace('*','').split("\n")[1:]
    for partition in partition_default:
        if partition not in available_partition:
            txt_rule = ", ".join(partition_default[partition])
            raise click.secho(
                f"ERROR: You'r partition '{partition}' for rule '{txt_rule}' doesn't exist in this cluster , please check the partition available with sinfo command.",
                fg='red', bold=True, err=True)
