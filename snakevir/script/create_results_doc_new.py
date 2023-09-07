import sys, os
from collections import Counter
import pandas as pd
import csv
from os.path import exists
import glob
import numpy as np
# import pandas as pd
# import locale
# locale.setlocale(locale.LC_ALL, '')
path_files=os.listdir(sys.argv[1])
ext1=sys.argv[2]
ext2=sys.argv[3]
ext_file=sys.argv[4]
run=sys.argv[5]
out=sys.argv[9]
output_directory=sys.argv[10]

stats_df=pd.read_csv(sys.argv[6], sep=',').drop_duplicates()
lin_df=pd.read_csv(sys.argv[7], sep=',').drop_duplicates()
count_df_r=pd.read_csv(sys.argv[8], sep=',').drop_duplicates()

stats_df=stats_df[(stats_df.tax_id.isin(lin_df.tax_id))]
count_df=count_df_r[(count_df_r.qseqid.isin(stats_df.qseqid))]
stats_df=stats_df[(stats_df.qseqid.isin(count_df.qseqid))]



df_s_l=stats_df.merge(lin_df, on='tax_id', how='left')
df=df_s_l.merge(count_df, on='qseqid', how='left')
df = df[df.iloc[: , -1].notna()]
tmp_df=df.iloc[:, np.r_[0,30:len(df. columns)]]
tmp_df.to_csv(r'tmp_df.csv')


df.to_csv(r'df.csv')
csv_columns=['All-sample']
list_files=[]
for input_files in path_files :
	if input_files.endswith(ext1+ext_file):
		file_name=input_files.split(ext1+ext_file)[0]
		csv_columns.append(file_name)
		list_files.append(file_name)

result_table = pd.DataFrame(columns=csv_columns,index=["Total read R1","Total read R2","Avg read length R1","Avg read length R2","Reads 1 cleaned","Reads 2 cleaned","Avg cleaned read length R1 (after cutadapt)","Avg cleaned read length R2 (after cutadapt)","Avg insert_size","Map on Diptera","UnMapped on Diptera","Map on bacteria","UnMapped on bacteria","Map on Host Genome","UnMapped Host Genome","Total pairs","Combined pairs","Widows","Assembled","Duplicates","Reads_count","Singletons","Nb of contigs","Min contigs length","Max contigs length","Avg contigs length","Contigs with viral hit","Nb of reads with viral hit 'inside' a contig","Nb of reads with viral hit as singleton","Reads with viral hit","% viral reads","Nb of viral hit 1 =< Reads < 10 ","Nb of viral hit 10 =< Reads < 100 ","Nb of viral hit 100 =< Reads < 1000","Nb of viral hit 1000 =< Reads < 10000","Nb of viral hit 10000=< Reads","Nb viral family","Nb viral genus","Nb viral species"])
contig_length=pd.read_csv(f'{output_directory}/logs/02_assembly_results/logsAssembly/{run}_assembly_stats.txt', sep='	')
stats_contigs=contig_length.iloc[:, 1].describe()

contig_length.columns.values[0] = "qseqid"


