#-*- coding: utf-8 -*-

import result_data

class IssueData(result_data.ResultData):
	def __init__(self, _Id, _CreatedAt, _RetrievedAt, _Project, _Summary, _Owner, _NominatedBy, _AcknowledgedAt, _FixChange, _ResolvedAt, _bNotify):
		super(IssueData,self).__init__()
		
		self.Id = _Id
		self.CreatedAt = _CreatedAt
		self.RetrievedAt = _RetrievedAt
		self.Project = _Project
		self.Summary = _Summary
		self.Owner = _Owner
		self.NominatedBy = _NominatedBy
		self.AcknowledgedAt = _AcknowledgedAt
		self.FixChange = _FixChange
		self.ResolvedAt = _ResolvedAt
		self.bNotify = _bNotify

class IssueBuildData(result_data.ResultData):
	def __init__(self, _Id, _Stream, _Change, _JobName, _JobUrl, _JobStepName, _JobStepUrl, _ErrorUrl, _Outcome):
		super(IssueBuildData, self).__init__()
		
		self.Id = _Id
		self.Steam = _Steam
		self.Change = _Change 
		self.JobName = _JobName
		self.JobUrl = _JobUrl
		self.JobStepName = _JobStepName
		self.JobStepUrl = _JobStepUrl
		self.ErrorUrl = _ErrorUrl
		self.Outcome = _Outcome


class IssueDiagnosticData(result_data.ResultData):
	def __init__(self, _BuildId, _Message, _Url):
		super(IssueDiagnosticData, self).__init__()
		
		self.BuildId = _BuildId
		self.Message = _Message
		self.Url = _Url 
