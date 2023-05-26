import json

import pytest
from unittest import mock
from unittest.mock import patch

from reader import app

@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body-json": "'token=rTyCTVa4LMQ2gMI0PSpwGxQA&team_id=T024F3C1G&team_domain=pariveda&channel_id=C04C9LWDZR8&channel_name=netrunner&user_id=URYK9H94M&user_name=jim.brown&command=%2Fchopbot&text=Ken+Tenma&is_enterprise_install=false&response_url=https%3A%2F%2Flocalhost%2Fcommands%2FT024F3C1G%2F5342000715232%2Fv2303Z0HJCZR1O6LrugOLR8u'",
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "POST",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }

@pytest.fixture()
def ndb_stub():
    with open("./tests/integration/netrunnerdb_stub.json") as f:
        data = json.load(f)
        return data

@patch("requests.post")
@patch("requests.get")
def test_lambda_handler(get, post, apigw_event, ndb_stub):
    mocked_response = mock.Mock()

    get.return_value = mocked_response
    mocked_response.status_code = 200
    mocked_response.json.return_value = ndb_stub

    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    get.assert_called_once()
    post.assert_called_once()

    query_text = "Ken Tenma"
    image_path = "https://static.nrdbassets.com/v1/large/05029.jpg"

    assert ret["statusCode"] == 200
    assert data["response_text"] == f"Here's what I found for `{query_text}`: \n{image_path}"
