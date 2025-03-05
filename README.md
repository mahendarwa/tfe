I checked the Jenkins pipeline, and it's running on a Linux-based agent (Linux-OSS-cvlappxi20017). The objects are created and deployed through the following process:

Git Checkout - The repo is cloned from GitHub.
Build & Artifact Creation - A Groovy script initializes the build, followed by a Maven build that compiles and packages objects.
Artifact Deployment - The built artifacts are uploaded to Artifactory and deployed to TDM servers.
Let me know if you need any further details.
==
I checked the Jenkins pipeline logs, and the deployment is triggered via uDeploy (udeploy.sys.cigna.com). The build artifact name suggests it's targeting TDM_PROD, but the specific TDM server name is not explicitly mentioned in the logs.

To confirm the exact deployment target, we may need to check uDeploy logs, I'm not able to open this logs link there mentioned in the Jenkins console output.
