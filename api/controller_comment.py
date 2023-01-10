#-*- coding: utf-8 -*-
import db_connect
import pymysql
import model_comment

class CommentController:
	def GetComments(project, lastCommentId):
		result=[]
		commentObjs = db_connect.fetchObjects(
			("SELECT Comments.Id, Comments.ChangeNumber, Comments.UserName, Comments.Text, Comments.Project FROM ugs_db.Comments " +
			"INNER JOIN ugs_db.Projects ON Projects.Id = Comments.ProjectId WHERE Comments.Id > {0} AND Projects.Name LIKE '%{1}%' ORDER BY Comments.Id").format(lastCommentId, project), None)
		for comment in commentObjs :
			Id = comment[0]
			ChangeNumber = comment[1]
			UserName = comment[2]
			Text = comment[3]
			Project = comment[4]
			result.append(model_comment.CommentData(Id, ChangeNumber, UserName, Text, Project))
		return result

	def PostComment(comment):
		ChangeNumber=comment["ChangeNumber"]
		UserName=comment["UserName"]
		Text=comment["Text"]
		Project=comment["Project"]
		ProjectId=db_connect.commonTryInsertAndGetProject(Project)
		
		sql = "INSERT INTO ugs_db.Comments (ChangeNumber, UserName, Text, Project, ProjectId) VALUES ({0}, '{1}', '{2}', '{3}', {4})".format(
				ChangeNumber, UserName, Text, Project, ProjectId)
		print(sql)
		return db_connect.executeSql(sql)
