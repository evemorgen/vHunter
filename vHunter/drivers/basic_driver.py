import logging
import socket

from utils import Config
from utils import run_cmd
from utils.distro import detect_distro

from db import *         # noqa: F401,F403
from notifiers import *  # noqa: F401,F403


class BasicDriver:
    def __init__(self, scenario):
        self.scenario = scenario
        logging.error(self.scenario['receivers'])
        self.hostname = socket.gethostname()
        self.config = Config()
        self.dbapi = self.make_instance("NvdapiAdapter", scenario['min_score'])

    def prepare_message(self, vulns):
        logging.debug("all found vulns are: %s", vulns)
        message_dict = {
            self.hostname: []
        }
        for vuln in vulns:
            message_dict[self.hostname].append({
                'name': vuln['product'][0]['name'],
                'version': vuln['product'][0]['version'],
                'cve': vuln['cve'],
                'score': vuln['score'],
                'description': vuln['description']
            })
        return message_dict

    def make_instance(self, name, *args, **kwargs):
        try:
            return globals()[name](*args, **kwargs)
        except KeyError:
            logging.error('Tried to load %s class, and failed. Typo perhaps?', name)
            raise

    async def perform(self):
        distro = detect_distro()
        job_selector = {
            'linux': distro['version'],
            'mac_os': distro['distro']
        }
        if job_selector[distro['distro']] in self.scenario['job']:
            res = await run_cmd(self.scenario['job'][job_selector[distro['distro']]])
        else:
            res = await run_cmd(self.scenario['job']['default'])

        all_vulns = []
        for thing in res.split("\n"):
            try:
                name, version = thing.split(",")
                vulns = await self.dbapi.check(name, version=version)
                all_vulns = all_vulns + vulns
            except ValueError as exc:
                logging.exception("Bad line format, it takes name and version separated by comma 'name,version'")

        for notifier_name in self.scenario['notifiers']:
            notifier = self.make_instance(notifier_name)
            notifier.send_msg(self.scenario['receivers'], self.prepare_message(all_vulns))
