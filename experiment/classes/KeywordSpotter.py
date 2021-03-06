import xml.etree.ElementTree as et
import xml.dom.minidom as minidom


def normalise(list1,nfactor):
	for l1 in list1:
		#l1['score'] = l1.get('score')/nfactor
		l1['score'] = float(l1.get('score'))**(1.0/float(nfactor))
#iterate till length of the string and generate all possible value pairs
def consec(list1,list2):
	l = []
	for l1 in list1:
		for l2 in list2:
			
			if l1.get('file_name') == l2.get('file_name') and \
				l1.get('next') == l2.get('word') and \
				((l2.get('tbeg')) - (l1.get('tbeg')) - (l1.get('dur'))<=0.5) and \
				((l2.get('tbeg')) - (l1.get('tbeg')) - (l1.get('dur'))>-1e-5):
					
				d = {}
				d['file_name'] = l1.get('file_name')
				d['channel']  = l1.get('channel')
				d['next'] = l2.get('next')
				d['word'] = l1.get('word') +' '+l2.get('word')
				d['dur'] = l2.get('tbeg') - l1.get('tbeg') + l2.get('dur')
				d['score'] = (l2.get('score')*l1.get('score'))
				d['tbeg'] = l1.get('tbeg')
				l.append(d)
				break
				
	return l
			
			
class KeywordSpotter:
	"""Keyword Spotter class"""

	def _init_(self):
		pass
	def kws(self,d,q,kwlist_filename="IARPA-babel202b-v1.0d_conv-dev.kwlist.xml", language="swahili", system_id = ""):
		"""
		Takes a indexer dictionary as input and generates an xml string output
		Args
			d: a indexer dictionary
			q: a dictionary of queries
		Returns
			a string of kws xml file
		"""
		root = et.Element("kwslist",kwlist_filename=kwlist_filename, language=language, system_id=system_id)
		for kwid, k in q.items():
			kwele = et.SubElement(root,"detected_kwlist",kwid=str(kwid),oov_count="0",search_time="0.0")
			vlist = []
			for i in range(len(k)):
				if k[i] in d:
					vlist.append(d[k[i]])
			if len(vlist)==len(k):
				getlist = reduce(consec,vlist)
				normalise(getlist,float(len(k)))
				for g in getlist:
					temp = et.SubElement(kwele,"kw",file=g.get('file_name'),\
						channel=g.get('channel'),tbeg=str(g.get('tbeg')),\
						dur=str(g.get('dur')),score=str(g.get('score')),decision="YES")
		
		
		xmlstr = minidom.parseString(et.tostring(root)).toprettyxml(indent="\t")
		temp_list = xmlstr.split('\n')
		xmlstr = '\n'.join(temp_list[1:])
		#xmlstr = et.tostring(root,encoding="utf8",method="xml")
		return xmlstr
		pass
