from flask import Flask,request,jsonify,abort, Response
from flask_cors import CORS
import json,re
from backend import *

app=Flask(__name__)
CORS(app)


debugbool=os.getenv('DEBUG')
if debugbool.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh', 'da']:
        debugbool=True
else:
        debugbool=False

#This route is only for testing, returns data for location and 4 days time span
@app.route('/Location/<location>', methods=['GET'])
def getTideData(location):
	data=locationDefined(location)
	if(len(data)==0):
		abort(400, 'There is no data for requested parameters!')			#In case there is problem with response, return message and statuscode.
	else:
		return jsonify(data)								#Return json response if all is okay.
		
#This route is used for returning data for location and specified dates		
@app.route('/Location/Tidedata', methods=['GET'])
def getTideDataByDate():
	location=request.args.get('location')							#Get parameters from url using requests
	start=request.args.get('start')
	end=request.args.get('end')
	data=dateDefined(location,start,end)				
	if(len(data)==0):
		abort(400, 'There is no data for requested parameters!')			#In case there is problem with response, return message and statuscode.
	elif(data=="No"):									#This is used for one location, that can't be encoded.
		abort(404, 'There is no decode!')
	else:
		return jsonify(data)								#Return json response if all is okay
		
#This route is used for returing information about location.
@app.route('/Location/Metadata/<location>', methods=['GET'])				
def getLocationData(location):
	data=detailDefined(location)
	if(len(data)==0):
		abort(400, 'There is no data for requested parameters!')
	else:
		return jsonify(data)
		
#This route is used for returning list of locations for searchbar
@app.route('/Location/Locationlist/<chars>', methods=['GET'])
def getLocationList(chars):
	data=locationList(chars)
	return jsonify(data)


if __name__=="__main__":
	app.run(debug=debugbool, host=os.getenv('HOST'), port=os.getenv('PORT')>
