import csv

import logging

import oci

 

# Configure logging to write to the log file

logging.basicConfig(filename='logfile.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

 

config = oci.config.from_file()

 

database_client = oci.database.DatabaseClient(config)

compute_client = oci.core.ComputeClient(config)

 

db_systems_map = {}

instances_map = {}

 

# Search for all DB systems across all compartments

logging.info("Searching for DB systems...")

search_details = oci.resource_search.models.StructuredSearchDetails(query="query dbsystem resources")

search_response = oci.pagination.list_call_get_all_results(

    oci.resource_search.ResourceSearchClient(config).search_resources,

    search_details

)

 

# Iterate through the search results and extract the hostname prefix from the display name

for resource in search_response.data:

    db_system = resource

    hostname_prefix = db_system.display_name.lower().split(".")[0]

    db_systems_map[hostname_prefix] = db_system

 

# Search for all instances across all compartments

logging.info("Searching for instances...")

search_details = oci.resource_search.models.StructuredSearchDetails(query="query instance resources")

search_response = oci.pagination.list_call_get_all_results(

    oci.resource_search.ResourceSearchClient(config).search_resources,

    search_details

)

 

# Iterate through the search results and extract the hostname prefix from the display name

for resource in search_response.data:

    instance = resource

    hostname_prefix = instance.display_name.lower().split(".")[0]

    instances_map[hostname_prefix] = instance

 

with open("Info2.csv", "r") as file:

    reader = csv.reader(file)

    next(reader)  # Skip header row

 

    for row in reader:

        hostname_prefix = row[0].lower()

        db_system = db_systems_map.get(hostname_prefix)

        instance = instances_map.get(hostname_prefix)

 

        if db_system:

            resource_type = "DB system"

            resource_id = db_system.identifier

            logging.info(f"Iterating through DB system: {hostname_prefix} ({resource_id})")

        elif instance:

            resource_type = "instance"

            resource_id = instance.identifier

            logging.info(f"Iterating through instance: {hostname_prefix} ({resource_id})")

        else:

            logging.error(f"No matching DB system or instance found for hostname prefix: {hostname_prefix}")

            continue

 

        application = row[1]

        ApplicationOwner = row[2]

        BusinessOwner = row[3]

        CostCenter = row[4]

        DatabaseName = row[5]

        DatabaseOwner = row[6]

        Environment = row[7]

        LifeCycleStatus = row[8]

        LOB = row[9]

        PMOID = row[10]

 

        tags = {

            "sh-tags": {

                "Application": application,

                "ApplicationOwner": ApplicationOwner,

                "BusinessOwner": BusinessOwner,

                "CostCenter": CostCenter,

                "DatabaseName": DatabaseName,

                "DatabaseOwner": DatabaseOwner,

                "Environment": Environment,

                "LifeCycleStatus": LifeCycleStatus,

                "LOB": LOB,

                "PMOID": PMOID

            }

        }

 

        logging.info(f"Tagging {resource_type}: {hostname_prefix} ({resource_id})")

        if resource_type == "DB system":

            update_details = oci.database.models.UpdateDbSystemDetails(defined_tags=tags)

            response = database_client.update_db_system(db_system_id=resource_id, update_db_system_details=update_details)

        elif resource_type == "instance":

            update_details = oci.core.models.UpdateInstanceDetails(defined_tags=tags)

            response = compute_client.update_instance(instance_id=resource_id, update_instance_details=update_details)

 

        logging.info(f"Tags updated for {resource_type}: {hostname_prefix} ({resource_id})")