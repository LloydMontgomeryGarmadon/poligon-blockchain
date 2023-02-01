from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "poligon_harvester poligon_timelord_launcher poligon_timelord poligon_farmer poligon_full_node poligon_wallet".split(),
    "node": "poligon_full_node".split(),
    "harvester": "poligon_harvester".split(),
    "farmer": "poligon_harvester poligon_farmer poligon_full_node poligon_wallet".split(),
    "farmer-no-wallet": "poligon_harvester poligon_farmer poligon_full_node".split(),
    "farmer-only": "poligon_farmer".split(),
    "timelord": "poligon_timelord_launcher poligon_timelord poligon_full_node".split(),
    "timelord-only": "poligon_timelord".split(),
    "timelord-launcher-only": "poligon_timelord_launcher".split(),
    "wallet": "poligon_wallet".split(),
    "introducer": "poligon_introducer".split(),
    "simulator": "poligon_full_node_simulator".split(),
    "crawler": "poligon_crawler".split(),
    "seeder": "poligon_crawler poligon_seeder".split(),
    "seeder-only": "poligon_seeder".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
