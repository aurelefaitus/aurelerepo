#-------------------------------------------------------------------
#
# Copyright (C) Liberty Mutual Group
# 
# All rights reserved
#
#
#
# File : $Source$
#
# Description : Helper Module containing functions to update the Oracle Data Source
#								URL and Update Authentication Data.
#								All functions assume that the 
#								caller will take responsibility for saving
#								changes
#
#
#
# History :
# $Header$
#
# $Log$
# 
##-----------------------------------------------------------

##-----------------
# Imports
##-----------------
import sys, java, re, javax, org, org.w3c.dom.NodeList, org.w3c.dom.Element
import javax.xml.parsers.DocumentBuilderFactory
import javax.xml.parsers.DocumentBuilder
import org.xml.sax.SAXException
import org.xml.sax.SAXParseException
import javax.xml.xpath.XPath
import javax.xml.xpath.XPathFactory 
import javax.xml.xpath.XPathConstants


##-----------------
# Global Variables
##-----------------
lineSeparator = java.lang.System.getProperty('line.separator')
lineStartChar = "> "
SUCCESS = 0
FAIL = 1
TRUE = 1
FALSE = 0

##-----------------
# Classes
##-----------------

##----------------------------------------------------------------------
# Name: ArgStorage
# Description: Stores arguments passed into the Application
##----------------------------------------------------------------------

class ArgStorage:
	filePath = ""
	toggle = ""
	disableDatasourceUpdate = FALSE
	disableAuthenticationUpdate = FALSE
	
	def __init__(self, fPath, t, disDatasource, disAuth):
		self.filePath = fPath
		self.toggle = t
		self.disableDatasourceUpdate = disDatasource
		self.disAuthenticationUpdate = disAuth
#end class ArgStorage

##----------------------------------------------------------------------
# Name: AuthenticationID
# Description: Key and Values for JAAS Authentication
##----------------------------------------------------------------------

class AuthenticationID:
	aliasName = ""
	databasePassword = ""
	
	def __init__(self, aName, dPass):
		self.aliasName = aName
		self.databasePassword = dPass
#end class AuthenticationID

##----------------------------------------------------------------------
# Name: DataSourceInfo
# Description: Key and Values for DataSourceInfo
##----------------------------------------------------------------------

class DataSourceInfo:
	datasourceURL = ""
	datasourceName = []
	
	def __init__(self, dURL, dName):
		self.datasourceURL = dURL
		self.datasourceName = dName
#end class DataSourceInfo

##----------------------------------------------------------------------
# Name: DatabaseSettings
# Description: 
##----------------------------------------------------------------------
class DatabaseSettings:
	dataSourceList = []
	authDataList = []
	
	def __init__(self, dSourceList, authList):
		self.dataSourceList = dSourceList
		self.authDataList = authList
#end class DatabaseSettings


##-----------------
# Functions
##-----------------

##----------------------------------------------------------------------
# Name: displayDataSource
# Description: Display only function
#		for showing existing Data Sources
##----------------------------------------------------------------------			
def displayDataSource():
	global AdminConfig
	
	print "<- Data Sources ->"
	
	try:
		sec = AdminConfig.getid("/Cell:/")
		
		# Display Providers and Data Sources
		
		providerList = AdminConfig.list("JDBCProvider", sec)
		providerListSeparated = providerList.split(lineSeparator)
		for element in providerListSeparated[:]:
			print "JDBCProvider Name: " + AdminConfig.showAttribute(element, 'name')
			providerName = AdminConfig.showAttribute(element, 'name');
			
			if(providerName == "Oracle JDBC Driver" or providerName == "Oracle JDBC Driver (XA)"):			
				dataSourceList = AdminConfig.list('DataSource', element).splitlines()
				for dataSource in dataSourceList:
					print "Data Source: " + AdminConfig.showAttribute(dataSource, 'name') 
					propertySet = AdminConfig.showAttribute(dataSource, 'propertySet')
					propertyList = AdminConfig.list('J2EEResourceProperty', propertySet).splitlines()
					for prop in propertyList:
						if (AdminConfig.showAttribute(prop, 'name') == 'URL'):
							print "URL Value: " + AdminConfig.showAttribute(prop, 'value')
		return SUCCESS
	except Exception, e:
		print e
		return FAIL
#end def displayDataSource