n=0
for files_name in list_files :
	with open(f"{output_directory}/logs/01_read_processing/01_cutadapt/01_remove_sequencing_adapters/{files_name}{ext1}_Remove_sequencing_adapters.log",'r') as cut1_1:
		for line in cut1_1:
			if "Total reads processed" in line:
				c = line.replace(',','').replace(' ','').replace('\n','').split(":")
				result_table.at['Total read R1', files_name] =int(c[-1])
			if "Total written" in line:
				c1 = line.replace(',','').replace('b',':').replace('\n','').replace(' ','').split(":")
				result_table.at['Avg read length R1', files_name]="%.2f" % (int(c1[1])/int(c[-1]))
	cut1_1.close()
	with open(f"{output_directory}/logs/01_read_processing/01_cutadapt/01_remove_sequencing_adapters/{files_name}{ext2}_Remove_sequencing_adapters.log",'r') as cut1_2:
		for line in cut1_2:
			if "Total reads processed" in line:
				c = line.replace(',','').replace(' ','').replace('\n','').split(":")
				result_table.at['Total read R2', files_name]=int(c[-1])
			if "Total written" in line:
				c1 = line.replace(',','').replace('b',':').replace('\n','').replace(' ','').split(":")
				result_table.at['Avg read length R2', files_name]="%.2f" % (int(c1[1])/int(c[-1]))
	cut1_2.close()

	with open(f"{output_directory}/logs/01_read_processing/01_cutadapt/02_triming/{files_name}{ext1}_triming.log",'r') as cut2_1:
		for line in cut2_1:
			if "Reads written" in line:
				c = line.replace(',','').replace('(',':').replace('\n','').replace(' ','').split(":")
				result_table.at['Reads 1 cleaned', files_name]=int(c[2])
			if "Total written" in line:
				c1 = line.replace(',','').replace('b',':').replace('\n','').replace(' ','').split(":")
				result_table.at['Avg cleaned read length R1 (after cutadapt)', files_name]="%.2f" % (int(c1[1])/int(c[2]))
	cut2_1.close()
	with open(f"{output_directory}/logs/01_read_processing/01_cutadapt/02_triming/{files_name}{ext2}_triming.log",'r') as cut2_2:
		for line in cut2_2:
			if "Reads written" in line:
				c = line.replace(',','').replace('(',':').replace('\n','').replace(' ','').split(":")
				result_table.at['Reads 2 cleaned', files_name]=int(c[2])
			if "Total written" in line:
				c1 = line.replace(',','').replace('b',':').replace('\n','').replace(' ','').split(":")
				result_table.at['Avg cleaned read length R2 (after cutadapt)', files_name]="%.2f" % (int(c1[1])/int(c[2]))
	cut2_2.close()
	path=f"{output_directory}/logs/03_mapping_on_assembly/{files_name}_insert_size_metrics_{run}.txt"
	files_insert=glob.glob(path)
	with open(files_insert[0],'r') as insert:
		for line in insert:
			if "LIBRARY	READ_GROUP" in line:
				line = next(insert)
				c = line.split("\t")
				result_table.at['Avg insert_size', files_name]="%.2f" % (float(c[5]))
	insert.close()
	with open(f"{output_directory}/logs/01_read_processing/07_flash_merge_pair/{files_name}q_flash.log",'r') as flash:
		for line in flash:
			if "Total pairs" in line:
				c = line.replace('\n','').replace(' ','').split(":")
				result_table.at['Total pairs', files_name]=int(c[1])
			if "Combined pairs" in line:
				c = line.replace('\n','').replace(' ','').split(":")
				result_table.at['Combined pairs', files_name]=int(c[1])
	flash.close()
	path=f"{output_directory}/logs/03_mapping_on_assembly/03_CountsMapping/{files_name}_coverage*"
	files_cov=glob.glob(path)
	with open(files_cov[0],'r') as cov:
		for line in cov:
			if "Mapped" in line:
				c = line.split(":")
				result_table.at['Reads_count', files_name]=int(c[1])
				line = next(cov)
				c = line.split(" ")
				result_table.at['Nb of contigs', files_name]=int(c[0])
				line = next(cov)
				c = line.split(":")
				result_table.at['Singletons', files_name]=int(c[1])
	cov.close()

	with open(f"{output_directory}/logs/03_mapping_on_assembly/01_mapping/{files_name}_duplicates_pairs_{run}.txt",'r') as dp,  open(f"{output_directory}/logs/03_mapping_on_assembly/01_mapping/{files_name}_duplicates_wi_{run}.txt",'r') as dw :
		for line in dp :
			if "READ:" in line:
				reads_pair = int(line.replace('\n','').split(": ")[-1])
			if "DUPLICATE TOTAL:" in line:
				dup_pair = int(line.replace('\n','').split(": ")[-1])
				
		for line in dw:
			if "READ:" in line:
				reads_wi = int(line.replace('\n','').split(": ")[-1])
			if "DUPLICATE TOTAL:" in line:
				dup_wi = int(line.replace('\n','').split(": ")[-1])
		result_table.at['Duplicates', files_name]=dup_pair+dup_wi
		result_table.at['Assembled', files_name]=result_table.at['Duplicates', files_name]+result_table.at['Reads_count', files_name]


	with open(f"{output_directory}/logs/01_read_processing/Stats_contaminent_{files_name}.txt",'r') as conta:
		print(files_name)
		for line in conta:
			if "Host_pair_R1" in line:
				c = line.replace('\n','').split(":")
				R1_h=c[1]
				line = next(conta)
				c = line.replace('\n','').split(":")
				R2_h=c[1]
				line = next(conta)
				c = line.replace('\n','').split(":")
				wi_h=c[1]
				line = next(conta)
				c = line.replace('\n','').split(":")
				R1_b=c[1]
				line = next(conta)
				c = line.replace('\n','').split(":")
				R2_b=c[1]
				line = next(conta)
				c = line.replace('\n','').split(":")
				wi_b=c[1]
				line = next(conta)
				c = line.replace('\n','').split(":")
				R1_gh=c[1]
				line = next(conta)
				c = line.replace('\n','').split(":")
				R2_gh=c[1]
				line = next(conta)
				c = line.replace('\n','').split(":")
				wi_gh=c[1]
				result_table.at['Widows', files_name]=int(wi_b)
				result_table.at['UnMapped on Diptera', files_name]=int(R1_h)+int(R2_h)+int(wi_h)
				result_table.at['UnMapped on bacteria', files_name]=int(R1_b)+int(R2_b)+int(wi_b)
				result_table.at['UnMapped Host Genome', files_name]=int(R1_gh)+int(R2_gh)+int(wi_gh)
				result_table.at['Map on Diptera', files_name]=(int(result_table.at['Reads 1 cleaned', files_name])+int(result_table.at['Reads 2 cleaned', files_name]))-int(result_table.at['UnMapped on Diptera', files_name])
				result_table.at['Map on bacteria', files_name]=result_table.at['UnMapped on Diptera', files_name]-result_table.at['UnMapped on bacteria', files_name]
				result_table.at['Map on Host Genome', files_name]=result_table.at['UnMapped on bacteria', files_name]-result_table.at['UnMapped Host Genome', files_name]
	conta.close()
	#print(df[files_name])
	result_table.at['Nb viral family', files_name]=df[["family", files_name]][df[files_name]> 1].family.value_counts().count()
	result_table.at['Nb viral genus', files_name]=df[["genus", files_name]][df[files_name]> 1].genus.value_counts().count()
	result_table.at['Nb viral species', files_name]=df[["species", files_name]][df[files_name]> 1].species.value_counts().count()
	raws = df[["species",files_name]].groupby('species',as_index=False).agg({files_name: 'sum' }).drop(columns='species')
	
	ranges = [1,10,100,1000,10000]
	result_table.at['Reads with viral hit', files_name]=raws.values.sum()
	result_table.at['Nb of viral hit 1 =< Reads < 10 ', files_name]=raws.groupby(pd.cut(raws[files_name], ranges)).count().iloc[0][files_name]
	result_table.at['Nb of viral hit 10 =< Reads < 100 ', files_name]=raws.groupby(pd.cut(raws[files_name], ranges)).count().iloc[1][files_name]
	result_table.at['Nb of viral hit 100 =< Reads < 1000', files_name]=raws.groupby(pd.cut(raws[files_name], ranges)).count().iloc[2][files_name]
	result_table.at['Nb of viral hit 1000 =< Reads < 10000', files_name]=raws.groupby(pd.cut(raws[files_name], ranges)).count().iloc[3][files_name]
	result_table.at['Nb of viral hit 10000=< Reads', files_name]=raws[raws[files_name]> 10000].count().values[0]
	result_table.at['Contigs with viral hit', files_name]=count_df[count_df[files_name]> 0].count().values[0]
	result_table.at['Min contigs length', files_name]=int(contig_length[(contig_length.qseqid.isin(count_df_r[count_df_r[files_name]!= 0][["qseqid",files_name]] .qseqid))].iloc[:, 1].describe().iloc[3])

	result_table.at['Max contigs length', files_name]=int(contig_length[(contig_length.qseqid.isin(count_df_r[count_df_r[files_name]!= 0][["qseqid",files_name]] .qseqid))].iloc[:, 1].describe().iloc[7])

	result_table.at['Avg contigs length', files_name]=round(contig_length[(contig_length.qseqid.isin(count_df_r[count_df_r[files_name]!= 0][["qseqid",files_name]] .qseqid))].iloc[:, 1].describe().iloc[1],2)
	result_table.at["Nb of reads with viral hit 'inside' a contig", files_name]=count_df[count_df[["qseqid",files_name]].qseqid.astype(str).str.startswith('k') | count_df[["qseqid",files_name]].qseqid.astype(str).str.startswith('C')][files_name].sum()
	result_table.at["Nb of reads with viral hit as singleton", files_name]=count_df[~count_df[["qseqid",files_name]].qseqid.astype(str).str.startswith('k') & ~count_df[["qseqid",files_name]].qseqid.astype(str).str.startswith('C')][files_name].sum()
	result_table.at['% viral reads', files_name]=round(result_table.loc["Reads with viral hit", files_name] *100 / (result_table.loc["Total read R1", files_name]+result_table.loc["Total read R1", files_name]),2)

