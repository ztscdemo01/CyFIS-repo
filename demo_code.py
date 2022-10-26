#!/usr/bin/env python

"""
Simple script to create a new incident, specifying values for custom fields.
#5
"""
from __future__ import print_function
from argparse import REMAINDER
import time
import logging
import resilient


logging.basicConfig()


class ExampleArgumentParser(resilient.ArgumentParser):
    """Arguments for this command-line application, extending the standard Resilient arguments"""

    def __init__(self, config_file=None):
        super(ExampleArgumentParser, self).__init__(config_file=config_file)

        self.add_argument('--name', '-n',
                          required=True,
                          help="The incident name.")

        self.add_argument('--description', '-d',
                          required=True,
                          help="The incident description.")

        self.add_argument('--itype', '-t',
                          action='append',
                          help="The incident type(s).  Multiple arguments may be supplied.")

        self.add_argument('--custom', '-c',
                          nargs=REMAINDER,
                          help="Custom field values, specified as: fieldname=value")


def main():
    """
    program main
    """

    parser = ExampleArgumentParser(config_file=resilient.get_config_file())
    opts = parser.parse_args()

    inc_name = opts["name"]
    inc_desc = opts["description"]
    inc_types = opts["itype"]

    # Create SimpleClient for a REST connection to the Resilient services
    client = resilient.get_client(opts)

    # Discovered Date will be set to the current time
    time_now = int(time.time() * 1000)

    # Construct the basic incident DTO that will be posted
    new_incident = {"name": inc_name,
                    "description": inc_desc,
                    "incident_type_ids": inc_types,
                    "discovered_date": time_now,
                    "properties": {}}

    # Add the specified values for any custom fields,
    # per the command-line arguments provided.
    # Within the incident JSON structure, the values for custom fields
    # are all contained within a dictionary value named 'properties'.
    for custom in opts["custom"]:
        (field_name, field_value) = custom.split("=", 1)
        print("{} = {}".format(field_name, field_value))
        new_incident["properties"][field_name] = field_value

    try:
        uri = '/incidents'

        # Create the incident
        incident = client.post(uri, new_incident)

        inc_id = incident["id"]

        print("Created incident {}".format(inc_id))

    except resilient.SimpleHTTPException as ecode:
        print("create failed : {}".format(ecode))

if __name__ == "__main__":
    main()