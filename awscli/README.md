List instances by tags:

    aws ec2 describe-tags --filters "Name=key,Values=Salt" "Name=value,Values=HAProxy_VPC"

or

    aws ec2 describe-tags --filters Name=tag:Salt,Values=HAProxy_VPC

With jq:

    aws ec2 describe-tags --filters Name=tag:Salt,Values=HAProxy_VPC | jq '.Tags[].ResourceId'

Query all instance within VPC:

     aws ec2 describe-instances --filters Name=vpc-id,Values=vpc-8efa66eb --query 'Reservations[].Instances[].[PrivateIpAddress,InstanceId,Tags[?Key==`Name`].Value[]]' --output text | sed 's/None$/None\n/' | sed '$!N;s/\n/ /'