result_table.at['Nb of contigs', 'All-sample']=int(count_df_r.shape[0])-1
result_table.at['Min contigs length', 'All-sample']=int(stats_contigs.iloc[3])
result_table.at['Max contigs length', 'All-sample']=int(stats_contigs.iloc[7])
result_table.at['Avg contigs length', 'All-sample']=round(stats_contigs.iloc[1],2)
result_table.at['Contigs with viral hit', 'All-sample']=count_df.shape[0]
result_table.at['Reads with viral hit', 'All-sample']=count_df.iloc[:, 1:].values.sum()
result_table.at['Nb viral family', 'All-sample']=df.family.value_counts().count()
result_table.at['Nb viral genus', 'All-sample']=df.genus.value_counts().count()
result_table.at['Nb viral species', 'All-sample']=df.species.value_counts().count()


spp=df.iloc[:,np.r_[df.columns.get_loc("species"), df_s_l.shape[1]:df.shape[1]]].groupby('species',as_index=False).agg('sum').drop(columns='species').sum(axis=1)
result_table.at['Nb of viral hit 1 =< Reads < 10 ',  'All-sample']=spp.groupby(pd.cut(spp, ranges)).count().iloc[0]
result_table.at['Nb of viral hit 10 =< Reads < 100 ',  'All-sample']=spp.groupby(pd.cut(spp, ranges)).count().iloc[1]
result_table.at['Nb of viral hit 100 =< Reads < 1000',  'All-sample']=spp.groupby(pd.cut(spp, ranges)).count().iloc[2]
result_table.at['Nb of viral hit 1000 =< Reads < 10000',  'All-sample']=spp.groupby(pd.cut(spp, ranges)).count().iloc[3]
result_table.at['Nb of viral hit 10000=< Reads',  'All-sample']=spp[spp > 10000].count()

