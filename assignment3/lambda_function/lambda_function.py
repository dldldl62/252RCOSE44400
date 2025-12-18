import boto3 
from textblob import TextBlob
import datetime
import json
import os

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("TABLE_NAME", "")

table = dynamodb.Table(TABLE_NAME)
ses = boto3.client("ses")

SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL", "")


def lambda_handler(event, context):
    try:
        if isinstance(event.get("body"), str):
            body = json.loads(event["body"])
        else:
            body = event

        user_name = body.get("user_name", "Anonymous")
        review_text = body.get("review", "")
        timestamp = datetime.datetime.now().isoformat()

        blob = TextBlob(review_text)
        polarity = blob.sentiment.polarity

        if polarity > 0.1:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        table.put_item(
            Item={
                "user_name": user_name,
                "review": review_text,
                "sentiment": sentiment,
                "polarity_score": str(
                    polarity
                ),
                "timestamp": timestamp,
            }
        )

        if sentiment == "Positive":
            ses.send_email(
                Source=SENDER_EMAIL,
                Destination={"ToAddresses": [RECEIVER_EMAIL]},
                Message={
                    "Subject": {"Data": f"[{sentiment}] Review from {user_name}"},
                    "Body": {"Text": {"Data": f"Review: {review_text}"}},
                },
            )

        return {
            "statusCode": 200,
            "body": json.dumps(f"Processed as {sentiment} (Score: {polarity:.2f})"),
        }

    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": "Internal Server Error"}

