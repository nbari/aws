#!/usr/bin/env python

"""
http://docs.aws.amazon.com/ElasticLoadBalancing/latest/DeveloperGuide/elb-cloudwatch-metrics.html
"""

import boto.ec2
import os
import sys
import time

AWS_REGION = os.environ['EC2_REGION']
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']


def create_instance(ami, instance_type):
    tags = {}
    tags['Name'] = 'web_production_JAILS'
    tags['Salt'] = 'web_production_JAILS'

    conn = boto.ec2.connect_to_region(
        AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY)

    interface = boto.ec2.networkinterface.NetworkInterfaceSpecification(
        subnet_id='subnet-f61b5293',
        groups=['sg-e77c9683'],
        device_index=0,
        secondary_private_ip_address_count=3,
        associate_public_ip_address=False
    )

    interfaces = boto.ec2.networkinterface.NetworkInterfaceCollection(
        interface)

    reservation = conn.run_instances(
        ami,
        key_name='VPC',
        instance_type=instance_type,
        network_interfaces=interfaces,
        dry_run=False
    )

    instance = reservation.instances[0]

    # Check up on its status every so often
    status = instance.update()
    while status == 'pending':
        time.sleep(10)
        status = instance.update()

    if status == 'running':
        instance.add_tags(tags)
    else:
        print('Instance status: ' + status)


if __name__ == "__main__":
   # if not sys.argv[2:]:
   #     print "Enter ELB name"
   #     sys.exit(1)

    ami = 'ami-dddd78ae'
    instance_type = 't2.medium'
    print create_instance(ami, instance_type)
