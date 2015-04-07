from packit.config import packit_facilities


def setup_hook(config, facilities=packit_facilities):
    active_facilities = facilities.get_enabled_facilities(config)

    for facility_name, config_processor in active_facilities.items():
        config_processor(config, facility_name)
