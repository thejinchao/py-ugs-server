#-*- coding: utf-8 -*-
import json

g_XMLSchema = " xmlns:i=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns=\"http://schemas.datacontract.org/2004/07/MetadataServer.Models\""

class ResultData():
	def __init__(self):
		pass
	
	def ExportToXML(self, withSchema):
		output = "<{0}{1}>\n".format(type(self).__name__, g_XMLSchema if withSchema else "")
		for k,v in self.__dict__.items():
			if(v != None):
				output = output + "<{0}>{1}</{0}>\n".format(k, v)
			else :
				output = output + "<{0} i:nil=\"true\"/>\n".format(k)
		output = output + "</{0}>".format(type(self).__name__)
		return output
	
	def ExportToJson(self):
		return json.dumps(self.__dict__)
