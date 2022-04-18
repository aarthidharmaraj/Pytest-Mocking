"""This module has script for testing mocking of AWS services, tests the python script of changing file in sql format"""
import os
import pytest
import boto3
from moto import mock_athena, mock_glue, mock_s3
from check import *

# class Renamsesql:
#     def __init__(self, bucket_name,database_name,table_name):
#         self.bucket_name = bucket_name
#         self.database_name=database_name
#         self.table_name=table_name


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def test_database_tables():
    """This method tests the create database in glue from mocked AWS services"""
    with mock_glue():
        glue_client = boto3.client("glue", region_name="us-east-1")
        response = glue_client.create_database(
            DatabaseInput={
                "Name": "SampleTestDatabase",
                "Description": "Sample database created for testing",
            }
        )
        response_data = glue_client.get_databases()
        table = glue_client.create_table(
            DatabaseName="SampleTestDatabase",
            TableInput={
                "Name": "table1",
                "StorageDescriptor": {
                    "Columns": [{"Name": "column1"}],
                    "SortColumns": [{"Column": "column1", "SortOrder": 123}],
                },
                "PartitionKeys": [{"Name": "column1"}],
            },
            PartitionIndexes=[
                {
                    "Keys": [
                        "key1",
                    ],
                    "IndexName": "index1",
                }
            ],
        )
        response_table = glue_client.get_tables(DatabaseName="SampleTestDatabase")
        list = [response_table["TableList"]]
        yield list


# @mock_glue
# def test_create_database(database_tables):
#     """This method tests for creating databases"""
#     assert True


# @mock_glue
# def test_get_databases(database_tables):
#     """This method tests for getting databases"""
#     assert True


# @mock_glue
# def test_cretae_table(database_tables):
#     """This method tests for creating table"""
#     assert True


@mock_athena
def test_start_query_execution():
    """This method tests the start query execution of athena"""
    client = boto3.client("athena", region_name="us-east-1")
    bucket = "test_bucket"
    database = "database1"
    table = "table1"
    sec_response = store_sql_query_s3(client, bucket, database, table)
    assert "QueryExecutionId" in sec_response


def change_sql_undertest():
    """Checks for the python script build for changing sql name"""
    s3_client2 = boto3.resource("s3")
    database_name = "database1"
    table_name = "table1"
    bucket_name = "test_bucket"
    response = change_file_sqlt(s3_client2, bucket_name, database_name, table_name)
    # return obj["Body"].read().decode("utf-8")
    return response


def test_function2():
    """This is a test method for calling function"""
    assert change_sql_undertest() == "success"
