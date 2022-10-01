import argparse
import os
import time

# pip install google-api-python-client


import googleapiclient.discovery
from six.moves import input

# important!

compute = googleapiclient.discovery.build('compute', 'v1')
result = compute.instances().stop(project='linux-vm-364004',zone='us-central1-a',instance='pyvm').execute()