#-*- coding: utf-8 -*-

import result_data

BR_Starting=0
BR_Failure=1
BR_Warning=2
BR_Success=3
BR_Skipped=4

g_buildResultString = [
	"Starting", 
	"Failure", 
	"Warning", 
	"Success", 
	"Skipped"
]

class BuildData(result_data.ResultData):
	def __init__(self, _Id, _ChangeNumber, _BuildType, _Result, _Url, _Project, _ArchivePath):
		super(BuildData,self).__init__()
		
		self.Id = _Id
		self.ChangeNumber = _ChangeNumber
		self.BuildType = _BuildType
		self.Result = _Result
		self.Url = _Url
		self.Project = _Project
		self.ArchivePath = _ArchivePath
		
def getResultString(intResult):
	if(intResult>=0 and intResult<len(g_buildResultString)):
		return g_buildResultString[intResult]
	return None