row_sum=["Total read R1","Total read R2","Reads 1 cleaned","Reads 2 cleaned","Map on Diptera","UnMapped on Diptera","Map on bacteria","UnMapped on bacteria","Map on Host Genome","UnMapped Host Genome","Total pairs","Combined pairs","Widows","Assembled","Duplicates","Reads_count","Singletons","Nb of reads with viral hit 'inside' a contig","Nb of reads with viral hit as singleton","Reads with viral hit"]

row_mean=["Avg read length R1","Avg read length R2","Avg cleaned read length R1 (after cutadapt)","Avg cleaned read length R2 (after cutadapt)","Avg insert_size"]
print("ok3")

for row in row_sum:
	result_table.at[row,'All-sample']=result_table.loc[row,result_table.columns != 'All-sample'].apply(int).sum(axis=0)
for row in row_mean:
	result_table.at[row,'All-sample']=result_table.loc[row,result_table.columns != 'All-sample'].apply(float).mean(axis=0).round(2)


result_table.at['% viral reads',  'All-sample']=round(result_table.loc["Reads with viral hit", 'All-sample'] *100 / (result_table.loc["Total read R1", 'All-sample']+result_table.loc["Total read R1", 'All-sample']),2)


result_table.to_csv(out)

	#	raws = df[[files_name,'qseqid']]
#	in_contigs=0
#	numcont=0
#	for index, raw in raws.iterrows():
#		numcont+=1
#		if raw[files_name] != 0 :
#			if raw['qseqid'].startswith('k') or raw['qseqid'].startswith('C'):
#				in_contigs+=raw[files_name]
#	sum0=sum10=sum100=sum1000=sum10000=sum0c=0
#	numcont=0
#	for index, raw in raws.iterrows():
#		numcont+=1
#		if raw[files_name] != 0 :
#			sum0+=raw[files_name]
#		if 10 <= raw[files_name] < 100 :
#			sum10+=1
#		if 100 <= raw[files_name] <1000 :
#			sum100+=1
#		if 1000 <= raw[files_name] < 10000 :
#			sum1000+=1
#		if raw[files_name] >= 10000 :
#			sum10000+=1
#	print("ok2.02")
#	result_table.at['Reads with viral hit', files_name]=sum0
#	result_table.at['Nb of viral hit 10 =< Reads < 100 ', files_name]=sum10
#	result_table.at['Nb of viral hit 100 =< Reads < 1000', files_name]=sum100
#	result_table.at['Nb of viral hit 1000 =< Reads < 10000', files_name]=sum1000
#	result_table.at['Nb of viral hit 10000=< Reads', files_name]=sum10000
#	raws = df[[files_name,'qseqid']]
#	in_contigs=0
#	numcont=0
#	for index, raw in raws.iterrows():
#		numcont+=1
#		if raw[files_name] != 0 :
#			if raw['qseqid'].startswith('k') or raw['qseqid'].startswith('C'):
#				in_contigs+=raw[files_name]
#	out_oncitgs=sum0-in_contigs
#	result_table.at['Contigs with viral hit', 'All-sample']=numcont
#	result_table.at["Nb of reads with viral hit 'inside' a contig", files_name]=in_contigs
#	result_table.at["Nb of reads with viral hit as singleton", files_name]=out_oncitgs
##	for i in range(19,24):
##		dict_data[i][files_name]='-'
##	for i in range(24,27):
##		dict_data[i]['All-sample']+=dict_data[i][files_name]

