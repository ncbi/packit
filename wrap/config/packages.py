from pbr import find_package


def packages_config(config, facility_section_name):
    packages = config.get(facility_section_name, {}).get('packages', None)
    if packages is None:
        packages = find_package.smart_find_packages(config['metadata']['name'])
    config.setdefault('files', {})['packages'] = packages