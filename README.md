# Get started with LavinMQ

Creation of a message producer and message consumer using LavinMQ message broker.

### Steps :
Clone the repository and open a terminal at the root of the cloned repository.

1. Create a virtual environment and activate it : 
   ```
   python3.12 -m venv venv
   ```
   ```
   . venv/bin/activate
   ```

2. Install the dependencies :
   ```
   pip install -r requirements.txt
   ```

3. Initialize your environment variable :
   ```
   cp .env.example .env
   ```
   Fill in `CLOUDAMQP_URL` by creating a free LavinMQ instance on [CloudAMQP](https://www.cloudamqp.com/docs/lavinmq-server.html).

4. Start each of the consumers, one per terminal : 
   ```
   python consumer.py hr
   ```
   ```
   python consumer.py marketing
   ```
   ```
   python consumer.py support
   ```
    

5. Start the producer : 
   ```
   python producer.py
   ```