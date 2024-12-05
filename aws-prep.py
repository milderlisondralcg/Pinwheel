# Test AWS connections

import boto3
# Create boto3 client
s3client = boto3.client(
    service_name='s3',
    aws_access_key_id='AKIA2OZOUY6TQNTHQJTR',
    aws_secret_access_key='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'
)

s3bucket = 'admintemp'
all_objects = s3client.list_objects(Bucket=s3bucket)
print(f"List of obj in bucket {s3bucket}: ")

for a in all_objects['Contents']:
    for b in a:
        print(str(b) + " " + str(a[b]))
 

    #print(a['Key'])
    
#s3client.delete_object(Bucket=s3bucket,Key='BSIDE-availability-2980.json')

#def del_file(filename):
 #   s3client.delete_object(Bucket=s3bucket,Key='BSIDE-availability-2980.json')

# Print out bucket names
#for bucket in s3bucket.all():
 #   print(bucket.name)


