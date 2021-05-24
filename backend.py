import pandas as pd
import json,os,re,io
from datetime import datetime


#Return tide data for sent location. This functions is not used in app. It has default date range.

def locationDefined(location):
	output=os.popen('tide -l ' + location + ' -f c').read()					#CSV format
	buff=io.StringIO(output)									#Dataframe is expecting file, so we have to use StringIO to create buffer. 
	dataframe=pd.read_csv(buff,sep=",",names=["Location","Date","Time","Height","Tide"])	#Pandas, json format.
	result=dataframe.to_json(orient="records")
	data=json.loads(result)
	return data
	
	
#Return tide data for sent location, starting date, ending date.	

def dateDefined(location,start,end):
	if('½' in location):										#xTide can't decode ½, so app returns error when that location is asked.
		return "No"
	else:
		output=os.popen(f'tide -l "{location}" -b  "{start}" -e "{end}" -f c').read()		#CSV format
		buff=io.StringIO(output)
		dataframe=pd.read_csv(buff, sep=",", names=["Location","Date","Time","Height","Tide"])	# CSV --> Dataframe
		dataframe['Height'] = dataframe['Height'].fillna(0)						# null --> 0
		for index, row in dataframe.iterrows():
    			if isinstance(row['Height'],str):						# Parsing, removing unit string.
    				row['Height']=row['Height'].replace('ft','')				
    				row['Height']=row['Height'].replace('kt','')
    			row['Height']=float(row['Height'])
    		
    			timeTemp=row['Time'][0:8]							#Edit string, before parsing. Removing "EDT", spaces...
    			if(timeTemp.endswith(' ')):
    				timeTemp=timeTemp[:-1]
    			timeObject=datetime.strptime(timeTemp,'%I:%M %p')				#Parsing I --> Hour M --> Minute as a zero-padded decimal number. P- AM/PM. Also adds (yyyy-mm-dd)
    			row['Time']=timeObject.time()							#Removes (yyyy-mm-dd), only time remains in format (HH:MM:ss)				
    		
		result=dataframe.to_json(orient="records")						#Pandas u JSON, orient records
		data=json.loads(result)								# JSON u python DICTIONARY ??
		return data
	
#Return details about sent location.
 
def detailDefined(location):
	output=os.popen(f'tide -l "{location}" -m a').read()
	output=output.split("\n")
	for i in range(0,len(output),1):
		output[i]=re.sub('\s{2,}', '#', output[i], count=1)					#App uses minimum two spaces to organise data. Replacing multiple spaces with '#' using regex.
	output.pop()											#Remove last item from array, empty.
	data=dict(s.split('#') for s in output)							#Array to dicty, delimiter --> #.
	return data
	
	
#Returns list of filtered locations.

def locationList(chars):
	output=os.popen('tide -m l').read()								#List of all locations, separted by comma.
	listOfLocations=output.split("\n")
	firstSeparator='Sub'
	secondSeparator='Ref'
	del listOfLocations[0:2]									#Removing description from location, last string.
	del listOfLocations[-1]

	for i in range(0,len(listOfLocations),1):							#Loop through list of locations, removing coordinates and spaces.
		listOfLocations[i]=listOfLocations[i].split(firstSeparator,1)[0]
		listOfLocations[i]=listOfLocations[i].split(secondSeparator,1)[0]
		listOfLocations[i]=' '.join(listOfLocations[i].split())			
	
	
	#FILTER LOCATIONS USING CHARS SENT FROM SERVER.
	filteredList=[]
	for z in range(0,len(listOfLocations),1):
		temp=listOfLocations[z].lower() 							#Chars are lower, python is case-sens so lowering locations.
		if(temp.startswith(chars)):
			filteredList.append(listOfLocations[z])					#Appends locations that start with chars.

	filteredList = list(dict.fromkeys(filteredList))						#Removes duplicates
	dataframe=pd.DataFrame(filteredList, columns=["Name"])
	result=dataframe.to_json(orient="records")
	data=json.loads(result)
	return data