##----------------------------------------------------------------------
# Name: displayAlias
# Description: Display only function
#		for showing existing Alias Names
##----------------------------------------------------------------------			
def displayAlias():
	global AdminConfig
	print "<- Displaying Alias Names ->"
	try:
		sec = AdminConfig.getid("/Cell:/")
	
		# Display Aliases
		
		authList = AdminConfig.list("JAASAuthData", sec)
		authListSeparated = authList.split(lineSeparator)
		for element in authListSeparated[:]:
			print "Alias Name: " + AdminConfig.showAttribute(element, 'alias')
		
		return SUCCESS
	except Exception, e:
		print e
		return FAIL
#end def displayAlias

##----------------------------------------------------------------------
# Name: displayDataSourceAndAlias
# Description: Display only function
#		for showing existing Data Sources
#		for showing existing Alias Names
##----------------------------------------------------------------------			
def displayDataSourceAndAlias():
	global AdminConfig
	print "<- Displaying Providers and Data Sources ->"
	try:
		result1 = displayDataSource()
		result2 = displayAlias()
		if(result1 == SUCCESS and result2 == SUCCESS):
			return SUCCESS
	except Exception, e:
		print e
		return FAIL
#end def displayDataSourceAndAlias

##----------------------------------------------------------------------
# Name: updateOracleDataSource
# Description: Helper function for updating Oracle Datasource on the 
#	       server for Old or New Database
##----------------------------------------------------------------------			
def updateOracleDataSource(inputDatasourceList):
	global AdminConfig
	returnValue = FAIL
	print "<- Updating Data Sources ->"
	
	try:
		if (inputDatasourceList == None or len(inputDatasourceList) == 0):
			print " - No Data Sources updated"
			returnValue = SUCCESS
		else:			
			successMessage = ' -     updateOracleDataSource: Pending SAVE --- Data Source URL updated'
			errorMessage = ' -     updateOracleDataSource: ERROR --- Data Source URL update failed.  Check the logs for more information.'
			
			sec = AdminConfig.getid("/Cell:/")
			JDBCProviderList = AdminConfig.list("JDBCProvider", sec)
			JDBCProviderListSeparated = JDBCProviderList.split(lineSeparator)
			for element in JDBCProviderListSeparated[:]:
				providerName = AdminConfig.showAttribute(element, 'name');
				
				if(providerName == "Oracle JDBC Driver" or providerName == "Oracle JDBC Driver (XA)"):			
					dataSourceList = AdminConfig.list('DataSource', element).splitlines()
					for dataSource in dataSourceList:
						propertySet = AdminConfig.showAttribute(dataSource, 'propertySet')
						propertyList = AdminConfig.list('J2EEResourceProperty', propertySet).splitlines()
						for prop in propertyList:
							if (AdminConfig.showAttribute(prop, 'name') == 'URL'):
								URLbefore = AdminConfig.showAttribute(prop, 'value')
								for data in inputDatasourceList[:]:
									for name in data.datasourceName[:]:
										if (AdminConfig.showAttribute(dataSource, 'name') == name):
											if (AdminConfig.modify(prop, '[[value ' + data.datasourceURL + ']]') == ""):
												URLafter = AdminConfig.showAttribute(prop, 'value')
												print AdminConfig.showAttribute(dataSource, 'name')  + successMessage
												print "\tURL Before --- " + URLbefore
												print "\tURL After --- " + URLafter
											else:
												raise Exception(AdminConfig.showAttribute(dataSource, 'name')  + errorMessage)
			returnValue = SUCCESS

	except Exception, e:
		print e
	return returnValue
#end def createOracleDataSource

##----------------------------------------------------------------------
# Name: updateAuthentication
# Description: get all the data in the XML Config file and update the Admin Console
##----------------------------------------------------------------------

def updateAuthentication(authDataList):
	global AdminConfig
	print "<- Updating Authentication Sources ->"
	returnValue = FAIL
	try:
		if (authDataList == None or len(authDataList) == 0):
			print " - No Authentication Data updated"
			returnValue = SUCCESS
		else:			
			successMessage = ' -     updateAuthentication: Pending SAVE --- Password updated'
			errorMessage = ' -     updateAuthentication: ERROR --- Password update failed.  Check the logs for more information.'
			
			sec = AdminConfig.getid("/Cell:/")
			JAASAuthDataList = AdminConfig.list("JAASAuthData", sec).split(lineSeparator)
			for element in JAASAuthDataList[:]:
				for data in authDataList[:]:
					if (AdminConfig.showAttribute(element, 'alias') == data.aliasName):
						if (AdminConfig.modify(element, '[[password ' + data.databasePassword + ']]') == ""):
							print data.aliasName + successMessage
						else:
							raise Exception(data.aliasName + errorMessage)
			returnValue = SUCCESS

	except Exception, e:
		print e
	return returnValue
#end def updateAuthentication

