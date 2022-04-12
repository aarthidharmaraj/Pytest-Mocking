from botocore.exceptions import ClientError
import pytest
import boto3
from moto import mock_athena,mock_glue,mock_s3
import os
@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
@mock_athena
def test_start_query_execution():
    client = boto3.client("athena", region_name="us-east-1")

    sec_response = client.start_query_execution(
        QueryString="query2",
        QueryExecutionContext={"Database": "string"},
        ResultConfiguration={"OutputLocation": "string"},
    )
    assert "QueryExecutionId" in sec_response
@mock_glue
def test_create_database():
    client = boto3.client("glue", region_name="us-east-1")
    response = client.create_database(DatabaseInput={
        'Name': 'SampleTestDatabase',
        'Description': 'Sample database created for testing',
        })
    
@mock_glue
def test_get_databases():
    client = boto3.client("glue", region_name="us-east-1")
    response = client.get_databases()
    dbname=response["DatabaseList"]
    
@mock_glue
def test_get_tables():
    client = boto3.client("glue", region_name="us-east-1")
    response = client.get_tables(DatabaseName='SampleTestDatabase')

@mock_s3
def test_create_bucket(aws_credentials):
    with mock_s3():
        client=boto3.client('s3',region_name='us-east-1')
        response=client.create_bucket(Bucket='sample1')

@mock_s3
def test_put_object(aws_credentials):
    with mock_s3():
        client=boto3.client('s3',region_name='us-east-1')
        response = client.put_object(
        Bucket='sample1',Key='sql_rename.py')
@mock_s3
def test_get_object():
    client=boto3.client('s3',region_name='us-east-1')
    response=client.get_object(Bucket='sample1',Key='sql_rename.py')