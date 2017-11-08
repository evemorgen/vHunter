import logging

from utils.distro import detect_distro
from utils.distro import check_python
from utils import prepare_asyncio
from utils import parse_args
from utils import setup_logging
from utils import run_cmd


async def main():
    output = await run_cmd("brew list --versions")
    logging.warning(output)

if __name__ == "__main__":
    args = parse_args()
    setup_logging(log_file=args.log_file, log_level=args.log_level)
    check_python()
    detect_distro()
    main_loop = prepare_asyncio()
    main_loop.run_until_complete(main())
    main_loop.close()
