
from utils.config import Config
from utils.distro import detect_distro
from utils.distro import check_python
from utils import prepare_asyncio
from utils import parse_args
from utils import setup_logging
from workers import ScenarioWorker


def run_workers():
    ScenarioWorker()


if __name__ == "__main__":
    config = Config()
    args = parse_args()
    config.set_args(args)
    setup_logging(log_file=args.log_file, log_level=args.log_level)
    check_python()
    detect_distro()
    main_loop = prepare_asyncio()
    run_workers()
    main_loop.run_forever()
    main_loop.close()
