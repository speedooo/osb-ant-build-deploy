What can ANT script do?
ant script (build.xml) is under your HUBConfigration folder. XXXX is represent your server target environment. LAN is login username or different environment like sbst, sbsit, sbat and sbprod
ant command	                                    description
ant	                                            package is the default task, make osb jar build package under target folder
ant releasePackage	                            will create the release zip file for release propose
ant package-deploy	                            make build jar and deploy to your dev osb server configured in your XXXX-weblogic.properties
ant -Ddestination=appbuild package	            this is for Bamboo agent, configured in appbuild-weblogic.properties

under your target folder, mostly used for deployment (only developer's vm without -Ddestination argument)

ant command	                                    description
ant -f deploy.xml configure	                    will create the your env customization.xml and python scripts
ant -f deploy.xml deploy	                    deploy to your dev osb server configured in your XXXX-weblogic.properties
ant -f deploy.xml undeployProjects	            undeploy projects from your server configured in your XXXX-weblogic.properties
ant -f deploy.xml exportFromOSB	                export all projects fro your OSB server.
ant -f deploy.xml createDataSource	            create datasource, DatabaseSource , JMS in your XXXX-weblogic.properties
ant -f deploy.xml createAdapter	                create adpter like DB, JMS and AQ, configured in your  XXXX-weblogic.properties
ant -f deploy.xml -Ddestination=appbuild        deploy	deploy the jar without customization.xml to appbuild environment, you can change to sbsit, sbat and sbprod
ant -f deploy.xml -Ddestination=sbst -DcustomizationFile=customization.xml deploy	deploy the jar with customization.xml to system test environment, you can change to sbsit, sbat and sbprod


How to configure the properties for your environment?
if you want configure your target server, package name..., you need modify properties/XXXX-weblogic.properties file
If you want to configure your third party IP and Port number, your need modify osbconfig/XXXX.properties. This is used to create customization.xml

What do you need configure for your project?
anything related to your project in properties/XXXX-weblogic.properties file. like project.name, release.number, build.jar and import.jar
any project want undeploy in your scripts, undeployProjects in your properties/XXXX-weblogic.properties file.
any project you want to include in your package. build.xml <property name="project.names" value="" and <property name="project.includes" value=""

How to deploy osb jar?
check out the zip file after " ant releasePackage" command.
verify/modify your target server password in  XXXX-weblogic.properties
backup the existing OSB from your server by "ant -f deploy.xml exportFromOSB"
undeploy the projects by "ant -f deploy.xml undeployProjects"
deploy your new jar by "ant -f deploy.xml deploy -Ddestination=XXXX"


How to run the Python scripts?
check out the zip file after " ant releasePackage" command.
verify/modify your target server password in  XXXX-weblogic.properties
ant -f deploy.xml createAdapter
OR you can using WLST environment just run the createAdapter.py

Bamboo plan setup for OSB project?
the (10.115.1.72) VM does have osb build capability at the moment, login as colbuild
There is main project for Hub2 OSB
you can create plan for your osb project against bamboo-agent-home1 agent
Code check out
package build " ant -Ddestination=appbuild package"
package deploy "ant -f deploy.xml -Ddestination=appbuild deploy"
run the integration test suite "ant eomtest"

What’s next steps?
write the process for soa project
write the process load the existing DBplan, JMSPlan and other existing adapter configuration plan file


Issue and concerned:
how to update/committed what you change in the osbconfig/customization.xml template for your new service?
issue fixed. The default is not loading customization.xml. but user could setup in the command, like  -DcustomizationFile=customization.xml. This customization.xml file is only for release in Hub2dev  , ST , SIT...

EST team is not happy with username/password in the plain txt properties file?
issue fixed. There is property called connectEncrypted  in XXXX-weblogic.properties could turn this feature.
