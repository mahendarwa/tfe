I checked the Jenkins pipeline, and it's running on a Linux-based agent (Linux-OSS-cvlappxi20017). The objects are created and deployed through the following process:

Git Checkout - The repo is cloned from GitHub.
Build & Artifact Creation - A Groovy script initializes the build, followed by a Maven build that compiles and packages objects.
Artifact Deployment - The built artifacts are uploaded to Artifactory and deployed to TDM servers.
Let me know if you need any further details.
