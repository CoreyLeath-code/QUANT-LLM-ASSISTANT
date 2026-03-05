from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def stream_market_data():
    while True:
        data = {
            "symbol": "AAPL",
            "price": 180.45,
            "volume": 1200000
        }
        producer.send("market_data", data)
        time.sleep(1)
