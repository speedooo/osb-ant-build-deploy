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

def deleteJDBCDataReource(dsName):
    if getMBean('/JDBCSystemResources/' + dsName) :
        delete(dsName, 'JDBCSystemResource')
        print "Found and Deleted the exit JDBC DataSource config --"+dsName
    else:
        print "NOT Found JDBC DataSource config --"+dsName


def createJDBCDataSource(dsName, dsJNDIName, datasourceTargets, dsDriverName, dsURL, dsUserName, dsPassword):
    cd('/')
    cmo.createJDBCSystemResource(dsName)
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName)
    cmo.setName(dsName)

    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName )
    cmo.setJNDINames(jarray.array([String(dsJNDIName)], String))

    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName )
    cmo.setUrl(dsURL)
    cmo.setDriverName( dsDriverName )
    cmo.setPassword(dsPassword)

    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCConnectionPoolParams/' + dsName )
    cmo.setTestTableName('SQL SELECT 1 FROM DUAL')
    
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName )
    cmo.createProperty('user')

    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/user')
    cmo.setValue(dsUserName)
   
    
    targetArray=[]
    for datasourceTarget in datasourceTargets:	  
        if datasourceTarget=='':
            print ''
        else:           
            target=datasourceTarget[datasourceTarget.index("/")+1:len(datasourceTarget)]
            print 'target JDBC datasource to target='+target
            
            if datasourceTarget.startswith('Cluster'):
                targetArray.append(ObjectName('com.bea:Name='+target+',Type=Cluster'))
            elif datasourceTarget.startswith('Server'):
                targetArray.append(ObjectName('com.bea:Name='+target+',Type=Server'))
    
    cd ('/JDBCSystemResources/'+dsName)
    set('Targets', jarray.array(targetArray, ObjectName))

    print "JDBC DataSource created successful -- "+dsName



def createJMSDataSource():
    servermb=getMBean('Servers/'+datasourceTarget)

    print "Creating WebServiceJMSServer..."
    jmsserver1mb = create(jmsServerName,'JMSServer')
    jmsserver1mb.addTarget(servermb) 
    #jmsserver1mb.setNotes("This JMS server is used by workshop 5")

    print "Creating the WebServiceResources JMS Module..."
    jmsMySystemResource = create(jmsModuleName,"JMSSystemResource")
    jmsMySystemResource.addTarget(servermb) 
    #jmsMySystemResource.setNotes("A JMS system module to contain the connection factory and the JMS queue")

    print "Creating subdeployment..."
    subDep1mb = jmsMySystemResource.createSubDeployment(moduleSubdeploy)
    subDep1mb.addTarget(jmsserver1mb)

    theJMSResource = jmsMySystemResource.getJMSResource()

    print "Creating connection factory..."
    connfact1 = theJMSResource.createConnectionFactory(connectFactory)
    connfact1.setJNDIName(cfJNDIName)
    connfact1.setLocalJNDIName('local/'+cfJNDIName)
    connfact1.setSubDeploymentName(moduleSubdeploy)
    connfact1.setNotes("Use the JNDI name to connect to the JMS queue")

    print "Creating XA connection factory..."
    connfact1 = theJMSResource.createConnectionFactory(connectFactoryXA)
    connfact1.setJNDIName(cfJNDINameXA)
    connfact1.setLocalJNDIName('local/'+cfJNDINameXA)
    connfact1.setSubDeploymentName(moduleSubdeploy)
    connfact1.setNotes("Use the JNDI name to connect to the JMS queue")
    connfact1.transactionParams.setXAConnectionFactoryEnabled(1)

    print "Creating SourceQueue..."
    jmsqueue1 = theJMSResource.createQueue('SourceQueue')
    jmsqueue1.setJNDIName('jms/SourceQueue')
    jmsqueue1.setSubDeploymentName(moduleSubdeploy)

    print "Creating DestinationQueue..."
    jmsqueue1 = theJMSResource.createQueue('DestinationQueue')
    jmsqueue1.setJNDIName('jms/DestinationQueue')
    jmsqueue1.setSubDeploymentName(moduleSubdeploy)

    print "Creating ErrorQueue..."
    jmsqueue1 = theJMSResource.createQueue('ErrorQueue')
    jmsqueue1.setJNDIName('jms/ErrorQueue')
    jmsqueue1.setSubDeploymentName(moduleSubdeploy)

    print "Creating DestinationTopic..."
    jmsqueue1 = theJMSResource.createTopic('DestinationTopic')
    jmsqueue1.setJNDIName('jms/DestinationTopic')
    jmsqueue1.setSubDeploymentName(moduleSubdeploy)


    print "Creating SourceTopic..."
    jmsqueue1 = theJMSResource.createTopic('SourceTopic')
    jmsqueue1.setJNDIName('jms/SourceTopic')
    jmsqueue1.setSubDeploymentName(moduleSubdeploy)    
    
try:
    initConfigToScriptRun()
    
    total_DS=configProps.get('total.DS')
    
    #Delete the exsiting JDBC Data Sources
    startTransaction()
    i=1
    while (i <= int(total_DS)) :
        deleteJDBCDataReource(configProps.get('ds'+str(i)+'.dsName'))
        i = i+1
    
    endTransaction()
    
    
    
    #Create JDBC Data Sources for DBAdapter and AQAdapter
    startTransaction()   
        
    datasourceTargets=configProps.get('ds.datasourceTargets').split(",")
    dsDriverName=configProps.get('ds.dsDriverName')
    i=1
    while (i <= int(total_DS)) :
        dsName = configProps.get('ds'+str(i)+'.dsName')
        dsJNDIName = configProps.get('ds'+str(i)+'.dsJNDIName')       
        dsURL= configProps.get('ds'+str(i)+'.dsURL')
        dsUserName= configProps.get('ds'+str(i)+'.dsUserName')
        dsPassword= configProps.get('ds'+str(i)+'.dsPassword')
        createJDBCDataSource(dsName, dsJNDIName, datasourceTargets, dsDriverName, dsURL, dsUserName, dsPassword)
        i=i+1
    
    
     
  
    #Create JMS Data Sources for JMSAdapter
       
  
    endTransaction()
finally:
  endOfConfigToScriptRun()