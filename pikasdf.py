import pika

# Set up connection parameters
credentials = pika.PlainCredentials('jaykin', 'jaykin')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

# Connect to RabbitMQ server
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='my_queue')

# Close the connection
connection.close()
