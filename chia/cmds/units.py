from typing import Dict

# The rest of the codebase uses mojos everywhere.
# Only use these units for user facing interfaces.
units: Dict[str, int] = {
    "chia": 10 ** 12,  # 1 BPX is 1,000,000,000,000 mojo (1 trillion)
    "mojo": 1,
    "cat": 10 ** 6,  # 1 token is 1,000,000 mojos
}
