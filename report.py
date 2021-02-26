import requests
import psycopg2
import ccxt
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import json


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

    CONNECTION = "postgres://mani:abcd@localhost:5432/binance_data"
    conn = None

    try:
        conn=psycopg2.connect(CONNECTION)
        cur = conn.cursor()
        QUERY = "SELECT market, 60, COUNT(*), ROUND(COUNT(*)*100.0/60,2) as count FROM one_tick_data where time>= NOW() - INTERVAL '1 HOURS' GROUP BY market"
        cur.execute(QUERY)
        data=cur.fetchall()

    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    data = '\n'.join('%s, %s, %s, %s' % x for x in data)
    
    SENDER = "teja3536mani@gmail.com"

    RECIPIENT = "edul@mudrex.com"

    AWS_REGION = "ap-south-1"

    SUBJECT = "Binance data report"

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

    msg = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    msg['Subject'] = SUBJECT 
    msg['From'] = SENDER 
    msg['To'] = RECIPIENT
    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
    # Add the text and HTML parts to the child container.
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)
    # Define the attachment part and encode it using MIMEApplication.
    att = MIMEText(str(data))
    att.add_header('Content-Disposition','attachment',filename="report.csv")
    msg.attach(msg_body)
    # Add the attachment to the parent container.
    msg.attach(att)
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_raw_email(
            Destinations=[
                msg['To']
            ],
            RawMessage={
                'Data':msg.as_string(),
            },
            Source=msg['From'],
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

if __name__ == "__main__":
    main()
