#!/usr/bin/env python

import boto.ec2
import os
import sys
import time

AWS_REGION = 'eu-west-1'
AWS_ACCESS_KEY = 'access_key'
AWS_SECRET_KEY = 'secret_key'

def reachability():

    conn = boto.ec2.connect_to_region(
        AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY)


    instances = conn.get_all_instance_status()
    for instance in instances:
        if instance.system_status.details["reachability"] != "passed":
            bad_instance =  instance.id



if __name__ == "__main__":
    reachability()