#print("ok2")

#tot_hit=tot_hit10=tot_hit100=tot_hit1000=tot_hit10000=0


#for index, raw in tmp_df.iterrows():
#	sum_raw=0
#	for input_files in path_files :
#		if input_files.endswith(ext1+ext_file):
#			files_name=input_files.split(ext1)[0]
#			sum_raw+=raw[files_name]
#			tot_hit+=1
#	if 10 <= sum_raw< 100 :
#		tot_hit10+=1
#	if 100 <= sum_raw < 1000 :
#		tot_hit100+=1
#	if 1000 <= sum_raw < 10000 :
#		tot_hit1000+=1
#	if sum_raw >= 10000 :
#		tot_hit10000+=1

#result_table.at['Nb of viral hit 10 =< Reads < 100 ','All-sample']=tot_hit10
#result_table.at['Nb of viral hit 100 =< Reads < 1000','All-sample']=tot_hit100
#result_table.at['Nb of viral hit 1000 =< Reads < 10000','All-sample']=tot_hit1000
#result_table.at['Nb of viral hit 10000=< Reads','All-sample']=tot_hit10000

##print("3")
#path=os.listdir("logs/logsAssembly/")
#for input_files in path :
#	if input_files.endswith(run+"_assembly_stats.txt"):
#		with open("logs/logsAssembly/"+input_files,'r') as asb:
#			data=pd.read_csv(asb, sep="\t", header=None)
#			result_table.at['Nb total of contigs','All-sample']=len(data.index)
#			c=data.min()
#			result_table.at['Min contigs length','All-sample']=c.values[1]
#			c=data.max()
#			result_table.at['Max contigs length','All-sample']=c.values[1]
#			c=data.mean()
#			result_table.at['Avg contigs length','All-sample']="%.2f" %(c.values[0])

#row_sum=["Total read R1","Total read R2","Reads 1 cleaned","Reads 2 cleaned","Map on Diptera","UnMapped on Diptera","Map on bacteria","UnMapped on bacteria","Total pairs","Combined pairs","Widows","Assembled","Singletons","Nb of reads with viral hit 'inside' a contig","Nb of reads with viral hit as singleton","Reads with viral hit"]

#row_mean=["Avg read length R1","Avg read length R2","Avg cleaned read length R1 (after cutadapt)","Avg cleaned read length R2 (after cutadapt)","Avg insert_size","Reads spread across n contig (nb for each samples and Avg for all_samples)"]
#print("ok3")

#for row in row_sum:
#	result_table.at[row,'All-sample']=result_table.loc[row,result_table.columns != 'All-sample'].apply(int).sum(axis=0)
#for row in row_mean:
#	result_table.at[row,'All-sample']=result_table.loc[row,result_table.columns != 'All-sample'].apply(float).mean(axis=0).round(2)













