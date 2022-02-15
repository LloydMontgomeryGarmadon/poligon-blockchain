from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "bpx_harvester bpx_timelord_launcher bpx_timelord bpx_farmer bpx_full_node bpx_wallet".split(),
    "node": "bpx_full_node".split(),
    "harvester": "bpx_harvester".split(),
    "farmer": "bpx_harvester bpx_farmer bpx_full_node bpx_wallet".split(),
    "farmer-no-wallet": "bpx_harvester bpx_farmer bpx_full_node".split(),
    "farmer-only": "bpx_farmer".split(),
    "timelord": "bpx_timelord_launcher bpx_timelord bpx_full_node".split(),
    "timelord-only": "bpx_timelord".split(),
    "timelord-launcher-only": "bpx_timelord_launcher".split(),
    "wallet": "bpx_wallet".split(),
    "introducer": "bpx_introducer".split(),
    "simulator": "bpx_full_node_simulator".split(),
    "crawler": "bpx_crawler".split(),
    "seeder": "bpx_crawler bpx_seeder".split(),
    "seeder-only": "bpx_seeder".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
