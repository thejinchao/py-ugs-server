#-*- coding: utf-8 -*-
import db_connect
import pymysql
import model_event
import json

class EventController:
	def GetUserVotes(project, lastEventId):
		result=[]
		sql = ("SELECT UserVotes.Id, UserVotes.Changelist, UserVotes.UserName, UserVotes.Verdict, UserVotes.Project FROM ugs_db.UserVotes "
				"INNER JOIN ugs_db.Projects ON Projects.Id = UserVotes.ProjectId WHERE UserVotes.Id > {0} AND Projects.Name LIKE '%{1}%' ORDER BY UserVotes.Id").format(lastEventId, project)
		eventObjs = db_connect.fetchObjects(sql, None)
		for event in eventObjs :
			Id = event[0]
			Change = event[1]
			UserName = event[2]
			Type = event[3]
			Project=event[4]
			if(Type!=None and Type in model_event.g_eventTypeString and (Project==None or Project==project)):
				result.append(model_event.EventData(Id, Change, UserName, Type, Project))
		return result
	
	def PostEvent(eventData):
		change = eventData["Change"]
		userName = eventData["UserName"]
		verdict = model_event.getTypeString(eventData["Type"])
		project = eventData["Project"]
		projectId=db_connect.commonTryInsertAndGetProject(project)
		
		sql = "INSERT INTO ugs_db.UserVotes (Changelist, UserName, Verdict, Project, ProjectId) VALUES ({0}, '{1}', '{2}', '{3}', {4})".format(
				change, userName, verdict, project, projectId)
		return db_connect.executeSql(sql)
		