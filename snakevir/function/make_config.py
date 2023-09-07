#!/usr/bin/env python3

# Module import
from pathlib import Path

def __make_config(name, fastq, r1, r2, ext, path_diamond_nr, path_blast_nt, a3, a5, output, host_genome):
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
            if line.startswith("host_genome:"):
                line = f"host_genome: {host_genome}\n"
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
