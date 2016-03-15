import csv
import operator
class Indexer:
	"""Indexer class"""

	def _init_(self):
		pass

	def indexer(self,f):
		"""
		Converts the received latice (1 best-hypothesis in this case) file into an indexer
		Args
			f - address to the input set of lattices (1-best hypotheses in this case)
		Returns
			a - dictionary corresponding to the lattice received in fs
		"""
		dict_indexer = {}
		flist = []
		with open(f,'r') as infile:
			flist = infile.readlines()
		
		dict_list = []
		
		#get the rows in list
		for f in flist:
			f = f.split()
			d = {'file_name': f[0], 'channel' : f[1], 'tbeg' : float(f[2]), 'dur' : float(f[3]), 'word' : f[4].lower(), 'score' : float(f[5])}
			dict_list.append(d)

		#update next words in the list
		for i in range(len(dict_list)):
			if i < len(dict_list)-1:
				dict_list[i]['next'] = dict_list[i+1].get('word')
			else:
				dict_list[i]['next'] = None


		#make the dictionary of words 
		for i in range(len(dict_list)):
			if dict_list[i].get('word') not in dict_indexer.keys():
				dict_indexer[dict_list[i].get('word')] = [dict_list[i]]
			else:
				val_word = dict_indexer.get(dict_list[i].get('word'))
				val_word.append(dict_list[i])
				dict_indexer[dict_list[i].get('word')] = val_word

		for dkey,dval in dict_indexer.items():
			
			flist = set([k['file_name'] for k in dval])
			d_newval = []
			[d_newval.append(temp) \
				for f in flist \
				for temp in sorted(filter(lambda x: x['file_name']==f,dval),key=operator.itemgetter('tbeg'))]
			dict_indexer[dkey] = d_newval	
		return dict_indexer





