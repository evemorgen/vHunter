import asyncio
import logging
from singleton_decorator import singleton

from vHunter.utils import async_every
from vHunter.notifiers import *  # noqa: F401,F403


@singleton
class NotifyAggregatorWorker:
    def __init__(self):
        self.things_to_send = {}
        self.ioloop = asyncio.get_event_loop()
        self.ioloop.call_soon(asyncio.ensure_future, self.run())

    def agregate(self, notifier_class, receivers, vulnerabilities):
        for receiver in receivers:
            if self.things_to_send.get((notifier_class, receiver)) is None:
                self.things_to_send[(notifier_class, receiver)] = []
            self.things_to_send[(notifier_class, receiver)].append(vulnerabilities)

    def load_notifier(self, name):
        return globals()[name]()

    @async_every(minutes=20)
    async def run(self):
        logging.info("sending agregated notifications")
        for notifier, receiver in self.things_to_send:
            logging.debug("trying to send stuff to %s via %s" % (receiver, notifier))
            final_dict = {}
            for scenario_set in self.things_to_send[(notifier, receiver)]:
                for host in scenario_set:
                    if host not in final_dict:
                        final_dict[host] = []
                    final_dict[host] = final_dict[host] + scenario_set[host]
            logging.debug("final merged vulns are: %s", final_dict)
            notify = self.load_notifier(notifier)
            notify.send_msg([receiver, ], final_dict)
        self.things_to_send = {}


def agregate(notifier_class, receivers, vulnerabilities):
    NotifyAggregatorWorker().agregate(notifier_class, receivers, vulnerabilities)