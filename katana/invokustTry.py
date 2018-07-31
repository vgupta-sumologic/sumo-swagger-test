import logging
from invokust import LambdaLoadTest

logging.basicConfig(level=logging.INFO)

lambda_payload = {
    'locustfile': 'test.py',
    'host': 'https://nite-api.sumologic.net',
    'num_requests': '20',
    'num_clients': '1',
    'hatch_rate': 1
}

load_test = LambdaLoadTest(
  lambda_function_name='lambda_locust',
  threads=2,
  ramp_time=0,
  time_limit=30,
  lambda_payload=lambda_payload
)

load_test.run()