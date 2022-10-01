import os
import boto3
import logging

# https://realpython.com/python-logging/#classes-and-functions
# https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

VISITOR_COUNT_TABLE_NAME = os.environ.get('VISITOR_COUNT_TABLE_NAME', 'visitor-count-resume-backend')


def lambda_handler(event=None, context=None):
    logger.debug("Execution Start")

    dynamodb = boto3.resource('dynamodb')
    visitor_count_table = dynamodb.Table(VISITOR_COUNT_TABLE_NAME)

    logger.info("Querying DynamoDB Table")
    response = visitor_count_table.get_item(
        Key={
            'pk': 'visitor_count'
        },
        ConsistentRead=True
    )
    item = response['Item']
    visitor_count = item['count']
    logger.debug(f"Got {visitor_count=} from table")

    logger.info("Updating table with visitor count")
    visitor_count_table.put_item(
        Item={
            'pk': 'visitor_count',
            'count': visitor_count + 1
        }
    )
    logger.debug("Execution complete")
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*"
        },
        'body': f'{visitor_count}'
    }


if __name__ == "__main__":
    lambda_handler()
