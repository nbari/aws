List instances by tags:

    aws ec2 describe-tags --filters "Name=key,Values=Salt" "Name=value,Values=HAProxy_VPC"

or

    aws ec2 describe-tags --filters Name=tag:Salt,Values=HAProxy_VPC

With jq:

    aws ec2 describe-tags --filters Name=tag:Salt,Values=HAProxy_VPC | jq '.Tags[].ResourceId'

Query all instance within VPC:

     aws ec2 describe-instances --filters Name=vpc-id,Values=vpc-8efa66eb --query 'Reservations[].Instances[].[PrivateIpAddress,InstanceId,Tags[?Key==`Name`].Value[]]' --output text | sed 's/None$/None\n/' | sed '$!N;s/\n/ /'


Get InstanceID, status, zone, ip:

    aws ec2 describe-instances --filters Name=tag:Salt,Values=HAProxy_VPC --query 'Reservations[].Instances[].[InstanceId, State.Name, Placement.AvailabilityZone, PrivateIpAddress]' --output table

outputs something like:

```sh
--------------------------------------------------------
|                   DescribeInstances                  |
+------------+----------+--------------+---------------+
|  i-c119cc49|  running |  eu-west-1a  |  10.0.11.235  |
|  i-57dae9da|  running |  eu-west-1c  |  10.0.28.83   |
|  i-92908e19|  running |  eu-west-1b  |  10.0.17.82   |
+------------+----------+--------------+---------------+
```

Get CPUUtilization Average in last 10 minutes:

    aws cloudwatch get-metric-statistics --metric-name CPUUtilization --namespace AWS/EC2 --statistics Average --dimensions Name=AutoScalingGroupName,Value=name-of-group --start-time `date -u -v-10M '+%FT%TZ'` --end-time `date -u '+%FT%TZ'` --period 60
