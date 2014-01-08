#
# Run this script on the AdminServer, else it won't find the Resource Adapter Plans
#


from weblogic.descriptor import BeanAlreadyExistsException
from java.lang.reflect import UndeclaredThrowableException
from java.lang import System
import javax
from javax import management
from javax.management import MBeanException
from javax.management import RuntimeMBeanException
import javax.management.MBeanException
from java.lang import UnsupportedOperationException
from javax.management import InstanceAlreadyExistsException
from java.lang import Exception
from jarray import array
from java.io import FileInputStream
import random


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
    #edit()
    startEdit()
    print "++++++++++++++++++++++++++++++++++++++++++++++++++"

def endTransaction():
    print "++++++++++++++++++++++++++++++++++++++++++++++++++"
    save()
    activate(block="true")
    print "--------------------------------------------------"


def endOfConfigToScriptRun():
    disconnect()
    print 'Done executing the script.'

def createResourceAdapter(eisName,propertyName,dataSourceName,connectionFactoryInterface,appName,appPath):

        uniqueString = str(random.randint(100000,1000000))

        connectionInstance='ConnectionInstance_'+eisName+'_JNDIName_'+uniqueString
        configProperty='ConfigProperty_ConnectionFactoryLocation_Value_'+uniqueString
        
        planPath = get('/AppDeployments/'+appName+'/AbsolutePlanPath')
        print '__ Using plan ' + planPath + ' ___'
                    
        myPlan=loadApplication(appPath, planPath)
                    
        print '___ BEGIN change plan'+ ' ___'
        
        makeDeploymentPlanVariable(myPlan, appName,connectionInstance, eisName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="'+connectionFactoryInterface+'"]/connection-instance/[jndi-name="'+ eisName + '"]/jndi-name')
        makeDeploymentPlanVariable(myPlan, appName, configProperty, dataSourceName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="'+connectionFactoryInterface+'"]/connection-instance/[jndi-name="'+ eisName + '"]/connection-properties/properties/property/[name="'+propertyName+'"]/value')
        
        print '___ DONE change plan  ___'
                    
        myPlan.save()


def makeDeploymentPlanVariable(wlstPlan, appName,interfaceName, jndiName, xpath, origin='planbased'):
        moduleOverrideName=appName+'.rar'
        moduleDescriptorName='META-INF/weblogic-ra.xml' 
        
        if (wlstPlan.getVariableAssignment(interfaceName, moduleOverrideName, moduleDescriptorName)):
            wlstPlan.destroyVariableAssignment(interfaceName, moduleOverrideName, moduleDescriptorName)
                
        if (wlstPlan.getVariable(interfaceName)):
            wlstPlan.destroyVariable(interfaceName)
                    
        variableAssignment = wlstPlan.createVariableAssignment( interfaceName, moduleOverrideName, moduleDescriptorName )
        variableAssignment.setXpath( xpath )
        variableAssignment.setOrigin( origin )
        wlstPlan.createVariable( interfaceName, jndiName )


def redeployResourceAdapter(appName):
        planPath = get('/AppDeployments/'+appName+'/AbsolutePlanPath')
        print '__ redeploy application __'+appName
        print '__ Using plan ' + planPath+ ' ___'
        cd('/AppDeployments/'+appName+'/Targets');
        redeploy(appName, planPath,targets=cmo.getTargets());
        #updateApplication(appName, planPath)
        cd('/')            

try:
    initConfigToScriptRun()
    edit()
    startTransaction()
  
    #attributes setup
    dbAdapterAppPath=connectorLocation+'DbAdapter.rar'
    dbConnectionFactoryInterface='javax.resource.cci.ConnectionFactory'
  
    aqAdapterAppPath=connectorLocation+'AqAdapter.rar'
    aqConnectionFactoryInterface='javax.resource.cci.ConnectionFactory'

    jmsAdapterAppPath=connectorLocation+'JmsAdapter.rar'
    jmsConnectionFactoryInterface='oracle.tip.adapter.jms.IJmsConnectionFactory'
  
  
  
    #Create DB Adaptor Resource, destroy the exsiting one if found the same 
    total_DBAdapter=configProps.get('total.DBAdapter')
    
    i=1
    while (i <= int(total_DBAdapter)) :
        eisName = configProps.get('db'+str(i)+'.eisName')
        propertyName = configProps.get('db'+str(i)+'.propertyName')       
        dataSourceName= configProps.get('db'+str(i)+'.dataSourceName')
        print '======= Starting configuration for '+eisName+' ============='
        createResourceAdapter(eisName,propertyName,dataSourceName,dbConnectionFactoryInterface,'DbAdapter',dbAdapterAppPath)
        i=i+1
        
  
    #Create AQ Adaptor Resource, DataSourceName=xADataSourceName or DataSourceName
    
    total_AQAdapter=configProps.get('total.AQAdapter')
    
    i=1
    while (i <= int(total_AQAdapter)) :
        eisName = configProps.get('aq'+str(i)+'.eisName')
        propertyName = configProps.get('aq'+str(i)+'.propertyName')       
        dataSourceName= configProps.get('aq'+str(i)+'.dataSourceName')
        print '======= Starting configuration for '+eisName+' ============='
        createResourceAdapter(eisName,propertyName,dataSourceName,aqConnectionFactoryInterface,'AqAdapter',aqAdapterAppPath)
        i=i+1
    
   
  
    #Create JMS Adaptor Resource
   
    total_JMSAdapter=configProps.get('total.JMSAdapter')
    
    i=1
    while (i <= int(total_JMSAdapter)) :
        eisName = configProps.get('jms'+str(i)+'.eisName')
        propertyName = configProps.get('jms'+str(i)+'.propertyName')       
        dataSourceName = configProps.get('jms'+str(i)+'.dataSourceName')
        print '======= Starting configuration for '+eisName+' ============='
        createResourceAdapter(eisName,propertyName,dataSourceName,jmsConnectionFactoryInterface,'JmsAdapter',jmsAdapterAppPath)
        i=i+1
  
    #active the new update.
  
     
    endTransaction()
        
    redeployResourceAdapter('DbAdapter')
    
finally:
  endOfConfigToScriptRun()