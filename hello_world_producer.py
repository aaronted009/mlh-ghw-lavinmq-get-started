import pika, os
from dotenv import load_dotenv

load_dotenv()

# Access the CLOUDAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get("CLOUDAMQP_URL", "amqp://guest:guest@localhost:5672/%2f")

# Create a connection
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)

# Create a channel
channel = connection.channel()
print("[✅] Channel over a connection created")

# Create a direct exchange called "slack_notifications"
channel.exchange_declare("slack_notifications", "direct")

# Declaring queues
channel.queue_declare(queue="hr_queue")
channel.queue_declare(queue="marketing_queue")
channel.queue_declare(queue="support_queue")

# Bind the queues to the exchange
channel.queue_bind("hr_queue", "slack_notifications", "hr")
channel.queue_bind("marketing_queue", "slack_notifications", "marketing")
channel.queue_bind("support_queue", "slack_notifications", "support")


def send_to_queue(channel, routing_key, body):
    """Send message to queue."""
    channel.basic_publish(exchange="slack_notifications", routing_key=routing_key, body=body)
    print(f"[📥] Message sent to queue - msg:  #{body}")


# Publish messages
send_to_queue(channel=channel, routing_key="hr", body="HR notification")
send_to_queue(channel=channel, routing_key="marketing", body="Marketing notification")
send_to_queue(channel=channel, routing_key="support", body="Support notification")
try:
    connection.close()
    print("[❎] Connection closed")
except Exception as e:
    print(f"Error: #{e}")
