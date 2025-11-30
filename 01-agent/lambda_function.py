from agent import run_agent

def lambda_handler(event, context):
    message = event.get("message", "")
    response = run_agent(message)
    return {
        "statusCode": 200,
        "body": str(response)
    }
