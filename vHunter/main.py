import logging

from utils.distro import detect_distro
from utils.distro import check_python
from utils import prepare_asyncio
from utils import parse_args
from utils import setup_logging


if __name__ == "__main__":
    args = parse_args()
    setup_logging(log_file=args.log_file, log_level=args.log_level)
    check_python()
    detect_distro()
    prepare_asyncio()
    logging.debug("HOLY SHIT IT WORKS")
    logging.info("NO KIDDING")
    logging.warning("THIS IS THE LAST WARNING, GOING DOWN.. NOW!")
    logging.error("HOAH.")
