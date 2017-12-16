import tempfile
import sys
from setproctitle import setproctitle
from daemonize import Daemonize

from vHunter.utils.config import Config
from vHunter.utils.distro import detect_distro
from vHunter.utils.distro import check_python
from vHunter.utils import prepare_asyncio
from vHunter.utils import parse_args
from vHunter.utils import setup_logging
from vHunter.workers import ScenarioWorker
from vHunter.workers import NotifyAggregatorWorker


PIDFILE = tempfile.gettempdir() + "/vhunter.pid"
PROCNAME = "vhunter %s" % (" ".join(sys.argv[1:]))


check_python()
config = Config()
args = parse_args()
config.set_args(args)
fd_list = setup_logging(log_file=args.log_file, log_level=args.log_level)


def run_workers():
    ScenarioWorker()
    NotifyAggregatorWorker()


def main():
    setproctitle(PROCNAME)
    detect_distro()
    main_loop = prepare_asyncio()
    run_workers()
    main_loop.run_forever()
    main_loop.close()


if __name__ == "__main__":
    daemon = Daemonize(
        app="test_app",
        pid=PIDFILE,
        action=main,
        keep_fds=fd_list,
        foreground=args.foreground
    )
    daemon.start()
