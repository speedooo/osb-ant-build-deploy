from java.util import HashMap
from java.util import HashSet
from java.util import ArrayList
import sys
import os
from java.lang import System
from java.lang import Exception
from jarray import array


def initConfigToScriptRun():
  
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
    startEdit()
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
  
   #change the wrong target for WTC
    cd('/WTCServers/'+wtcServerName)
    set('Targets',jarray.array([ObjectName('com.bea:Name=' + osbServerTargetName + ',Type=Server')], ObjectName))

    #setup extra attribute value
    cd('LocalTuxDoms/'+localTuxDomName)
    set('Interoperate', 'YES')
    set('BlockTime', '86400')
      
  
    endTransaction()
finally:
  endOfConfigToScriptRun()