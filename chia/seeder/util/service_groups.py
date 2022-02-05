from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "bpx_seeder_crawler bpx_seeder_server".split(),
    "crawler": "bpx_seeder_crawler".split(),
    "server": "bpx_seeder_server".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service
