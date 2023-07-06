OCI Resource Tagging:
This script helps in tagging Oracle Cloud Infrastructure (OCI) resources, specifically DB systems and instances, based on information provided in a CSV file.

Prerequisites:
Before running the script, make sure you have the following prerequisites:

Python installed on your system
OCI SDK installed
OCI configuration file (config) set up with appropriate credentials
Installation
Clone the repository:
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

Install the required dependencies:
pip install oci

Usage
Place the CSV file (Info2.csv) with the resource information in the same directory as the script.

Run the script:

python tag_resources.py

The script will read the CSV file and iterate through each row to find the corresponding DB system or instance in your OCI tenancy. It will then update the tags for the resources based on the information provided in the CSV file.

Note: The script assumes that the necessary OCI SDK configuration is already set up in your environment.

CSV File Format
The CSV file (Info2.csv) should have the following columns:

HostnamePrefix: The hostname prefix of the resource.
Application: The application associated with the resource.
ApplicationOwner: The owner of the application.
BusinessOwner: The business owner of the resource.
CostCenter: The cost center associated with the resource.
DatabaseName: The name of the database.
DatabaseOwner: The owner of the database.
Environment: The environment in which the resource is deployed.
LifeCycleStatus: The current lifecycle status of the resource.
LOB: The line of business associated with the resource.
PMOID: The project management office (PMO) ID of the resource.

Logging
The script uses logging to write information and error messages to the logfile.log file in the same directory. You can refer to this log file for detailed execution logs and any encountered errors.
