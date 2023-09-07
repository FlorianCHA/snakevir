import sys
import csv
import glob
import pandas as pd
from functools import reduce
import gc
import os, re
import psutil
columns = []
data = {}
ids = set()
df=pd.DataFrame()
nb = 0
for subdir, dirs, files in os.walk(sys.argv[1]):
	for filename in files:
		filepath = subdir + os.sep + filename
		if filename.endswith(".cov") and sys.argv[2] in filename[0:2]:
			nb += 1
			print(filename, nb)
			key = filename.rstrip(".cov")
			with open(filepath) as tsvfile:
				f = pd.read_csv(tsvfile, delimiter="\t", names=["contig", "nuc_pos", key])
				print(f)
				if df.empty:
					df=f
				else:
					df=df.merge(f, how='outer', on=['contig','nuc_pos'])
					print(round(psutil.virtual_memory().used / psutil.virtual_memory().total *100,2))
					df = df.fillna(0).drop_duplicates()
				del f
				gc.collect()

df.to_csv(sys.argv[3], index=False)

def merge_dataframe(subdir, type_file, output):
	"""
	"""
	liste_file = [elt for elt in os.listdir('split_cont/') if type_file in elt]
	liste_panda = [pd.read_csv(f'{subdir}/{file}', delimiter="\t", names=["contig", "nuc_pos", file.rstrip('.cov')]) for file in liste_file]
	df = reduce(lambda df1, df2: pd.merge(df1, df2, how='outer', on=['contig', 'nuc_pos']), liste_panda)
	df = df.fillna(0).drop_duplicates()
	df.to_csv(output, index=False)

# merge_dataframe(sys.argv[1], sys.argv[2], sys.argv[3])

#for subdir, dirs, files in os.walk(sys.argv[1]):
#	for filename in files:
#		filepath = subdir + os.sep + filename
#		if filepath.endswith(".cov"):
#			print(filename)
#			key = filename.rstrip("_on_nova_bat.bam.cov")
#			with open(filepath) as tsvfile:
#				f = pd.read_csv(tsvfile, delimiter="\t", names=["contig", "nuc_pos", key])
#				if df.empty:
#					df=f
#				else:
#					df=df.merge(f, how='outer', on=['contig','nuc_pos'])
#				del f
#				gc.collect()
#df = df.fillna(0).drop_duplicates()

#
