#-*- coding: utf-8 -*-

'''
python -m pip install --upgrade pip
pip install flask dbutils cryptography pymysql
'''
import sys
import pymysql
import json
import os
from flask import Flask, make_response, request
from gevent import pywsgi

import result_data

from controller_latest import LatestController
from model_latest import LatestData

from controller_comment import CommentController
from model_comment import CommentData

from controller_build import BuildController
from model_build import BuildData

from controller_issues import IssuesController, IssueBuildsSubController, IssueDiagnosticsSubController
from model_issues import IssueData, IssueBuildData, IssueDiagnosticData

from controller_event import EventController
from model_event import EventData

app = Flask(__name__)

def make_json_response(result):
	responseString = ""
	
	if(isinstance(result, list)):
		responseString+="["
		for i in range(len(result)):
			responseString += result[i].ExportToJson()
			responseString += "," if i<len(result)-1 else ""
		responseString+="]"
	else:
		responseString = result.ExportToJson()
	response = make_response(responseString)
	response.headers['Content-Type']='application/json; charset=utf-8'
	return response

def make_xml_response(result, dataTypeName):
	responseString = ""
	
	if(isinstance(result, list)):
		responseString += "<ArrayOf{0}{1}>\n".format(dataTypeName, result_data.g_XMLSchema)
		for item in result:
			responseString += item.ExportToXML(False)
		responseString += "</ArrayOf{0}>".format(dataTypeName)
	else:
		responseString = result.ExportToXML(True)
	response = make_response(responseString)
	response.headers['Content-Type']='application/xml; charset=utf-8'
	return response

@app.route("/")
def hello_world():
	return("<html>" + "UnrealGameSync Metadata Server(Python Version)" + "</html>")

###############################################################################
# /api/latest
# LatestController
###############################################################################
@app.route("/api/latest")
def latest_route():
	project=request.args.get('project')
	result = LatestController.GetLastIds(project)
	
	if(request.content_type == "application/json"):
		return make_json_response(result)
	else:
		return make_xml_response(result, LatestData.__name__)

###############################################################################
# /api/comment
# CommentController
###############################################################################
@app.route("/api/comment", methods=["GET"])
def get_comment_route():
	project=request.args.get('project')
	lastcommentid=request.args.get('lastcommentid')
	result = CommentController.GetComments(project, lastcommentid)
	
	if(request.content_type == "application/json"):
		return make_json_response(result)
	else:
		return make_xml_response(result, CommentData.__name__)

@app.route("/api/comment", methods=["POST"])
def post_comment_route():
	comment = json.loads(request.data.decode('utf-8'))
	CommentController.PostComment(comment)
	return ""

###############################################################################
# /api/build
# BuildController
###############################################################################
@app.route("/api/build", methods=["GET"])
def get_build_route():
	result=[]
	project=request.args.get('project')
	
	if('lastbuildid' in request.args) :
		lastbuildid=request.args.get('lastbuildid')
		result = BuildController.GetBuilds(project, lastbuildid)
	elif('buildtype' in request.args) :
		buildtype=request.args.get('buildtype')
		if('changenumber' in request.args):
			changenumber=request.args.get('changenumber')
			result = BuildController.GetBuildsWithBuildTypeAndChangeNumber(project, buildtype, changenumber)
		else:
			result = BuildController.GetBuildsWithBuildType(project, buildtype)
		
	if(request.content_type == "application/json"):
		return make_json_response(result)
	else:
		return make_xml_response(result, BuildData.__name__)

@app.route("/api/Build", methods=["POST"])
def post_build_route():
	buildData = json.loads(request.data.decode('utf-8'))
	BuildController.PostBuild(buildData)
	return ""

###############################################################################
# /api/issues
# IssuesController
###############################################################################
@app.route("/api/issues", methods=["GET"])
def get_issues_route():
	user=request.args.get('user')
	result = IssuesController.GetIssues(user)
	
	if(request.content_type == "application/json"):
		return make_json_response(result)
	else:
		return make_xml_response(result, IssueData.__name__)

@app.route("/api/issues", methods=["POST"])
def post_issues_route():
	issueData = json.loads(request.data.decode('utf-8'))
	issueId = IssuesController.AddIssue(issueData)
	return "" #TODO:return issueId

@app.route("/api/issues/<int:issueid>", methods=["PUT"])
def put_issue_route(issueid):
	issueUpdateData = json.loads(request.data.decode('utf-8'))
	IssuesController.UpdateIssue(issueid, issueUpdateData)
	return ""

###############################################################################
# /api/issues/<int:issueid>/builds
# IssueBuildsSubController
###############################################################################
@app.route("/api/issues/<int:issueid>/builds", methods=["GET"])
def get_issue_builds_sub_route(issueid):
	result = IssueBuildsSubController.GetBuilds(issueid)
	
	if(request.content_type == "application/json"):
		return make_json_response(result)
	else:
		return make_xml_response(result, IssueBuildData.__name__)

###############################################################################
# /api/issues/<int:issueid>/diagnostics
# IssueDiagnosticsSubController
###############################################################################
@app.route("/api/issues/<int:issueid>/diagnostics", methods=["GET"])
def get_issue_diagnostics_sub_route(issueid):
	result = IssueDiagnosticsSubController.GetDiagnostics(issueid)
	
	if(request.content_type == "application/json"):
		return make_json_response(result)
	else:
		return make_xml_response(result, IssueDiagnosticData.__name__)

@app.route("/api/issues/<int:issueid>/diagnostics", methods=["POST"])
def post_issue_diagnostics_sub_route(issueid):
	issueDiagnosticData = json.loads(request.data.decode('utf-8'))
	diagnosticId = IssueDiagnosticsSubController.AddDiagnostic(issueid, issueDiagnosticData)
	return ""

###############################################################################
# /api/event
# EventController
###############################################################################
@app.route("/api/event", methods=["GET"])
def get_event_route():
	project=request.args.get('project')
	lasteventid=request.args.get('lasteventid')
	result = EventController.GetUserVotes(project, lasteventid)
	
	if(request.content_type == "application/json"):
		return make_json_response(result)
	else:
		return make_xml_response(result, EventData.__name__)

@app.route("/api/event", methods=["POST"])
def post_event_route():
	eventData = json.loads(request.data.decode('utf-8'))
	EventController.PostEvent(eventData)
	return ""

###############################################################################
# Main
###############################################################################
if __name__=='__main__':
	str_listen_port = os.getenv("UGS_LISTEN_PORT", "5001")
	listen_port=int(str_listen_port)
	
	pywsgi.WSGIServer(('0.0.0.0', listen_port), app).serve_forever()
