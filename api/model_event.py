#-*- coding: utf-8 -*-

import result_data

g_eventTypeString = [
	"Syncing",

	#Reviews
	"Compiles",
	"DoesNotCompile",
	"Good",
	"Bad",
	"Unknown",

	# Starred builds
	"Starred",
	"Unstarred",

	# Investigating events
	"Investigating",
	"Resolved"
]


class EventData(result_data.ResultData):
	def __init__(self, _Id, _Change, _UserName, _Type, _Project):
		super(EventData,self).__init__()
		
		self.Id = _Id
		self.Change = _Change
		self.UserName = _UserName
		self.Type = _Type
		self.Project = _Project
	
def getTypeString(intType):
	if(intType>=0 and intType<len(g_eventTypeString)):
		return g_eventTypeString[intType]
	return None
