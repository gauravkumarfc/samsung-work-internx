import boto3

def check_image_safety(image_id):
   
    if not is_trusted_source(image_id):
        return False

  
    if is_older_os_version(image_id):
        return False

  
    if has_vulnerabilities(image_id):
        return False

 
    if not is_image_approved(image_id):
        return False

    if not is_latest_ami(image_id):
        return False

    return True

def is_trusted_source(image_id):

    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_images(ImageIds=[image_id])

    if 'Images' in response:
        image = response['Images'][0]
        if 'OwnerId' in image and 'Public' in image['ImageLocation']:
            return True

    return False

def is_older_os_version(image_id):
  
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_images(ImageIds=[image_id])

    if 'Images' in response:
        image = response['Images'][0]
        if 'Name' in image and 'OldVersion' in image['Name']:
            return True

    return False

def has_vulnerabilities(image_id):
    ec2_client = boto3.client('ec2')

    # Describe the launch permissions of the image
    response = ec2_client.describe_image_attribute(
        ImageId=image_id,
        Attribute='launchPermission'
    )

    if 'LaunchPermissions' in response:
        launch_permissions = response['LaunchPermissions']

        # Check if there are any public launch permissions
        for permission in launch_permissions:
            if 'Group' in permission and permission['Group'] == 'all':
                return True

    return False
   

def is_image_approved(image_id):
    ec2_client = boto3.client('ec2')

    # Get the tags of the image
    response = ec2_client.describe_images(
        ImageIds=[image_id]
    )

    if 'Images' in response and len(response['Images']) > 0:
        image_tags = response['Images'][0]['Tags']

        # Check if the image has an "Approved" tag with a value of "Yes"
        for tag in image_tags:
            if tag['Key'] == 'Approved' and tag['Value'].lower() == 'yes':
                return True

    return False
  

def is_latest_ami(image_id):
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_images(
        Owners=['amazon'],
        Filters=[
            {'Name': 'name', 'Values': ['*amazon-ecs-optimized']},
            {'Name': 'state', 'Values': ['available']},
            {'Name': 'architecture', 'Values': ['x86_64']},
        ],
        SortBy='CreationDate',
        MaxResults=1
    )
   
    if 'Images' in response and len(response['Images']) > 0:
        latest_ami_id = response['Images'][0]['ImageId']
        # Check if the given image ID matches the latest AWS EGS-optimized AMI ID
        return image_id == latest_ami_id

    return False




