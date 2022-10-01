import boto3
import unittest
from moto import mock_dynamodb

from src import index


class MyTestCase(unittest.TestCase):

    @mock_dynamodb
    def test_lambda_handler(self):
        # Arrange
        visitor_count_table_name = "test-visitor-count"
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'pk',
                    'AttributeType': 'S'
                },
            ],
            TableName=visitor_count_table_name,
            KeySchema=[
                {
                    'AttributeName': 'pk',
                    'KeyType': 'HASH'
                },
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        table.put_item(
            Item={
                'pk': 'visitor_count',
                'count': 1
            }
        )

        # Act
        index.VISITOR_COUNT_TABLE_NAME = visitor_count_table_name
        actual_response = index.lambda_handler()

        # Assert
        expected = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': '1'
        }
        self.assertEqual(actual_response, expected)


if __name__ == '__main__':
    unittest.main()
