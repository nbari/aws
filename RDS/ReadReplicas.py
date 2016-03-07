#!/usr/bin/env python

"""
http://docs.aws.amazon.com/cli/latest/reference/rds/describe-db-instances.html
"""

import boto.rds
import os
import sys

AWS_REGION = os.environ['EC2_REGION']
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']

def ReadReplicas(RDS_NAME):
    conn = boto.rds.connect_to_region(
            AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY)

    instance = conn.get_all_dbinstances(RDS_NAME)
    db = instance[0]
    replicas = {}
    for replica in  db.read_replica_dbinstance_identifiers:
        replica_instance = conn.get_all_dbinstances(replica)
        db_replica = replica_instance[0]
        replicas[db_replica.endpoint[0]] = db_replica.endpoint[1]
    return replicas

if __name__ == "__main__":
    if not sys.argv[1:]:
        print "Enter RDS name"
        sys.exit(1)

    RDS_NAME = sys.argv[1:]
    replicas = ReadReplicas(RDS_NAME[0])
    for k, v in replicas.items():
        print k, v
