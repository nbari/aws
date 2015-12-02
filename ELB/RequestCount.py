#!/usr/bin/env python

"""
http://docs.aws.amazon.com/ElasticLoadBalancing/latest/DeveloperGuide/elb-cloudwatch-metrics.html
"""

import datetime
import os
import sys

from boto.ec2 import cloudwatch

AWS_REGION = os.environ['EC2_REGION']
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
PERIOD = 60
MINUTES = 1 # minutes of data to retrieve

metrics = {
        "RequestCount": {
            "stat": "Sum",
            "type": "int",
            "value":None,
            "uom": ""
            }
        }

def SumRequests(ELB_NAME):
    conn = cloudwatch.connect_to_region(
            AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY)

    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(minutes=MINUTES)

    for k, m in metrics.items():
        try:
            # print k
            res = conn.get_metric_statistics(
                    PERIOD,
                    start,
                    end, k,
                    "AWS/ELB",
                    m['stat'],
                    dimensions={"LoadBalancerName": ELB_NAME})
        except Exception, e:
            print "WARN - status err Error running elb stats: %s" % e.message
            sys.exit(1)

        for r in res:
           return  '%d' % r[m['stat']]


if __name__ == "__main__":
    if not sys.argv[1:]:
        print "Enter ELB name"
        sys.exit(1)

    ELB_NAME = sys.argv[1:]
    print SumRequests(ELB_NAME)
