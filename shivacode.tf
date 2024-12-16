as part of the process to clean up and validate the libraries listed in requirement.txt, I followed the steps below:

Created a virtual environment (Python version 3.9) on the Dev server cvlinq0177.
Checked the existing libraries in the environment by executing the pip3 list command. I observed only two libraries:
pip
setuptools
Installed the main required libraries (awscli and dbt-core) and rechecked the environment.
After the installation, approximately 60 libraries were installed as dependencies (verified using pip3 list).
The original requirement.txt file had 89 libraries. I compared the newly installed 60 libraries with the original 89, removed overlaps, and added the remaining libraries.
This resulted in a total of 17 libraries (including dependencies), which are functionally equivalent to the original 89 libraries.
To validate the setup, I ran the jobrunn.py script using the optimized set of 17 libraries, and it executed successfully.
