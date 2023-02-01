import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("POLIGON_ROOT", "~/.poligon/mainnet"))).resolve()

DEFAULT_KEYS_ROOT_PATH = Path(os.path.expanduser(os.getenv("POLIGON_KEYS_ROOT", "~/.poligon_keys"))).resolve()
