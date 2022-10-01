import argparse
import os
import time

# pip install google-api-python-client


import googleapiclient.discovery
from six.moves import input

# important!
compute = googleapiclient.discovery.build('compute', 'v1')
def delete_instance(compute,project,zone,name):
    return compute.instances().delete(
        project=project,
        zone=zone,
        instance = name).execute()
delete_instance(compute,'linux-vm-364004',
                    'us-central1-a', 'pyvm')

