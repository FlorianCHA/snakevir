.. contents:: Table of Contents
   :depth: 2
   :backlinks: entry

How to create a workflow
========================

Snakevir allows you to build a workflow using a simple ``config.yaml`` configuration file.

To create this file, just run:

.. click:: culebrONT.main:make_config
    :prog: culebrONT make_config
    :show-nested:

If you didn't use the command for complete your config file, you can edit your config file :

Edit config file
----------------

1. Analysis name
~~~~~~~~~~~~~~~~

First, give a name at your analysis

.. code-block:: YAML

   DATA:
       run: 'HNXXXXXX'

2. Fastq params
~~~~~~~~~~~~~~~~

Then, indicate the data path and extension for fastq data :

.. code-block:: YAML

   DATA:
       fastq: '/path/to/fastq/directory/'
       ext_R1: "_1"
       ext_R2: "_2"
       ext: ".fastq.gz"

3. Database path
~~~~~~~~~~~~~~~~

Indicate the database path for diamond and blast:

.. code-block:: YAML

   DATA:
       base_nr: "/PATH/TO/DIAMOND/NR/DATABASE"
       base_nt: "/PATH/TO/NT/DATABASXE"


Summary table
-------------

Find here a summary table with the description of each data needed to run snakevir :

.. csv-table::
    :header: "Input", "Description"
    :widths: auto

    "run", "A name for the run."
    "fastq", "Path to the fastq directory which contains the paired fastq for each sample."
    "ext_R1","Type of your R1 fastq files contains in FASTQ directory (for exemple : '_R1' or '_1', etc.)."
    "ext_R2", "Type of your R2 fastq files contains in FASTQ directory (for exemple : '_R2' or '_2', etc.)."
    "ext"," Etension of your reads files in the FASTQ directory (for exemple : '.fastq.gz' or '.fq', etc.)."
    "base_nr"," Path of the Diamond specific protein database built from NCBI nr database."
    "base_nt","Path of the blast specific protein database built from NCBI nt database."

------------------------------------------------------------------------

How to run the workflow
=======================

Before attempting to run snakevir, please verify that you have already modified the ``config.yaml`` file as explained in :ref:`Edit config file`.

If you installed snakevir and create the config file, you can now run:


.. click:: culebrONT.main:run
    :prog: culebrONT run
    :show-nested:

------------------------------------------------------------------------


Output on CulebrONT
===================

To modify.

.. code-block:: bash

    OUTPUT_CULEBRONT_CIRCULAR/
    ├── SAMPLE-1
    │   ├── AGGREGATED_QC
    │   │   ├── DATA
    │   │   ├── MAUVE_ALIGN
    │   │   └── QUAST_RESULTS
    │   ├── ASSEMBLERS
    │   │   ├── CANU
    │   │   │   ├── ASSEMBLER
    │   │   │   ├── CORRECTION
    │   │   │   ├── FIXSTART
    │   │   │   ├── POLISHING
    │   │   │   └── QUALITY
    │   │   ├── FLYE
    │   │   │   ├── ...
    │   │   ├── MINIASM
    │   │   │   ├── ...
    │   │   ├── RAVEN
    │   │   │   ├── ...
    │   │   ├── SHASTA
    │   │   │   ├── ...
    │   │   └── SMARTDENOVO
    │   │   │   ├── ...
    │   ├── DIVERS
    │   │   └── FASTQ2FASTA
    │   ├── LOGS
    │   └── REPORT
    └── FINAL_REPORT
    ├── SAMPLE-2 ...


Report
======

To add.