##----------------------------------------------------------------------
# Name: testFilePath
# Description: Test whether file exists or not
##----------------------------------------------------------------------
def testFilePath (filePath):
	if (filePath is None):
		return FALSE
	inputFile = java.io.File(filePath)
	if (inputFile.exists() == 1 and inputFile.isDirectory() == 0):
		return TRUE
	return FALSE
#end def testFilePath

##----------------------------------------------------------------------
# Name: loadArgs
# Description: Validate and load arguments passed in
##----------------------------------------------------------------------	
def loadArgs (argv):
	filePath = None
	toggle = None
	disableDatasourceUpdate = FALSE
	disAuthenticationUpdate = FALSE
	if(len(argv) > 0):
		if((len(argv) % 2)  != 0):
			raise Exception("Invalid number of Arguments")
		numLoop = len(argv)/2
		for ctr in range(0,numLoop):
			key = argv[ctr*2]
			value = argv[(ctr*2) + 1]
			if(key == "-filepath"):
				filePath = value
			elif(key == "-toggle"):
				toggle = value
			elif(key == "-disable"):
				if(value == "DatasourceUpdate"):
					disableDatasourceUpdate = TRUE
				elif(value == "AuthenticationUpdate"):
					disAuthenticationUpdate = TRUE
				else:
					raise Exception("Unknown disable value: " + value)
			else:
				raise Exception("Unknown argument: " + key)
		
		if(filePath == None):
			raise Exception("-filepath not found.")
		if(toggle == None):
			raise Exception("-toggle not found.")
		if(disableDatasourceUpdate == TRUE):
			print "> - Update Data source -- disabled."
		else:
			print "> - Update Data source -- enabled."
		if(disAuthenticationUpdate == TRUE):
			print "> - Update Authentication Data -- disabled."
		else:
			print "> - Update Authentication Data -- enabled."
	return ArgStorage(filePath, toggle, disableDatasourceUpdate, disAuthenticationUpdate)
#end def loadArgs

##----------------------------------------------------------------------
# Name: loadSettings
# Description: Read in the configuration file settings
#		load values into class
##----------------------------------------------------------------------	
def loadSettings (loadPath, toggle):
	loadedClass = None
	xPathExpression = "/data/toggle[@id='"+str(toggle)+"']"
	xDataSourceExpression = xPathExpression+ "/DataSourceList/DataSourceInfo"
	xJaasExpression = xPathExpression + "/JAASAuthData/authData"
	datasourceList = []
	authList= []
	
	if(testFilePath(loadPath) == TRUE):
		print lineStartChar + "loading configuration file"
		xmlDataSourceConfig = java.io.File(loadPath)
		dbFactory = javax.xml.parsers.DocumentBuilderFactory.newInstance()
		dBuilder = dbFactory.newDocumentBuilder()
		doc = dBuilder.parse(xmlDataSourceConfig)
		doc.getDocumentElement().normalize()
		
		xpath = javax.xml.xpath.XPathFactory.newInstance().newXPath()
		expr = xpath.compile(xPathExpression)
		nList = expr.evaluate(doc, javax.xml.xpath.XPathConstants.NODESET)
		
		if(nList.getLength() == 0):
			raise Exception("Toggle not found")
		elif(nList.getLength() > 1):
			raise Exception("Multiple Toggles found.")
		else:
			# get datasource
			expr = xpath.compile(xDataSourceExpression)
			nList1 = expr.evaluate(doc, javax.xml.xpath.XPathConstants.NODESET)
 			
			if(nList1.getLength() > 0):
				for n2 in range(0,nList1.getLength()):
					datasourceChildNode = nList1.item(n2)
					if(datasourceChildNode.hasChildNodes()):
						datasourceElementNodes = datasourceChildNode.getChildNodes()
						childURL = ""
						childName = []
						for n3 in range(0,datasourceElementNodes.getLength()):
							datasourceChildNode = datasourceElementNodes.item(n3)
							if (datasourceChildNode.getNodeName() == "URL"):
								childURL = datasourceChildNode.getTextContent()
							if (datasourceChildNode.getNodeName() == "SourceNamesList"):
								datasourceNameListNodes = datasourceChildNode.getChildNodes()
								for n4 in range(0,datasourceNameListNodes.getLength()):
									datasourceNamesListChildNode = datasourceNameListNodes.item(n4)
									if (datasourceNamesListChildNode.getNodeName() == "name"):
										childName.append(datasourceNamesListChildNode.getTextContent())
						datasourceList.append(DataSourceInfo(childURL, childName))
			else:
				print "No datasource loaded."
			# get auth data
			expr = xpath.compile(xJaasExpression)
			nList2 = expr.evaluate(doc, javax.xml.xpath.XPathConstants.NODESET)
			if(nList2.getLength() > 0):
				for n2 in range(0,nList2.getLength()):
					jaasAuthChildNode = nList2.item(n2)
					if(jaasAuthChildNode.hasChildNodes()):
						authdataElementNodes = jaasAuthChildNode.getChildNodes()
						childAlias = ""
						childPassword = ""
						for n3 in range(0,authdataElementNodes.getLength()):
							authdataChildNode = authdataElementNodes.item(n3)
							if (authdataChildNode.getNodeName() == "aliasName"):
								childAlias = authdataChildNode.getTextContent()
							if (authdataChildNode.getNodeName() == "password"):
								childPassword = authdataChildNode.getTextContent()
						authList.append(AuthenticationID(childAlias, childPassword))
			else:
				print "No Auth data loaded."
			loadedClass = DatabaseSettings(datasourceList, authList)
	else:
		raise Exception("Could not find file")
		
	return loadedClass	
