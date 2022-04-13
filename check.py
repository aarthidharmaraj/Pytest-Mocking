'''This script is for checking testcases for changing file to sql'''
def change_file_sqlt(s3_res,bucket_name,database_name,table_name):
    """This method changes the file format to sql by getting file from s3"""
    exceptionfile = []
    try:
        my_bucket = s3_res.Bucket(bucket_name)
        for obj in my_bucket.objects.filter(
        Prefix=database_name/table_name
        ):
            if obj.key.endswith(".txt"):
                copy_source = {"Bucket": bucket_name, "Key": obj.key}
                s3_res.Object(
                bucket_name,database_name / table_name.sql,
                ).copy_from(CopySource=copy_source)
                s3_res.Object(bucket_name, obj.key).delete()
                print("\nSuccessfully renamed and changed the location of sql file")
                return 'success'
    except Exception as excep:
        exceptionfile.extend([table_name,excep])
        print(
                "\ncannot be renamed in [ ",
               table_name,
                " ] of [",
               database_name,
                " ]because of this error\n",
                exceptionfile,
            )
        return 'failure'
