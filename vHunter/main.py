import logging

from utils.config import Config
from utils.distro import detect_distro
from utils.distro import check_python
from utils import prepare_asyncio
from utils import parse_args
from utils import setup_logging
from utils import Scenarios
from drivers import BasicDriver
from notifiers import GmailSmtpNotifier

async def main():
    logging.debug("starting main")
    scenarios = Scenarios()
    #driver = BasicDriver(scenarios['list-apps-scenario'])
    driver = BasicDriver(scenarios['list-python-packages-scenario'])
    await driver.perform()


if __name__ == "__main__":
    config = Config()
    args = parse_args()
    config.set_args(args)
    setup_logging(log_file=args.log_file, log_level=args.log_level)
    check_python()
    detect_distro()
    main_loop = prepare_asyncio()
    main_loop.run_until_complete(main())
    main_loop.close()
