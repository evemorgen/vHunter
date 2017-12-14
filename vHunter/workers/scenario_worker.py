import logging
import asyncio

from utils import Config
from utils import async_every
from utils import Scenarios

from drivers import *  # noqa: F401,F403


class ScenarioWorker:
    def __init__(self):
        self.config = Config()
        self.counter = 0
        self._running = False
        logging.info("Scenario worker started")
        self.ioloop = asyncio.get_event_loop()
        self.ioloop.call_soon(asyncio.ensure_future, self.run())

    def load_driver(self, name, scenario):
        return globals()[name](scenario)

    @async_every(minutes=1)
    async def run(self):
        if self._running is True:
            logging.info("Worker is still working on last course, waiting")
            return
        self._running = True
        drivers = []
        logging.info("Scenario worker running for %s time!", self.counter)
        scenarios = Scenarios()
        for name in scenarios:
            driver = self.load_driver(scenarios[name]['driver'], scenarios[name])
            drivers.append(driver.perform())
        self.counter = self.counter + 1
        for driver in drivers:
            await driver
        #self.ioloop.run_until_complete(asyncio.gather(*drivers))
        logging.info("Done performing scenarios, setting flag to idle")
        self._running = False
