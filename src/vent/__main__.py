import datetime as dt
import json
import os

import mastodon
import zmq


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, dt.datetime):
            return o.isoformat()


class QueueingListener(mastodon.StreamListener):
    def __init__(self):
        super().__init__()

    def on_update(self, status):
        pub.send_string(str(status["id"]))


if __name__ == "__main__":
    ctx = zmq.Context()
    pub = ctx.socket(zmq.PUB)
    pub.bind(os.environ["VENT_ADDRESS"])

    print("starting")
    m = mastodon.Mastodon(api_base_url="https://fosstodon.org")
    print("connected")
    h = m.stream_public(QueueingListener())
