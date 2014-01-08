from java.util import HashMap
from java.util import HashSet
from java.util import ArrayList
import sys
import os
from java.lang import System
from java.lang import Exception
from jarray import array
from java.io import FileInputStream

from com.bea.wli.config import Ref
from com.bea.wli.config.mbeans import SessionMBean
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.sb.util import EnvValueTypes


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

def discardSession(SessionMBean, sessionName):
    if SessionMBean != None:
        if SessionMBean.sessionExists(sessionName): 
            SessionMBean.discardSession(sessionName)
            print "Session discarded"    

try:
    initConfigToScriptRun()
    #startTransaction()
  
   
    undeployProjList=String(configProps.get('undeployProjects')).split(",")
        
    # obtain session management mbean to create a session.
    # This mbean instance can be used more than once to
    # create/discard/commit many sessions
    sessionMBean = findService(SessionManagementMBean.NAME, SessionManagementMBean.TYPE)
    
    sessionName = "undeployProjectsSession"
   
    if sessionMBean.sessionExists(sessionName):
        discardSession(sessionMBean, sessionName)
        
    sessionMBean.createSession(sessionName)
        
    
    # obtain the ALSBConfigurationMBean instance that operates
    # on the session that has just been created. Notice that
    # the name of the mbean contains the session name.
    alsbSession = findService(ALSBConfigurationMBean.NAME + "." + sessionName, ALSBConfigurationMBean.TYPE)
    
    refs = ArrayList()
    
    for project in undeployProjList:
        projectRef = Ref(Ref.PROJECT_REF, Ref.DOMAIN, project.strip())
        if alsbSession.exists(projectRef):
            print "#### adding OSB project to the delete list: " + project.strip()
            refs.add(projectRef)
        
        else:
            print "OSB project <"+project.strip()+"> does not exist"	
           
    alsbSession.delete(refs)
    
    # activate changes performed in the session
    sessionMBean.activateSession(sessionName, "Complete project removal with customization using wlst")
    
    print "#### removed project: " + configProps.get('undeployProjects')
    print
    
    endOfConfigToScriptRun()
except:
    print "Error whilst removing project:", sys.exc_info()[0]
    discardSession(sessionMBean, sessionName)
    raise  
    