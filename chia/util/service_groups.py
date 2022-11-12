from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "floteo_harvester floteo_timelord_launcher floteo_timelord floteo_farmer floteo_full_node floteo_wallet".split(),
    "node": "floteo_full_node".split(),
    "harvester": "floteo_harvester".split(),
    "farmer": "floteo_harvester floteo_farmer floteo_full_node floteo_wallet".split(),
    "farmer-no-wallet": "floteo_harvester floteo_farmer floteo_full_node".split(),
    "farmer-only": "floteo_farmer".split(),
    "timelord": "floteo_timelord_launcher floteo_timelord floteo_full_node".split(),
    "timelord-only": "floteo_timelord".split(),
    "timelord-launcher-only": "floteo_timelord_launcher".split(),
    "wallet": "floteo_wallet".split(),
    "introducer": "floteo_introducer".split(),
    "simulator": "floteo_full_node_simulator".split(),
    "crawler": "floteo_crawler".split(),
    "seeder": "floteo_crawler floteo_seeder".split(),
    "seeder-only": "floteo_seeder".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
