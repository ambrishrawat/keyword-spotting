import os
import xml.etree.ElementTree as et
import xml.dom.minidom as minidom
import pickle
import csv

def getKWlist(qaddr):
	tree = et.parse(qaddr)
	r = tree.getroot()
	kwlist = {}
	for keywords,kid in zip(r.iter('kwtext'),r.iter('kw')):
		kwlist[kid.attrib['kwid']] = (keywords.text).split()
	return kwlist

class Morph:
	""" The morphological decomposition"""
	def _init_(self):
		pass
	def getmorphdict(self,dpath):
		dlist = []
		with open(dpath,'r') as dfile:
			dlist = dfile.readlines()
		d = {}
		for dele in dlist:
			temp =dele.split()
			d[temp[0]] = temp[1:]
		return d

	def morphctm(self,m,f,o):
		dict_list = []
		flist = []
		with open(f,'r') as infile:
			flist = infile.readlines()
		
		ocsv = csv.writer(open(o,'w'),delimiter=' ')
		for f in flist:
			f = f.split()
			d = {'file_name': f[0], 'channel' : f[1], 'tbeg' : f[2], 'dur' : f[3], 'word' : f[4].lower(), 'score' : f[5]}
			dict_list.append(d)
		for i in range(len(dict_list)):
			fname = dict_list[i].get('file_name')
			channel = dict_list[i].get('channel')
			tbeg = dict_list[i].get('tbeg')
			dur = dict_list[i].get('dur')
			score = dict_list[i].get('score')
			
			if dict_list[i].get('word') in m:
				
				mlist = m[dict_list[i].get('word')]
				mlen = float(len(mlist))
				for mitem in mlist:
					ocsv.writerow([fname,channel,tbeg,str(float(dur)/mlen),mitem,str(float(score))])
					tbeg = str(float(tbeg) + float(dur)/mlen)
			
			else:
				ocsv.writerow([fname,channel,tbeg,dur,dict_list[i].get('word'),score])

	def morphdict(self,m,f,o,ecf_filename="IARPA-babel202b-v1.0d_conv-dev.ecf.xml",language="swahili",encoding="UTF-8",compareNormalize="lowercase",version="202 IBM and BBN keywords"):
		flist = []
		with open(f, "r") as qfile:
			kwlist = getKWlist(qfile)
		
		
		root = et.Element("kwslist",ecf_filename=ecf_filename, language=language, encoding=encoding,compareNormalize=compareNormalize,version=version)
		
		for kwid,k in kwlist.items():
			kwele = et.SubElement(root,"kw",kwid=str(kwid))
			kwchild = et.SubElement(kwele,"kwtext")
			kwchild.text = ' '.join(map(lambda x: ' '.join(m[x]),k))
		xmlstr = minidom.parseString(et.tostring(root)).toprettyxml(indent="")
		temp_list = xmlstr.split('\n')
		xmlstr = '\n'.join(temp_list[1:])
		#xmlstr = et.tostring(root,encoding="utf8",method="xml")
		with open(o,'w') as ofile:
			ofile.write(xmlstr)
		pass
			

		
