import argparse
import os
import time

# pip install google-api-python-client


import googleapiclient.discovery
from six.moves import input

# important!
compute = googleapiclient.discovery.build('compute', 'v1')

# [Start list_instances]
# def list_instances(compute, project, zone):
# result = compute.instance().list(project=project,zone = zone).execute()
# return result['items'] if 'items' in result else None
# [END list_instances]

# x= list_instances(compute,'linux-vm-364004','us-central1-a')
# print(x)


def create_instance(compute, project, zone, name, bucket):
    # Get the latest Windows server
    image_response = compute.images().getFromFamily(
        project='debian-cloud', family='debian-11').execute()
    source_disk_image = image_response['selfLink']
    print(source_disk_image)
    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone

    config = {
        'name': name,
        'machineType': machine_type,

        'disks': [
            {
                'boot': True,
                'autodelete': True,
                'initializeparams': {
                    'sourceImage': source_disk_image,
                },
                'source': f'https://www.googleapis.com/compute/v1/projects/linux-vm-364004/zones/us-central1-a/disks/disk-2'
            }
        ],
        # Specify a network interfaces with NAT to access the public internet
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Allow the instances to access cloud storage and logging
        'serviceaccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth.logging.write'
            ]
        }],
        'metadata': {
            # 'items': [{
            #     # Startup script is automatically executed by the
            #     # instance upon startup.
            #     'key': 'startup-script',
            #     'value': startup_script
            # }, {
            #     'key': 'url',
            #     'value': image_url
            # }, {
            #     'key': 'text',
            #     'value': image_caption
            # }, {
            #     'key': 'bucket',
            #     'value': bucket
            # }]
        }
    }
    print(config['disks'][0]['source'])
    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()


if __name__ == '__main__':
    create_instance(compute, 'linux-vm-364004',
                    'us-central1-a', 'pyvm', 'pybucket')