#result_table.at['Total read R1','All-sample']=result_table.loc['Total read R1',result_table.columns != 'All-sample'].apply(int).sum(axis=0)
#result_table.at['Total read R2','All-sample']=result_table.loc['Total read R2',result_table.columns != 'All-sample'].apply(int).sum(axis=0)
#result_table.at['Avg read length R1','All-sample']=result_table.loc['Avg read length R1',result_table.columns != 'All-sample'].apply(float).mean(axis=0).round(2)
#result_table.at['Avg read length R2','All-sample']=result_table.loc['Avg read length R2',result_table.columns != 'All-sample'].apply(float).mean(axis=0).round(2)
#result_table.at['Reads 1 cleaned','All-sample']=result_table.loc['Reads 1 cleaned',result_table.columns != 'All-sample'].apply(int).sum(axis=0)
#result_table.at['Reads 2 cleaned','All-sample']=result_table.loc['Reads 2 cleaned',result_table.columns != 'All-sample'].apply(int).sum(axis=0)
#result_table.at['Avg cleaned read length R1 (after cutadapt)','All-sample']=result_table.loc['Avg cleaned read length R1 (after cutadapt)',result_table.columns != 'All-sample'].apply(float).mean(axis=0).round(2)
#result_table.at['Avg cleaned read length R2 (after cutadapt)','All-sample']=result_table.loc['Avg cleaned read length R2 (after cutadapt)',result_table.columns != 'All-sample'].apply(float).mean(axis=0).round(2)
#result_table.at['Avg read length R2','All-sample']=result_table.loc['Avg read length R2',result_table.columns != 'All-sample'].apply(float).mean(axis=0).round(2)
#result_table.at['','All-sample']=result_table.loc[''].sum(axis=0)
#result_table.at['','All-sample']=result_table.loc[''].sum(axis=0)
#result_table.at['','All-sample']=result_table.loc[''].sum(axis=0)
#result_table.at['','All-sample']=result_table.loc[''].sum(axis=0)
#result_table.at['','All-sample']=result_table.loc[''].sum(axis=0)
#result_table.at['','All-sample']=result_table.loc[''].sum(axis=0)
#result_table.at['','All-sample']=result_table.loc[''].sum(axis=0)

#print(result_table)
#result_table.loc['Avg read length R1'].apply(np.round)
#result_table.at['', files_name]

#def WriteDictToCSV(csv_file,csv_columns,dict_data):
#    with open(csv_file, 'w') as csvfile:
#        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#        writer.writeheader()
#        for data in dict_data:
#            writer.writerow(data)
#            
#            
#csv_columns=['Stats','All-sample']
#dict_data = [{'Stats':"Total read R1"},{'Stats':"Total read R2"},{'Stats':"Avg read length R1"},{'Stats':"Avg read length R2"},{'Stats':"Reads 1 cleaned"},{'Stats':"Reads 2 cleaned"},
#{'Stats':"Avg cleaned read length R1 (after cutadapt)"},{'Stats':"Avg cleaned read length R2 (after cutadapt)"},{'Stats':"Avg insert_size"},{'Stats':"Map on Diptera"},{'Stats':"UnMapped on Diptera"},{'Stats':"Map on bacteria"},{'Stats':"UnMapped on bacteria"},
#{'Stats':"Total pairs"},{'Stats':"Combined pairs"},{'Stats':"Widows"},{'Stats':"Assembled"},{'Stats':"Reads spread across n contig (nb for each samples and Avg for all_samples)"},{'Stats':"Singletons"},{'Stats':"Nb total of contigs"},
#{'Stats':"Min contigs length"},{'Stats':"Max contigs length"},{'Stats':"Avg contigs length"},{'Stats':"Contigs with viral hit"},{'Stats':"Nb of reads with viral hit 'inside' a contig"},{'Stats':"Nb of eads with viral hit as singleton"},{'Stats':"Reads with viral hit"},
#{'Stats':"Nb of viral hit 10 =< Reads < 100 "},{'Stats':"Nb of viral hit 100 =< Reads < 1000"},{'Stats':"Nb of viral hit 1000 =< Reads < 10000"},{'Stats':"Nb of viral hit 10000=< Reads"},{'Stats':"Nb viral family"},{'Stats':"Nb viral genus"},{'Stats':"Nb viral species"}]

#for i in range(27):
#	dict_data[i]['All-sample']=int(0)
#list_files=[]
#for input_files in path_files :
#	if input_files.endswith(ext1+ext_file):
#		file_name=input_files.split(ext1+ext_file)[0]
#		csv_columns.append(file_name)
#		list_files.append(file_name)

#for files_name in list_files :
#	with open("logs/logscutadapt/"+files_name+ext1+"_cut1.log",'r') as cut1_1:
#		for line in cut1_1:
#			if "Total reads processed" in line:
#				c = line.replace(',','').replace(' ','').replace('\n','').split(":")
#				dict_data[0][files_name]=int(c[-1])
#			if "Total written" in line:
#				c1 = line.replace(',','').replace('b',':').replace('\n','').replace(' ','').split(":")
#				dict_data[2][files_name]="%.2f" % (int(c1[1])/int(c[-1]))

