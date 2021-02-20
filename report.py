import requests
import psycopg2
import ccxt
import boto3
from botocore.exceptions import ClientError

def main():

    exchange = ccxt.binance({
        'rateLimit':1000,
        'headers':{
            
        },
        'interval':"1m",
        'options':{
            'adjustedForTimeDifference': True,
        }
    })

    exchange.load_markets()

    symbols = exchange.symbols

    CONNECTION = "postgres://mani:abcd@localhost:5432/nyc_data"
    conn = None
    
    SENDER = "teja3536mani@gmail.com"


    RECIPIENT = "manitejavuppula@gmail.com"

    AWS_REGION = "ap-south-1"

    SUBJECT = "Amazon SES Test (SDK for Python)"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                "This email was sent with Amazon SES using the "
                "AWS SDK for Python (Boto)."
                )
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Amazon SES Test (SDK for Python)</h1>
    <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
        AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
                """            

    CHARSET = "UTF-8"

    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

    # try:
    #     conn=psycopg2.connect(CONNECTION)
    #     cur = conn.cursor()
    #     QUERY = "SELECT market, COUNT(*) as count FROM one_tick_data GROUP BY market"
    #     cur.execute(QUERY)
    #     for symbol in symbols:

    # except (Exception, psycopg2.Error) as error:
    #     print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()

if __name__ == "__main__":
    main()