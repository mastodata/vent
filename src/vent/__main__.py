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

    def on_status_update(self, status):
        _process_status(status)

    def on_update(self, status):
        _process_status(status)


def _process_status(status):
    pub.send_json(status, cls=DateTimeEncoder)


if __name__ == "__main__":
    ctx = zmq.Context()
    pub = ctx.socket(zmq.PUSH)
    pub.connect(os.environ["TASK_ADDRESS"])

    print("starting")
    m = mastodon.Mastodon(api_base_url=os.environ["API_BASE_URL"], access_token=os.environ.get("MASTODON_ACCESS_TOKEN"))
    print("authenticated")
    h = m.stream_public(QueueingListener())
