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

# Setup error handling for this REST service
@app.errorhandler(TideError)
def handle_tide_error(error):
	response=jsonify(error.to_dict())
	response.status_code=error.status_code
	return response

# This route is only for testing, returns data for location and 4 days time span
@app.route('/')
def welcome():
        return """
        <h1>Welcome to bazTide!</h1>
        <p>This is REST API built around xTide application. You can try it out by switching URL to:</p>
        <code><em>/data/Miami/metadata</em></code>
        """
# This route is used for returning data for location and specified dates
@app.route('/data/<location>/tidedata', methods=['GET'])
def getTideDataByDate(location):
	start=request.args.get('start')
	end=request.args.get('end')
	try:
		data=dateDefined(location,start,end)
		logger.debug("Request has been successfully completed!")
		return jsonify(data)
	except TideError as error:
		raise
	except Exception as error:
		logger.exception(str(error))
		raise TideError("Unknown error!",status_code=400)
# This route is used for returing information about location.
@app.route('/data/<location>/metadata', methods=['GET'])
def getLocationData(location):
	try:
		data=detailDefined(location)
		logger.debug("Request has been successfully completed!")
		return jsonify(data)
	except TideError as error:
		logger.warning(str(error))
		raise
	except Exception as error:
		logger.exception(str(error))
		raise TideError("Unknown error!",status_code=400)
# This route is used for returning list of locations for searchbar
@app.route('/search/<chars>', methods=['GET'])
def getLocationList(chars):
	try:
       		data=locationList(chars)
       		logger.debug("Request has been successfully completed!")
       		return jsonify(data)
	except TideError as error:
		logger.warning(str(error))
		raise
	except Exception as error:
		logger.exception(str(error))
		raise TideError("Unknown error!",status_code=400)

if __name__=="__main__":
	app.run(debug=debugbool, host=os.getenv('HOST'), port=os.getenv('PORT'))
