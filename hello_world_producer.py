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
exchange_name = "slack_notifications"
channel.exchange_declare(exchange_name, "direct")

# Declaring queues
queues = {"hr": "hr_queue", "support": "support_queue", "marketing": "marketing_queue"}
for _, queue_name in queues.items():
    channel.queue_declare(queue=queue_name, durable=True)


# Bind the queues to the exchange
for binding_key, queue_name in queues.items():
    channel.queue_bind(
        exchange=exchange_name, queue=queue_name, routing_key=binding_key
    )


def send_to_queue(channel, routing_key, body):
    """Send message to queue."""
    channel.basic_publish(
        exchange=exchange_name, routing_key=routing_key, body=body
    )
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
