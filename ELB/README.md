Check contents of a policy:

	aws elb describe-load-balancer-policies --policy-names ELBSecurityPolicy-2016-08 | jq '.PolicyDescriptions[] .PolicyAttributeDescriptions[] | select(.AttributeValue == "true")'


To create a custom SSL configuration (Disable TLSv1.0)

	aws elb create-load-balancer-policy \
	--load-balancer-name myloadbalancer \
	--policy-name disable-TLS-1-0 \
	--policy-type-name SSLNegotiationPolicyType \
	--region eu-central-1 \
	--policy-attributes \
    AttributeName=Protocol-TLSv1,AttributeValue=false \
	AttributeName=Protocol-TLSv1.1,AttributeValue=true \
	AttributeName=Protocol-TLSv1.2,AttributeValue=true \
	AttributeName=Server-Defined-Cipher-Order,AttributeValue=true \
	AttributeName=ECDHE-ECDSA-AES128-GCM-SHA256,AttributeValue=true \
	AttributeName=ECDHE-RSA-AES128-GCM-SHA256,AttributeValue=true \
	AttributeName=ECDHE-ECDSA-AES128-SHA256,AttributeValue=true \
	AttributeName=ECDHE-RSA-AES128-SHA256,AttributeValue=true \
	AttributeName=ECDHE-ECDSA-AES128-SHA,AttributeValue=true \
	AttributeName=ECDHE-RSA-AES128-SHA,AttributeValue=true \
	AttributeName=ECDHE-ECDSA-AES256-GCM-SHA384,AttributeValue=true \
	AttributeName=ECDHE-RSA-AES256-GCM-SHA384,AttributeValue=true \
	AttributeName=ECDHE-ECDSA-AES256-SHA384,AttributeValue=true \
	AttributeName=ECDHE-RSA-AES256-SHA384,AttributeValue=true \
	AttributeName=ECDHE-RSA-AES256-SHA,AttributeValue=true \
	AttributeName=ECDHE-ECDSA-AES256-SHA,AttributeValue=true \
	AttributeName=AES128-GCM-SHA256,AttributeValue=true \
	AttributeName=AES128-SHA256,AttributeValue=true \
	AttributeName=AES128-SHA,AttributeValue=true \
	AttributeName=AES256-GCM-SHA384,AttributeValue=true \
	AttributeName=AES256-SHA256,AttributeValue=true

To activate the policy:

	aws elb set-load-balancer-policies-of-listener --load-balancer-name myloadbalancer --load-balancer-port 443 --policy-name disable-TLS-1-0 --region eu-central-1
