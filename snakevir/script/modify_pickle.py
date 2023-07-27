import pickle
import sys, os



with open(sys.argv[1], 'rb') as handle:
    taxo_dict = pickle.load(handle)
    
    
taxo_dict['fam2gent']['Hepadnaviridae']="dsDNA-RT"
taxo_dict['fam2gent']['Caulimoviridae']="dsDNA-RT"

print(taxo_dict['fam2gent']['Caulimoviridae'])

with open('correc_taxo1.pickle', 'wb') as handle:
	pickle.dump(taxo_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
