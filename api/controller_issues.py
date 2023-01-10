#-*- coding: utf-8 -*-
import db_connect
import pymysql
import model_issues
import json

class IssuesController:
	def GetIssues(userName):
		return IssuesController.GetIssuesInternal(-1, userName, False, -1)
	
	def GetIssuesInternal(issueId, userName, includeResolved, numResults):
		userId=-1
		if(userName != None):
			userId=db_connect.commonFindOrAddUserId(userName)
		
		sql = "SELECT"
		sql += " Issues.Id, Issues.CreatedAt, UTC_TIMESTAMP(), Issues.Project, Issues.Summary, OwnerUsers.Name, NominatedByUsers.Name, Issues.AcknowledgedAt, Issues.FixChange, Issues.ResolvedAt"
		if(userName != None):
			sql += ", IssueWatchers.UserId"
		sql += " FROM ugs_db.Issues"
		sql += " LEFT JOIN ugs_db.Users AS OwnerUsers ON OwnerUsers.Id = Issues.OwnerId"
		sql += " LEFT JOIN ugs_db.Users AS NominatedByUsers ON NominatedByUsers.Id = Issues.NominatedById"
		if(userName != None):
			sql += " LEFT JOIN ugs_db.IssueWatchers ON IssueWatchers.IssueId = Issues.Id AND IssueWatchers.UserId = {0}".format(userId)
		
		if(issueId != -1):
			sql += " WHERE Issues.Id = {0}".format(issueId)
		elif(not includeResolved):
			sql += " WHERE Issues.ResolvedAt IS NULL"
				
		if(numResults > 0):
			sql += " ORDER BY Issues.Id DESC LIMIT {0}".format(numResults)
		result = []
		issueObjs = db_connect.fetchObjects(sql, None)
		for issue in issueObjs:
			Id = issue[0]
			CreateAt = issue[1].strftime('%Y-%m-%dT%H:%M:%S')
			RetrieveAt = issue[2].strftime('%Y-%m-%dT%H:%M:%S')
			Project = issue[3]
			Summary = issue[4]
			Owner = issue[5] #...
			NominatedBy = issue[6] #...
			AcknowledgeAt = issue[7].strftime('%Y-%m-%dT%H:%M:%S') if issue[7]!=None else None
			FixChange = int(issue[8])
			ResolvedAt = issue[9].strftime('%Y-%m-%dT%H:%M:%S') if issue[9]!=None else None
			bNotify = False
			if(userName != None):
				bNotify = True if (len(issue)>10 and issue[10]!=None) else False
			result.append(model_issues.IssueData(Id, CreateAt, RetrieveAt, Project, Summary, Owner, NominatedBy, AcknowledgeAt, FixChange, ResolvedAt, bNotify))
		return result
	
	def UpdateIssue(issueId, issueUpdateData):
		#print(issueUpdateData)
		kvDict = {}
		if("Summary" in issueUpdateData and issueUpdateData["Summary"]!=None) :
			kvDict["Summary"] = "'{0}'".format(issueUpdateData["Summary"])
			
		if("Owner" in issueUpdateData and issueUpdateData["Owner"]!=None) :
			kvDict["OwnerId"] = db_connect.commonFindOrAddUserId(issueUpdateData["Owner"])
			
		if("NominatedBy" in issueUpdateData and issueUpdateData["NominatedBy"]!=None) :
			kvDict["NominatedById"] = db_connect.commonFindOrAddUserId(issueUpdateData["NominatedBy"])
		
		if("Acknowledged" in issueUpdateData and issueUpdateData["Acknowledged"]==True) :
			kvDict["AcknowledgedAt"] = "UTC_TIMESTAMP()"
			
		if("FixChange" in issueUpdateData and issueUpdateData["FixChange"]!=None) :
			kvDict["FixChange"] = issueUpdateData["FixChange"]
		
		if("Resolved" in issueUpdateData and issueUpdateData["Resolved"]!=None) :
			kvDict["ResolvedAt"] = "UTC_TIMESTAMP()"
		
		sql = "UPDATE ugs_db.Issues SET "
		idx=0
		for key,value in kvDict.items():
			sql += "{0}={1}".format(key, value)
			if(idx < len(kvDict)-1):
				sql += ","
			idx = idx+1
		
		sql += " WHERE Id={0}".format(issueId)
		#print("sql='{0}'".format(sql))
		return db_connect.executeSql(sql)
	
	def AddIssue(issueData):
		ownerId=None
		if("Owner" in issueData and issueData["Owner"]!=None):
			ownerId = db_connect.commonFindOrAddUserId(issueData["Owner"])
		
		sql = "INSERT INTO ugs_db.Issues (Project, Summary, OwnerId, CreatedAt, FixChange) VALUES ('{0}', '{1}', {2}, UTC_TIMESTAMP(), 0)".format(
			issueData["Project"], issueData["Summary"], ownerId)
		return db_connect.executeSql_InsertRow(sql)


class IssueBuildsSubController:
	def GetBuilds(issueid):
		result = []
		sql = ("SELECT IssueBuilds.Id, IssueBuilds.Stream, IssueBuilds.Change, IssueBuilds.JobName, IssueBuilds.JobUrl, IssueBuilds.JobStepName,"
				" IssueBuilds.JobStepUrl, IssueBuilds.ErrorUrl, IssueBuilds.Outcome FROM ugs_db.IssueBuilds WHERE IssueBuilds.IssueId = {0}").format(issueid)
		issueBuilds = db_connect.fetchObjects(sql, None)
		for build in issueBuilds:
			Id = issue[0]
			Stream = issue[1]
			Change = issue[2]
			JobName = issue[3]
			JobUrl = issue[4]
			JobStepName = issue[5]
			JobStepUrl = issue[6]
			ErrorUrl = issue[7]
			Outcome = issue[8]
			result.append(model_issues.IssueBuildData(Id, Stream, Change, JobName, JobUrl, JobStepName, JobStepUrl, ErrorUrl, Outcome))
		return result

class IssueDiagnosticsSubController:
	def GetDiagnostics(issueid):
		result = []
		sql = ("SELECT BuildId, Message, Url FROM ugs_db.IssueDiagnostics"
				" WHERE IssueDiagnostics.IssueId = {0}").format(issueid)
		issueDiagnostics = db_connect.fetchObjects(sql, None)
		for diagnostics in issueDiagnostics:
			BuildId = issue[0]
			Message = issue[1]
			Url = issue[1]
			result.append(model_issues.IssueDiagnosticData(BuildId, Message, Url))
		return result
	
	def AddDiagnostic(issueid, issueDiagnosticData):
		print("issueDiagnosticData={0}".format(issueDiagnosticData))
		
		buildId=None
		if("BuildId" in issueDiagnosticData and issueDiagnosticData["BuildId"]!=None):
			buildId = issueDiagnosticData["BuildId"]
		
		sql = "INSERT INTO ugs_db.IssueDiagnostics (IssueId, BuildId, Message, Url) VALUES ({0}, {1}, '{2}', '{3}')".format(
			issueid, 
			buildId if buildId!=None else 'NULL', 
			db_connect.sanitizeText(issueDiagnosticData["Message"], 1000), 
			issueDiagnosticData["Url"])
		print(sql)
		return db_connect.executeSql_InsertRow(sql)


