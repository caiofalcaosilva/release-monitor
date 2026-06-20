import os

from dotenv import load_dotenv

_env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(_env_file)

from app.setup_wizard import run_setup_wizard, start_status_server  # noqa: E402

run_setup_wizard()
start_status_server()

from app.main import main  # noqa: E402

main()
