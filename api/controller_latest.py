#-*- coding: utf-8 -*-
import db_connect
import pymysql
import model_latest

class LatestController:
	def GetLastIds(project):
		LastEventId=0
		LastCommentId=0
		LastBuildId=0
		
		#Get Last Event
		LastEventId = db_connect.fetchOneValue(
			("WITH user_votes AS (SELECT UserVotes.Id, UserVotes.Changelist FROM ugs_db.UserVotes "
			"INNER JOIN ugs_db.Projects ON Projects.Id = UserVotes.ProjectId "
			"WHERE Projects.Name LIKE '{0}' GROUP BY Changelist ORDER BY Changelist DESC LIMIT 100) "
			"SELECT * FROM user_votes ORDER BY user_votes.Changelist ASC LIMIT 1").format(project), 0, 0)
		
		#Get Last Comment 
		LastCommentId = db_connect.fetchOneValue(
			("WITH comments AS (SELECT Comments.Id, Comments.ChangeNumber FROM ugs_db.Comments "
			"INNER JOIN ugs_db.Projects ON Projects.Id = Comments.ProjectId "
			"WHERE Projects.Name LIKE '{0}' GROUP BY ChangeNumber ORDER BY ChangeNumber DESC LIMIT 100) "
			"SELECT * FROM comments ORDER BY comments.Id ASC LIMIT 1").format(project), 0, 0)
		
		#Get Last Build Id
		LastBuildId = db_connect.fetchOneValue(
			("WITH badges AS (SELECT Badges.Id, Badges.ChangeNumber FROM ugs_db.Badges " 
			"INNER JOIN ugs_db.Projects ON Projects.Id = Badges.ProjectId "
			"WHERE Projects.Name LIKE '{0}' GROUP BY ChangeNumber ORDER BY ChangeNumber DESC LIMIT 100) "
			"SELECT * FROM badges ORDER BY badges.ChangeNumber ASC LIMIT 1").format(project), 0, 0)
		
		return model_latest.LatestData(LastEventId, LastCommentId, LastBuildId)


