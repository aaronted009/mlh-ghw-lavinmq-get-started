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

user_groups = ["hr", "marketing", "support"]

# Get user group argument from commandline
user_group = sys.argv[1]
if not user_group:
    sys.stderr.write("Usage: %s [hr] [marketing] [support]\n" % sys.argv[0])
    sys.exit(1)

if user_group not in user_groups:
    sys.stderr.write(
        "Invalid argument - allowed arguments: %s [hr] [marketing] [support]\n"
        % sys.argv[0]
    )
    sys.exit(1)

queue_name = user_group + "_queue"
queue_binding_key = user_group

# Create a direct exchange called "slack_notifications"
exchange_name = "slack_notifications"
channel.exchange_declare(exchange_name, "direct")

# Declare queues
channel.queue_declare(
    queue=queue_name, durable=True
)  # This is idempotent : meaning we could be not declaring this, as a queue for the producer has already been created and queue can only be declared once (regardless of how many times we run the command, only one queue will be created). This is still declared as the consumer process can be started first.


# Create a binding
channel.queue_bind(
    exchange=exchange_name, queue=queue_name, routing_key=queue_binding_key
)


def callback(ch, method, properties, body):
    print(f"[✅] Received #{ body }")


channel.basic_consume(
    queue_name,
    callback,
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
