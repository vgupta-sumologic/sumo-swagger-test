# little changes from: https://github.com/pglass/designate-locust/blob/master/graphite_client.py
import sys
import os
import time
import locust
import gevent

# from gevent.socket import socket
from gevent.queue import Queue

graphite_queue = Queue()
user_count_map = {}
HttpsLogServer='https://stag-events.sumologic.net/receiver/v1/http/ZaVnC4dhaV0ovzMt2yphbE2j8kzawgBL1WP7m_mon8BkoLwX5429XdmxGpKXGlhg62V0jMEOo7g61a6yUalUtrxyKXbLYpUa15mh_Q8CW-h9R3XMs8aH3A=='
# HOST = os.getenv('GRAPHITE_HOST', '')
# PORT = os.getenv('GRAPHITE_PORT', '443')

def is_slave():
    return '--slave' in sys.argv

def graphite_worker():
    """The worker pops each item off the queue and sends it to graphite."""
    # print('connecting to graphite on (%s, %s)' % (HOST, PORT))
    # sock = socket()
    # try:
    #     sock.connect((HOST, PORT))
    # except Exception as e:
    #     raise Exception(
    #         "Couldn't connect to Graphite server {0} on port {1}: {2}"
    #         .format(HOST, PORT, e))
    # print('done connecting to graphite')

    while True:
        data = graphite_queue.get()
        import requests
        r = requests.post(HttpsLogServer, data=data)
        print(r.status_code, r.reason)
        # print "graphite_worker: got data {0!r}".format(data)
        # print "sending data"
        # sock.sendall(data)

def _get_requests_per_second_graphite_message(stat, client_id):
    request = stat['method'] + '.' + stat['name'].replace(' - ', '.').replace('/', '-')
    graphite_key = "locust.{0}.reqs_per_sec".format(request)
    graphite_data = "".join(
        "{0} {1} {2}\n".format(graphite_key, count, epoch_time)
        for epoch_time, count in stat['num_reqs_per_sec'].iteritems())
    return graphite_data

def _get_response_time_graphite_message(stat, client_id):
    request = stat['method'] + '.' + stat['name'].replace(' - ', '.').replace('/', '-')
    graphite_key = "locust.{0}.response_time".format(request)
    epoch_time = int(stat['start_time'])

    # flatten a dictionary of {time: count} to [time, time, time, ...]
    response_times = []
    for t, count in stat['response_times'].iteritems():
        for _ in xrange(count):
            response_times.append(t)

    graphite_data = "".join(
        "{0} {1} {2}\n".format(graphite_key, response_time, epoch_time)
        for response_time in response_times)
    return graphite_data

def graphite_producer(client_id, data):
    """This takes a Locust client_id and some data, as given to
    locust.event.slave_report handlers."""
    #print "Got data: ", data, 'from client', client_id
    for stat in data['stats']:
        graphite_data = (
            _get_response_time_graphite_message(stat, client_id)
            + _get_requests_per_second_graphite_message(stat, client_id))
        graphite_queue.put(graphite_data)
        print(graphite_data)
        print("I am ALIVEEEEEEE")

def setup_graphite_communication():
    # only the master sends data to graphite
    if not is_slave():
        gevent.spawn(graphite_worker)
        locust.events.slave_report += graphite_producer