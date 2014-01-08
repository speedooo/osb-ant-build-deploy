from java.util import HashMap
from java.util import HashSet
from java.util import ArrayList
import sys
import os
from java.lang import System
from java.lang import Exception
from jarray import array
from java.io import FileInputStream


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
  
    domainName = configProps.get('DOMAIN_NAME')

    plans=configProps.get("plans")
    adapters=configProps.get("adapters")

    planArray = []
    adapterArray = []

#create needed directories where to put *Plan.xml
    for plan in plans.split(','):
        planFullPath = configProps.get(plan).replace("${DOMAIN_NAME}", domainName)
        planArray.append(planFullPath)

#create array of adapters
    for adapter in adapters.split(','):
        adapterName = configProps.get(adapter)
        adapterArray.append(adapterName)


#create dir if doesn't exist - fail if unable to create it
    for planFullPath in planArray:    
        dirName = os.path.dirname(planFullPath)
    
        if not os.path.exists(dirName):
            print "creating directory " + dirName
            os.makedirs(dirName)
    
#check for directory existence
    for planFullPath in planArray:
        dirName = os.path.dirname(planFullPath)
        print "testing directory " + dirName
    
        if not os.path.exists(dirName):
            message = "directory " + dirName + " does not exist"
            print message
            raise Exception(message)

    

#copy all Plan.xml files to their final destination, with token substitution
    for planFullPath in planArray:
        fileName = os.path.basename(planFullPath)
        print "copying " + fileName + " to " + planFullPath  
        copyfileWithTokenSubstitution(fileName, planFullPath, configProps)
   
  

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
      
def copyfileWithTokenSubstitution(filein, fileout, properties):
        input = open(filein)
        output = open(fileout, 'w')
        for s in input:
            rep = s
            for tokenname in properties.get("tokens").split(','):
                rep = rep.replace("${" + tokenname + "}", properties.get(tokenname))
            output.write(rep)
        input.close()
        output.close()
        
        
try:
    initConfigToScriptRun()
    edit()
    print 'TESTING TESTING TESTING TESTING TESTINGTESTING TESTING TESTING'
    
    for index in range(len(planArray)):
        startEdit()
        plan = planArray[index]
        adapter = adapterArray[index]
        
        adapterType = os.path.basename(adapter).split('.')[0]
        
        print 'Applying plan ' + plan + " to adapter " + adapter + " (adapter type is " + adapterType + ")"
        myPlan = loadApplication(adapter, plan)
        myPlan.save()
        save()
        activate(block='true')
        cd('/AppDeployments/' + adapterType + '/Targets')
        #updateApplication(appName, planPath);
        redeploy(adapterType, plan, targets = cmo.getTargets())
    
  
    
except:
    dumpStack()
    stopEdit('y')
    message="unable to finish job"
    raise Exception(message)
    
endOfConfigToScriptRun()