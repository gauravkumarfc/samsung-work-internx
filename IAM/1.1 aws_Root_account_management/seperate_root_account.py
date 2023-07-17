import boto3


def check_root_account_separation():
    # Get the AWS account ID
    sts_client = boto3.client("sts")
    account_id = sts_client.get_caller_identity()["Account"]

    # Check if the root account is separated based on purpose of use
    organizations_client = boto3.client("organizations")
    response = organizations_client.describe_account(AccountId=account_id)

    account_type = response["Account"]["Type"]
    if account_type == "ORGANIZATION_MEMBER":
        print("AWS Root account is separated based on purpose of use.")
    else:
        print("AWS Root account is not separated based on purpose of use.")


def check_vpc_peering():
    ec2_client = boto3.client("ec2")

    # Get all VPC peering connections
    response = ec2_client.describe_vpc_peering_connections()

    for peering_connection in response["VpcPeeringConnections"]:
        requester_owner_id = peering_connection["RequesterVpcInfo"]["OwnerId"]
        accepter_owner_id = peering_connection["AccepterVpcInfo"]["OwnerId"]

        if requester_owner_id == accepter_owner_id:
            print("PASS - Requester's Owner and Accepter's Owner of VPC Peering match.")
        else:
            print(
                "FAIL - Requester's Owner and Accepter's Owner of VPC Peering do not match."
            )


# Call the functions to check AWS root account separation and VPC peering
check_root_account_separation()
check_vpc_peering()
