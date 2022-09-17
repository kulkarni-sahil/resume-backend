import os
import boto3

VISITOR_COUNT_TABLE_NAME = os.environ.get('VISITOR_COUNT_TABLE_NAME', 'visitor-count-resume-backend')

dynamodb = boto3.resource('dynamodb')
visitor_count_table = dynamodb.Table(VISITOR_COUNT_TABLE_NAME)


def lambda_handler(event=None, context=None):
    response = visitor_count_table.get_item(
        Key={
            'pk': 'visitor_count'
        },
        ConsistentRead=True
    )
    item = response['Item']
    visitor_count = item['count']
    print(f"{visitor_count=}")
    visitor_count_table.put_item(
        Item={
            'pk': 'visitor_count',
            'count': visitor_count + 1
        }
    )

    return {
      'statusCode': 200,
      'body': f'{visitor_count}'
    }


if __name__ == "__main__":
    lambda_handler()
