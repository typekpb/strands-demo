# Run locally
```shell
 .venv/bin/pip install -r requirements.txt
 source .venv/bin/activate && python -m local.py
```

# Run in AWS
1. build+deploy:
    ```shell
    terraform init
    terraform plan -out tfplan
    terraform apply "tfplan"
    ```
1. run in Amazon Console with sample payload: `test-lambda.json`