#	with open("logs/logscutadapt/"+files_name+ext2+"_cut1.log",'r') as cut1_2:
#		for line in cut1_2:
#			if "Total reads processed" in line:
#				c = line.replace(',','').replace(' ','').replace('\n','').split(":")
#				dict_data[1][files_name]=int(c[-1])
#			if "Total written" in line:
#				c1 = line.replace(',','').replace('b',':').replace('\n','').replace(' ','').split(":")
#				dict_data[3][files_name]="%.2f" % (int(c1[1])/int(c[-1]))
#	with open("logs/logscutadapt/"+files_name+ext1+"_cut2.log",'r') as cut2_1:
#		for line in cut2_1:
#			if "Reads written" in line:
#				c = line.replace(',','').replace('(',':').replace('\n','').replace(' ','').split(":")
#				dict_data[4][files_name]=int(c[2])
#			if "Total written" in line:
#			
#				c1 = line.replace(',','').replace('b',':').replace('\n','').replace(' ','').split(":")
#				dict_data[6][files_name]="%.2f" % (int(c1[1])/int(c[2]))
#	with open("logs/logscutadapt/"+files_name+ext2+"_cut2.log",'r') as cut2_2:
#		for line in cut2_2:
#			if "Reads written" in line:
#				c = line.replace(',','').replace('(',':').replace('\n','').replace(' ','').split(":")
#				dict_data[5][files_name]=int(c[2])
#			if "Total written" in line:
#				c1 = line.replace(',','').replace('b',':').replace('\n','').replace(' ','').split(":")
#				dict_data[7][files_name]="%.2f" % (int(c1[1])/int(c[2]))

#	path="logs/insert_size/"+files_name+"_insert_size_metrics_"+run+".txt"
#	files_insert=glob.glob(path)
#	with open(files_insert[0],'r') as insert:
##	with open("logs/insert_size/"+files_name+"_insert_size_metrics.txt",'r') as insert:
#		for line in insert:
#			if "LIBRARY	READ_GROUP" in line:
#				line = next(insert)
#				c = line.split("\t")
#				dict_data[8][files_name]="%.2f" % (float(c[4]))

#	with open("logs/logsFLASH/"+files_name+"_flash.log",'r') as flash:
#		for line in flash:
#			if "Total pairs" in line:
#				c = line.replace('\n','').replace(' ','').split(":")
#				dict_data[13][files_name]=int(c[1])
#			if "Combined pairs" in line:
#				c = line.replace('\n','').replace(' ','').split(":")
#				dict_data[14][files_name]=int(c[1])

