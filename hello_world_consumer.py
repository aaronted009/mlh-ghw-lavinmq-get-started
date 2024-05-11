import sys
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

# Declare a queue
channel.queue_declare(
    queue="hello_world"
)  # This is idempotent : meaning we could be not declaring this, as a queue for the producer has already been created and queue can only be declared once (regardless of how many times we run the command, only one queue will be created). This is still declared as the consumer process can be started first.


def callback(ch, method, properties, body):
    print(f"[✅] Received #{ body }")


channel.basic_consume(
    "hello_world",
    callback,
    auto_ack=True,
)

try:
    print("\n[❎] Waiting for messages. To exit press CTRL+C \n")
    channel.start_consuming()
except Exception as e:
    print(f"Error: #{e}")
try:
    sys.exit(0)
except SystemExit:
    os._exit(0)
