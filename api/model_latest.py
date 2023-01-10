#-*- coding: utf-8 -*-

import result_data

class LatestData(result_data.ResultData):
	def __init__(self, _LastEventId, _LastCommentId, _LastBuildId):
		super(LatestData,self).__init__()
		
		self.LastEventId = _LastEventId
		self.LastCommentId = _LastCommentId
		self.LastBuildId = _LastBuildId