#	path="logs/logs_coverage/"+files_name+"_coverage*"
#	files_cov=glob.glob(path)
#	with open(files_cov[0],'r') as cov:
#		for line in cov:
#			if "Mapped" in line:
#				c = line.split(":")
#				dict_data[16][files_name]=int(c[1])
#				line = next(cov)
#				c = line.split(" ")
#				dict_data[17][files_name]=int(c[0])
#				line = next(cov)
#				c = line.split(":")
#				dict_data[18][files_name]=int(c[1])
#				
#	with open("logs/logs_contaminent/Stats_contaminent_"+files_name+".txt",'r') as conta:
#		for line in conta:
#			if "Host_pair_R1" in line:
#				c = line.replace('\n','').split(":")
#				R1_h=c[1]
#				line = next(conta)
#				c = line.replace('\n','').split(":")
#				R2_h=c[1]
#				line = next(conta)
#				c = line.replace('\n','').split(":")
#				wi_h=c[1]
#				line = next(conta)
#				c = line.replace('\n','').split(":")
#				R1_b=c[1]
#				line = next(conta)
#				c = line.replace('\n','').split(":")
#				R2_b=c[1]
#				line = next(conta)
#				c = line.replace('\n','').split(":")
#				wi_b=c[1]
#				dict_data[15][files_name]=int(wi_b)
#				dict_data[10][files_name]=int(R1_h)+int(R2_h)+int(wi_h)
#				dict_data[12][files_name]=int(R1_b)+int(R2_b)+int(wi_b)
#				dict_data[9][files_name]=(int(dict_data[4][files_name])+int(dict_data[5][files_name]))-int(dict_data[10][files_name])
#				dict_data[11][files_name]=dict_data[10][files_name]-dict_data[12][files_name]
##WriteDictToCSV("test.step1.csv",csv_columns,dict_data)
#print("1")
#df_s = pd.read_csv(stats_seq, delimiter='\t')
#df_l=pd.read_csv(lineage, delimiter=',')
#df_c = pd.read_csv(count_table, delimiter=',')
#df_s_l=df_s.merge(df_l, on='tax_id', how='left')
#df=df_s_l.merge(df_c, on='qseqid', how='left')
#df = df[df.iloc[: , -1].notna()]
#tmp_df=df.iloc[:, np.r_[0,30:len(df. columns)]]
#tmp_df.to_csv(r'tmp_df.csv')
#df.to_csv(r'df.csv')
#n=0
#for files_name in list_files :
#	n+=1
#	for i in (0,1,4,5,16,18):
#		dict_data[i]['All-sample']+=int(dict_data[i][files_name])
#	for i in (2,3,6,7,17):
#		if dict_data[i]['All-sample']==0:
#			dict_data[i]['All-sample']=round((float(dict_data[i][files_name])), 2)
#		else:
#			dict_data[i]['All-sample']= round((float(dict_data[i]['All-sample']+float(dict_data[i][files_name]))/2), 2)
#	stat_vir=df[files_name] != 0
#	df1=(df[stat_vir].family.value_counts())
#	dict_data[31][files_name]=df1.count()
#	df1_1=(df.family.value_counts())
#	dict_data[31]['All-sample']=df1_1.count()
#	df2=(df[stat_vir].genus.value_counts())
#	dict_data[32][files_name]=df2.count()
#	df2_2=(df.genus.value_counts())
#	dict_data[32]['All-sample']=df2_2.count()
#	df3=(df[stat_vir].species.value_counts())
#	dict_data[33][files_name]=df3.count()
#	df3_3=(df.species.value_counts())
#	dict_data[33]['All-sample']=df3_3.count()
#	raws = df[[files_name]]
#	sum0=sum10=sum100=sum1000=sum10000=sum0c=0
#	numcont=0
#	for index, raw in raws.iterrows():
#		numcont+=1
#		if raw[files_name] != 0 :
#			sum0+=raw[files_name]
#			print()
#		if 10 <= raw[files_name] < 100 :
#			sum10+=1
#		if 100 <= raw[files_name] <1000 :
#			sum100+=1
#		if 1000 <= raw[files_name] < 10000 :
#			sum1000+=1
#		if raw[files_name] >= 10000 :
#			sum10000+=1
#	dict_data[26][files_name]=sum0
#	dict_data[27][files_name]=sum10
#	dict_data[28][files_name]=sum100
#	dict_data[29][files_name]=sum1000
#	dict_data[30][files_name]=sum10000
##	df = pd.read_csv(stats_seq, delimiter=',')
#	raws = df[[files_name,'qseqid']]
#	in_contigs=0
#	numcont=0
#	for index, raw in raws.iterrows():
#		numcont+=1
#		if raw[files_name] != 0 :
#			if raw['qseqid'].startswith('k') or raw['qseqid'].startswith('C'):
#				in_contigs+=raw[files_name]
#	out_oncitgs=sum0-in_contigs
#	dict_data[23]['All-sample']=numcont
#	dict_data[24][files_name]=in_contigs

#	dict_data[25][files_name]=out_oncitgs
#	for i in range(19,24):
#		dict_data[i][files_name]='-'
#	for i in range(24,27):
#		dict_data[i]['All-sample']+=dict_data[i][files_name]
#print("2")

#tot_hit=tot_hit10=tot_hit100=tot_hit1000=tot_hit10000=0


#for index, raw in tmp_df.iterrows():
#	sum_raw=0
#	for input_files in path_files :
#		if input_files.endswith(ext1+ext_file):
#			files_name=input_files.split(ext1)[0]
#			sum_raw+=raw[files_name]
#			tot_hit+=1
#	if 10 <= sum_raw< 100 :
#		tot_hit10+=1
#	if 100 <= sum_raw < 1000 :
#		tot_hit100+=1
#	if 1000 <= sum_raw < 10000 :
#		tot_hit1000+=1
#	if sum_raw >= 10000 :
#		tot_hit10000+=1
#dict_data[27]['All-sample']=tot_hit10
#dict_data[27]['All-sample']=tot_hit10
#dict_data[28]['All-sample']=tot_hit100
#dict_data[29]['All-sample']=tot_hit1000
#dict_data[30]['All-sample']=tot_hit10000
#print("3")
#path=os.listdir("logs/logsAssembly/")
#for input_files in path :
#	if input_files.endswith(run+"_assembly_stats.txt"):
#		with open("logs/logsAssembly/"+input_files,'r') as asb:
#			data=pd.read_csv(asb, sep="\t", header=None)
#			dict_data[19]['All-sample']=len(data.index)
#			c=data.min()
#			dict_data[20]['All-sample']=c.values[1]
#			c=data.max()
#			dict_data[21]['All-sample']=c.values[1]
#			c=data.mean()
#			dict_data[22]['All-sample']="%.2f" %(c.values[0])
#			
#csv_file = out
#WriteDictToCSV(csv_file,csv_columns,dict_data)
