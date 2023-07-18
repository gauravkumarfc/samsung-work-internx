import boto3


def delete_root_access_key(access_key_id):
    iam_client = boto3.client("iam")

    # Delete the access key
    iam_client.delete_access_key(UserName="root", AccessKeyId=access_key_id)


def check_root_access_key():
    iam_client = boto3.client("iam")

    # Get the root account's access keys
    response = iam_client.list_access_keys(UserName="root")

    if len(response["AccessKeyMetadata"]) == 0:
        print("PASS - No access keys found for the root account.")
        print("Recommended Value:")
        print("1. Ensure there is no history of issuing Access Key.")
    else:
        print("FAIL - Access keys found for the root account.")

        # Additional checks for access key history and status
        for access_key in response["AccessKeyMetadata"]:
            access_key_id = access_key["AccessKeyId"]
            access_key_status = access_key["Status"]

            print("Access Key ID:", access_key_id)
            print("Access Key Status:", access_key_status)

            if access_key_status == "Active":
                print("Deleting access key...")
                delete_root_access_key(access_key_id)
                print("Access key deleted.")

        print("Recommended Value:")
        print(
            '2. In case there is a history of issuing an Access Key: Confirm "Status Deleted".'
        )


# Call the function to check the usage of access keys in the root account
check_root_access_key()
