from java.util import HashMap
from java.util import HashSet
from java.util import ArrayList
import sys
import os
from java.lang import System
from java.lang import Exception
from jarray import array


def initConfigToScriptRun():
  
    environment = sys.argv[1]
  
    loadProperties("properties/"+environment+ "-weblogic.properties")
  
    global configProps
    propInputStream = FileInputStream("properties/"+environment+ "-weblogic.properties")
    configProps = Properties()
    configProps.load(propInputStream)
  
    hideDisplay()
    hideDumpStack("false")
    try:
        if connectEncrypted=="true" :
            connect(userConfigFile=configFile, userKeyFile=keyFile,  url=adminUrl)
    
        else:
            connect(adminUser, adminPassword, adminUrl)
        domainRuntime()
    except WLSTException:
        print 'No server is running at '+ adminUrl
        stopExecution('You need to be connected.')

def startTransaction():
    print "--------------------------------------------------"
    edit()
    
    print "++++++++++++++++++++++++++++++++++++++++++++++++++"

def endTransaction():
    print "++++++++++++++++++++++++++++++++++++++++++++++++++"
    save()
    activate(block="true")
    print "--------------------------------------------------"


def endOfConfigToScriptRun():
    print 'Done executing the script.'
    disconnect()
      

try:
    initConfigToScriptRun()
    startTransaction()
    print 'TESTING TESTING TESTING TESTING TESTINGTESTING TESTING TESTING'
    appName='DbAdapter'
    planPath = get('/AppDeployments/'+appName+'/AbsolutePlanPath')
    print '__ Using plan ' + planPath+ ' ___'
    cd('/AppDeployments/'+appName+'/Targets');
    redeploy(appName, planPath,targets=cmo.getTargets());
    #updateApplication(appName, planPath)
    
    
  
    
finally:
  endOfConfigToScriptRun()