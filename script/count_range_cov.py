
import sys
import csv
import glob
import pandas as pd
from itertools import groupby



file=sys.argv[1]
fileout=sys.argv[2]

with open(file) as csvfile:
	count=pd.read_csv(csvfile)
	count['sum'] = count[list(count.iloc[:,2:].columns)].sum(axis=1)
	count=count[['contig', 'nuc_pos','sum']]
	count=count.sort_values(['contig', 'nuc_pos'], ascending=[True, True]) .reset_index(drop=True)
	col_sum_list = count['sum'].tolist()
liste_pos=[]

names=count['contig'].unique()
for names in names:
	indices = []
	df = count.loc[count.contig==names]
	col_sum_list = df['sum'].tolist()
	indexed_cross = enumerate(col_sum_list)
	key = lambda x: x[1] < 10
	for key, group in groupby(indexed_cross, key=key):
		if key:
			chunk = list(group)
			indices.append((chunk[0][0], chunk[-1][0]))  # extracting the indice
	for pos in indices:
		liste_pos.append([df.iat[pos[0],0],df.iat[pos[0],1],df.iat[pos[1],1]])

df = pd.DataFrame(liste_pos)
df.columns = ['contig', 'start','end']
df.to_csv(fileout, index=False,header=False)

