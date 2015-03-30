from setuptools import find_packages


def packages_config(config, facility_section_name):
    packages = config.setdefault('files', {}).get('packages').strip()

    if packages:
        return

    exclude = config.get(facility_section_name, {}).get('exclude', '\n'.join(['tests', 'docs']))
    exclude_list = exclude.strip().split('\n')

    found_packages = find_packages(exclude=exclude_list)
    config['files']['packages'] = "\n".join(set(found_packages))