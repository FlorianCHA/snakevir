import sys, os
from ete3 import NCBITaxa
from collections import Counter
import pandas as pd
import csv
import subprocess
import numpy as np


file=sys.argv[1]
fileout=sys.argv[2]
cov = pd.read_csv(file)
cov['sum'] = cov.iloc[:, 2:].sum(axis=1)

cov1=cov.groupby("contig").agg(
        min_coverage=pd.NamedAgg(column='sum', aggfunc='min'),
        max_coverage=pd.NamedAgg(column='sum', aggfunc='max'),
        mean_coverage=pd.NamedAgg(column='sum', aggfunc=np.mean),
        median_coverage=pd.NamedAgg(column='sum', aggfunc=np.median)
)

cov1.to_csv(fileout, sep=',', index=True,header=False)
