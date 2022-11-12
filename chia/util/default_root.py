import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("FLOTEO_ROOT", "~/.floteo/mainnet"))).resolve()

DEFAULT_KEYS_ROOT_PATH = Path(os.path.expanduser(os.getenv("FLOTEO_KEYS_ROOT", "~/.floteo_keys"))).resolve()
