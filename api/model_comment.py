#-*- coding: utf-8 -*-

import result_data

class CommentData(result_data.ResultData):
	def __init__(self, _Id, _ChangeNumber, _UserName, _Text, _Project):
		super(CommentData,self).__init__()
		
		self.Id = _Id
		self.ChangeNumber = _ChangeNumber
		self.UserName = _UserName
		self.Text = _Text
		self.Project = _Project

