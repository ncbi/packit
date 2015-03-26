from packman.config import packman_facilities


def setup_hook(config, facilities=packman_facilities):
    active_facilities = facilities.get_enabled_facilities(config)

    for facility_name, config_processor in sorted(active_facilities.items()):
        config_processor(config, facility_name)