#end def loadSettings

#-----------------------------------------------------------------
# Main
#-----------------------------------------------------------------
def main(argv):
	global AdminConfig
	try:
		step1 = FAIL
		step2 = FAIL
		returnValue = FAIL
		
		argResults = loadArgs(argv)
		
		if ((argResults == None) or (argResults.filePath == None and argResults.toggle == None)):
			print lineStartChar + "Running in Demo Mode"
			displayDataSourceAndAlias()
			returnValue = SUCCESS
		else:
			print lineStartChar + "filepath: " + argResults.filePath
			print lineStartChar + "toggle: " + argResults.toggle
			
			settings = loadSettings(argResults.filePath, argResults.toggle)
			disableDatasourceUpdate = argResults.disableDatasourceUpdate
			disableAuthenticationUpdate = argResults.disAuthenticationUpdate
			if(settings == None):
				print lineStartChar + "Error loading settings"
			else:
				print lineStartChar + "Settings loaded from file:"
				print "-----------------------------------------------"
				# print Data Source Info
				if(settings.dataSourceList != None and disableDatasourceUpdate == FALSE):
					for n2 in range(0,len(settings.dataSourceList)):
						datasourceStuff = settings.dataSourceList[n2]
						print "--------------"+str(n2) + "--------------"
						print  "DataSource URL = "+ datasourceStuff.datasourceURL;
						for n3 in range (0, len(datasourceStuff.datasourceName)):
							print  "DataSource Name = "+ datasourceStuff.datasourceName[n3];
				#print Auth Data List
				if(settings.authDataList != None and disableAuthenticationUpdate == FALSE):
					for n2 in range(0,len(settings.authDataList)):
						authStuff = settings.authDataList[n2]
						print "--------------"+str(n2) + "--------------"
						print  "aliasName = "+ authStuff.aliasName;
						if not(authStuff.databasePassword == None):
							print "databasePassword = "+ "*"
				print "-----------------------------------------------"
				print lineStartChar + "Attempting to update server"
				if (disableDatasourceUpdate == FALSE):
					step1 = updateOracleDataSource(settings.dataSourceList)
				else:
					step1 = SUCCESS
				if (step1 == SUCCESS and disableAuthenticationUpdate == FALSE):
					step2 = updateAuthentication(settings.authDataList)
				else:
					step2 = SUCCESS
				if (step1 == SUCCESS and step2 == SUCCESS):
					try:
						UpdateMessage = ""
						if(disableDatasourceUpdate == FALSE and disableAuthenticationUpdate == FALSE):
							UpdateMessage = "Data source and Alias"
						elif(disableDatasourceUpdate == FALSE and disableAuthenticationUpdate == TRUE):
							UpdateMessage = "Data source"
						elif(disableDatasourceUpdate == TRUE and disableAuthenticationUpdate == FALSE):
							UpdateMessage = "Alias"
						else:
							UpdateMessage = "No"
						print lineStartChar + "Attempting to SAVE " + UpdateMessage + " Changes..."
#						AdminConfig.save();
						print lineStartChar + UpdateMessage + " Updates was committed Successfully."
						returnValue = SUCCESS
					except Exception, e:
						print e
				else:
					print lineStartChar + "-     ERROR During Update"
				AdminConfig.reset()
				print lineStartChar + "Displaying current settings:"
				displayDataSourceAndAlias()
	except Exception, e:
		print lineStartChar + "Exception in main:"
		print e
		print "-End Expection-"
	print lineStartChar + "Closing Program"
	return returnValue
#end def main

if __name__ == "__main__":
	main(sys.argv[:])