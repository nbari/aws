List instances by tags:

    aws ec2 describe-tags --filters "Name=key,Values=Salt" "Name=value,Values=HAProxy_VPC"

or

    aws ec2 describe-tags --filters Name=tag:Salt,Values=HAProxy_VPC

With jq:

    aws ec2 describe-tags --filters Name=tag:Salt,Values=HAProxy_VPC | jq '.Tags[].ResourceId'
