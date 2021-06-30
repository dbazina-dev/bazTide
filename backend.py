import pandas as pd
import json,os,re,io,logging
from datetime import datetime
from subprocess import PIPE, Popen


logbool=os.getenv('LOG')
if logbool.upper() not in ['DEBUG','INFO','WARNING','ERROR','CRITICAL']:
        logbool="INFO"


# Logger used for printing information about processes inside application. Application also used default Flask/Werkzeug logger.
logger=logging.getLogger('tide_logger')
logging.basicConfig(
      level=logbool,											# Log level, it could be changed by swaping ENV variable "LOG".
      format='%(asctime)s %(levelname)-8s %(message)s [%(name)s : %(module)s : %(funcName)s : %(lineno)d]',
      datefmt='%Y-%m-%d %H:%M:%S')

# Generic error class used for REST error handling
class TideError(Exception):
    def __init__(self, message, status_code=400, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload
    def to_dict(self):												# Used for creating dictionary, later dictionary is used to transform in JSON.
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

# Function for obtaining tide data within time period.
def dateDefined(location,start,end):
	if("rincon p" in location.lower()):									# This location can't be decoded in CSV format.
		logger.info("Requested location can't be decoded. Location: "+location)
		raise TideError("Requested location can't be decoded!",status_code=400)
	elif(start!=None and end==None):									# Branching depending on provided parameters. xTide function is called based on params.												# If end date is none, set it as empty string. Used for concatenation.
		p = Popen(f'tide -l "{location}" -b  "{start}" -f c', shell=True, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate()
	elif(start==None and end!=None):
		p = Popen(f'tide -l "{location}" -e "{end}" -f c', shell=True, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate()
	elif (start==None and end==None):
		p = Popen(f'tide -l "{location}" -f c', shell=True, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate()
	else:
		p = Popen(f'tide -l "{location}" -b  "{start}" -e "{end}" -f c', shell=True, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate()

	stdout=stdout.decode('utf-8')										# Decoding python bytes class to string class.
	stderr=stderr.decode('utf-8')
	stderr=stderr.split("\n")										# Editing error output, parsing from string to array based on "\n"

	if("Indexing /usr/share/xtide/harmonics-dwf-20100529-free.tcd..." in stderr and "Indexing /usr/share/xtide/harmonics-initial.tcd..." in stderr):
		stderr.remove("Indexing /usr/share/xtide/harmonics-dwf-20100529-free.tcd...")		# Editing error output, removing unnecessary lines.
		stderr.remove("Indexing /usr/share/xtide/harmonics-initial.tcd...")
		if("Tide Warning:  swapping begin and end times" in stderr):
			stderr.remove("Tide Warning:  swapping begin and end times")
	stderr=stderr[0]											# First element of array contains information about error.

	if(stdout!="" and stderr==""):
		buff=io.StringIO(stdout)
		dataframe=pd.read_csv(buff, sep=",", names=["Location","Date","Time","Height","Tide"])  	# CSV --> Dataframe
		dataframe['Height'] = dataframe['Height'].fillna(0)                                     	# null --> 0
		for index, row in dataframe.iterrows():
			if isinstance(row['Height'],str):                                               	# Parsing, removing "Meausring unit" string.
				row['Height']=row['Height'].replace('ft','')
				row['Height']=row['Height'].replace('kt','')
			row['Height']=float(row['Height'])

			timeTemp=row['Time'][0:8]                                                       	# Edit string, before parsing. Removing "EDT", spaces...
			if(timeTemp.endswith(' ')):
				timeTemp=timeTemp[:-1]
			timeObject=datetime.strptime(timeTemp,'%I:%M %p')                               # Parsing I --> Hour M --> Minute as a zero-padded decimal number. P- AM/PM. Also adds (yyyy-mm-dd)
		row['Time']=timeObject.time()                                                   		# Removes (yyyy-mm-dd), only time remains in format (HH:MM:ss)

		result=dataframe.to_json(orient="records")                                              	# Pandas -> JSON, orient records.
		data=json.loads(result)                                                         		# JSON -> python DICTIONARY .
		return data
	elif(stdout=="" and stderr=="XTide Error:  STATION_NOT_FOUND"):					# ERROR HANDLING!
		logger.warning("Requested station was not found in harmonic files. Station: " + location)
		raise TideError("Requested location is not defined in harmonic files!",status_code=400)		# Stations that is not defined in harmonic files.
	elif(stdout=="" and stderr==""):
		if(start==None):
			logger.warning("There is no data within time period. End: "+ end)
		elif(end==None):
			logger.warning("There is no data within time period. Start: " + start)
		else:
			logger.warning("There is no data within time period. Start: " + start +". End: "+ end)
		raise TideError("There is no data within time period!",status_code=400)			# No data for time period.
	elif(stdout=="" and stderr=="XTide Fatal Error:  BAD_TIMESTAMP"):
		if(start==None):
			logger.warning("Date format is not valid. End: "+ end)
		elif(end==None):
			logger.warning("Date format is not valid. Start: " + start)
		else:
			logger.warning("Date format is not valid. Start: " + start +". End: "+ end)
		raise TideError("Date format is not valid! It should look like: YYYY-MM-DD hh:mm.", status_code=400)
	elif(stdout=="" and stderr=="XTide Fatal Error:  BAD_OR_AMBIGUOUS_COMMAND_LINE"):
		logger.warning("Bad format of command line that is used to fetch data from xtide.")
		raise TideError("Command line format is not valid. Command line is used to fetch data from xtide!", status_code=400)	# Broken command for fetching data from xTide.
	elif(stdout=="" and stderr=="XTide Fatal Error:  NO_HFILE_IN_PATH"):
		logger.warning("Harmonic files have been deleted or corrupted.")
		raise TideError("Harmonic files have been deleted or corrupted.!", status_code=400)	# Deleted harmonic files.
	else:
		logger.error("Unknown xtide error.")
		raise TideError("Unknown xtide error!",status_code=400)					# Any other error.

# Function for obtaining tide data within time period.
def detailDefined(location):
	p = Popen(f'tide -l "{location}" -m a', shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()
	stdout=stdout.decode('utf-8')
	stderr=stderr.decode('utf-8')
	stderr=stderr.split("\n")

	if("Indexing /usr/share/xtide/harmonics-dwf-20100529-free.tcd..." in stderr and "Indexing /usr/share/xtide/harmonics-initial.tcd..." in stderr):
                stderr.remove("Indexing /usr/share/xtide/harmonics-dwf-20100529-free.tcd...")
                stderr.remove("Indexing /usr/share/xtide/harmonics-initial.tcd...")
	stderr=stderr[0]

	if(stdout!="" and stderr==""):
		stdout=stdout.split("\n")
		for i in range(0,len(stdout),1):
                	stdout[i]=re.sub('\s{2,}', '#', stdout[i], count=1)                             # App uses minimum two spaces to organise data. Replacing multiple spaces with '#' using regex.
		stdout.pop()                                                                            	# Remove last item from array, empty.
		data=dict(s.split('#') for s in stdout)                                                 	# Array to dicty, delimiter --> #.
		return data
	elif(stdout=="" and stderr=="XTide Error:  STATION_NOT_FOUND"):					# ERROR HANDLING! 
		raise TideError("Requested location is not defined in harmonic files!",status_code=400)
	elif(stdout=="" and stderr=="XTide Fatal Error:  BAD_OR_AMBIGUOUS_COMMAND_LINE"):
                raise TideError("Command line format is not valid. Command line is used to fetch data from xtide!", status_code=400)
	elif(stdout=="" and stderr=="XTide Fatal Error:  NO_HFILE_IN_PATH"):
                raise TideError("Harmonic files have been deleted or corrupted.", status_code=400)
	else:
                raise TideError("Unknown xTide error!",status_code=400)

# Function for obtaining list of locations that start with defined characters.
def locationList(chars):
	p = Popen("tide -m l", shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()
	stdout=stdout.decode('utf-8')
	stderr=stderr.decode('utf-8')
	stderr=stderr.split("\n")

	if("Indexing /usr/share/xtide/harmonics-dwf-20100529-free.tcd..." in stderr and "Indexing /usr/share/xtide/harmonics-initial.tcd..." in stderr):
		stderr.remove("Indexing /usr/share/xtide/harmonics-dwf-20100529-free.tcd...")
		stderr.remove("Indexing /usr/share/xtide/harmonics-initial.tcd...")
	stderr=stderr[0]

	if(stdout!="" and stderr==""):
		listOfLocations=stdout.split("\n")
		firstSeparator='Sub'
		secondSeparator='Ref'
		del listOfLocations[0:2]                                                                        # Removing description from location, last string.
		del listOfLocations[-1]

		for i in range(0,len(listOfLocations),1):                                                       # Loop through list of locations, removing coordinates and spaces.
		        listOfLocations[i]=listOfLocations[i].split(firstSeparator,1)[0]
		        listOfLocations[i]=listOfLocations[i].split(secondSeparator,1)[0]
		        listOfLocations[i]=' '.join(listOfLocations[i].split())

		#FILTER LOCATIONS USING CHARS SENT FROM SERVER.
		filteredList=[]
		for z in range(0,len(listOfLocations),1):
		        temp=listOfLocations[z].lower()                                                         # Chars are lower, python is case-sens so lowering locations.
		        if(temp.startswith(chars.lower())):
		                filteredList.append(listOfLocations[z])                                 	   # Appends locations that start with chars.

		filteredList = list(dict.fromkeys(filteredList))                                                # Removes duplicates by parsing to dict. Dict can't have to same keys.
		dataframe=pd.DataFrame(filteredList, columns=["Name"])
		result=dataframe.to_json(orient="records")
		data=json.loads(result)
		return data
	elif(stdout=="" and stderr=="XTide Fatal Error:  BAD_OR_AMBIGUOUS_COMMAND_LINE"):			     # ERROR HANDLING !
		raise TideError("Command line format is not valid. Command line is used to fetch data from xtide!", status_code=400)
	elif(stdout=="" and stderr=="XTide Fatal Error:  NO_HFILE_IN_PATH"):
		raise TideError("Harmonic files have been deleted or corrupted.", status_code=400)
	else:
		raise TideError("Unknown xTide error!",status_code=400)
