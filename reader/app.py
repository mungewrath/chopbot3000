import json
from cardrepository import CardRepository
# import ptvsd
import time
import urllib.parse
import requests

# Uncomment for local debugging
# ptvsd.enable_attach(address=('0.0.0.0', 5858), redirect_output=True)
# ptvsd.wait_for_attach()


def lambda_handler(event, context):
    try:
        """Sample pure Lambda function

        Parameters
        ----------
        event: dict, required
            API Gateway Lambda Proxy Input Format

            Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

        context: object, required
            Lambda Context runtime methods and attributes

            Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

        Returns
        ------
        API Gateway Lambda Proxy Output Format: dict

            Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
        """

        print("Event:")
        print(event)

        print("Context:")
        print(context)

        body = event['body-json']
        # Convert to dictionary. Each value is an array, even if it's just got one value
        data = urllib.parse.parse_qs(body)

        query_text = data['text'][0]
        response_url = data['response_url'][0]

        start_time = time.time()

        card_repo = CardRepository()

        fetch_time = time.time()


        image_path = card_repo.get_card_path(query_text)

        if image_path is None:
            response_text = f"Sorry, couldn't find a card matching `{query_text}`."
        else:
            response_text = f"Here's what I found for `{query_text}`: \n{image_path}"

        search_time = time.time()

        response_payload = {
            'text': response_text,
            'response_type': 'in_channel'
        }

        print(f"response_url={response_url}")
        print(f"response_text={response_text}")

        requests.post(response_url, json=response_payload)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "response_text": response_text,
                "fetch_time": fetch_time - start_time,
                "search_time": search_time - fetch_time
            })
        }
    except Exception as e:
        response_payload = {
            'text': f'Something went wrong:worried:: {type(e)} {e}',
            'response_type': 'in_channel'
        }
        requests.post(response_url, json=response_payload)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "response_text": "Error occurred"
        })
    }

