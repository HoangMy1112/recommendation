# import boto3
# from botocore.exceptions import NoCredentialsError, PartialCredentialsError
# import json

# class DynamoDBQuery:
#     def __init__(self, region_name, table_name, partition_key, partition_value):
#         self.dynamodb = boto3.client("dynamodb", region_name=region_name)
#         self.table_name = table_name
#         self.partition_key = partition_key
#         self.partition_value = partition_value

#     def query_posts(self):
#         try:
#             posts_response = self.dynamodb.query(
#                 TableName=self.table_name,
#                 KeyConditionExpression=f"{self.partition_key} = :pk",
#                 ExpressionAttributeValues={
#                     ":pk": {"S": self.partition_value},
#                 },
#             )

#             posts = posts_response.get("Items", [])
#             info = []

#             for item in posts:
#                 user_id = item.get("UserID", {}).get("S", "Unknown")
#                 place_id = item.get("PlaceID", {}).get("S", "Unknown")
#                 rating = float(item.get("RatingValue", {}).get("N", 0))
#                 info.append(
#                     {
#                         "UserID": user_id,
#                         "PlaceID": place_id,
#                         "Rating": rating,
#                     }
#                 )

#             return info  # Returning a list of dictionaries

#         except NoCredentialsError:
#             raise Exception("Error: No AWS credentials found. Ensure AWS credentials are configured.")
#         except PartialCredentialsError:
#             raise Exception("Error: Incomplete AWS credentials. Double-check your AWS configuration.")
#         except Exception as e:
#             raise Exception(f"An error occurred while querying DynamoDB: {e}")

# if __name__ == "__main__":
#     query = DynamoDBQuery(
#         region_name="ap-southeast-2",
#         table_name="nc-table",
#         partition_key="pk",
#         partition_value="POST#",
#     )
#     try:
#         # Query and return the JSON-formatted results
#         result = query.query_posts()
#         print(result)  # This will output the result to the console
#     except Exception as e:
#         # If there's an error, print the error message
#         print(f"An error occurred: {e}")


import boto3
from boto3.dynamodb.conditions import Key
class DynamoDBQuery:
    def __init__(self, region_name, table_name):
        self.dynamodb = boto3.resource("dynamodb", 
                                       aws_access_key_id="AKIA5HPKATSKF6Z37DJ3",
                                       aws_secret_access_key="U7HtkAk6r30htxEnOXC1SHk49VWRD0ymIgfvuei",
                                       region_name=region_name
                                       )
        self.table = self.dynamodb.Table(table_name)

    def query_items(self, partition_key_value):
        try:
            response = self.table.query(
                KeyConditionExpression=Key('pk').eq(partition_key_value)
            )
            return response.get("Items", [])
        except Exception as e:
            raise Exception(f"Failed to query items: {e}")

    def merge_results(self, users, places, posts):
        place_ids = {place['sk']: place for place in places}
        user_ids = {user['sk']: user for user in users}
        results = []

        for post in posts:
            user_id = post.get("UserID")
            place_id = post.get("PlaceID")
            rating = float(post.get("RatingValue", "0"))

            if user_id in user_ids and place_id in place_ids:
                results.append({
                    "UserID": user_id,
                    "PlaceID": place_id,
                    "Rating": rating
                })

        # Add missing combinations with rating 0
        for user_id in user_ids:
            for place_id in place_ids:
                if not any(r['UserID'] == user_id and r['PlaceID'] == place_id for r in results):
                    results.append({
                        "UserID": user_id,
                        "PlaceID": place_id,
                        "Rating": 0
                    })

        return results

    def execute_query(self):
        users = self.query_items("USER#")
        places = self.query_items("PLACE#")
        posts = self.query_items("POST#")

        return self.merge_results(users, places, posts)

# if __name__ == "__main__":
#     query = DynamoDBQuery(region_name="ap-southeast-2", table_name="nc-table")
#     try:
#         result = query.execute_query()
#         print(result)
#     except Exception as e:
#         print(f"An error occurred: {e}")


# import boto3
# from botocore.exceptions import NoCredentialsError, PartialCredentialsError
# import json
# dynamodb = boto3.client("dynamodb", region_name="ap-southeast-2")

# table_name = "nc-table"

# partition_key = "pk" 
# partition_value2 = "POST#"  

# try:
#     postsResponse = dynamodb.query(
#         TableName='nc-table',
#         KeyConditionExpression=f"{partition_key} = :pk",
#         ExpressionAttributeValues={
#             ":pk": {"S": partition_value2} 
#         }
#     )
    
#     posts = postsResponse.get("Items", [])
#     info = []

#     for item in posts:
#         user_id = item.get("UserID", {}).get("S", "Unknown") 
#         place_id = item.get("PlaceID", {}).get("S", "Unknown")
#         rating = float(item["RatingValue"]["N"])
#         info.append({
#                 "UserID": user_id,
#                 "PlaceID": place_id,
#                 "Rating": rating
#             })
#     info_json = json.dumps(info, indent=4)
#     print(info_json)


# except NoCredentialsError:
#     print("Error: No AWS credentials found. Ensure AWS credentials are configured.")
# except PartialCredentialsError:
#     print("Error: Incomplete AWS credentials. Double-check your AWS configuration.")
# except Exception as e:
#     print(f"An error occurred while querying DynamoDB: {e}")
