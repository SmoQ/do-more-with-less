#!/bin/bash
aws configure set default.aws_secret_access_key dummy_secret_key \
    && aws configure set default.aws_access_key_id dummy_access_key_id
npx sls dynamodb start --config=serverless.yml --stage=local &
npx sls offline --config=serverless.yml --stage=local
