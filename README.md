# AWS Lambda - EC2 State Change Notification to Slack



**Amazon EventBridge -> Lambda -> Slack notification.**



## ○Lambda

- [Python 3.9](https://github.com/yinyangdev/docker-aws)

  ```shell
  git clone https://github.com/yinyangdev/aws-lambda-ec2-statechange-notification-to-slack.git
  cd aws-lambda-ec2-statechange-notification-to-slack
  pip install requests boto3 -t .
  chmod -R 755 ./*
  zip -r lambda.zip *
  ```

  

## ○EventBridge - Event pattern

```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"]
}
```



## ○Lambda - Environment variables

| Key               | Value       |
| ----------------- | ----------- |
| SLACK_WEBHOOK_URL | Webhook URL |



## ○Lambda IAM Role Policy 

- AWSLambdaBasicExecutionRole
- AmazonEC2ReadOnlyAccess



