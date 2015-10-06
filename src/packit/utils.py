import email


def _get_version_from_meta(package_name, pkg_metadata_filenames=('PKG-INFO', 'METADATA')):
    pkg_metadata = {}
    for filename in pkg_metadata_filenames:
        try:
            with open(filename, 'r') as pkg_metadata_file:
                pkg_metadata = email.message_from_file(pkg_metadata_file)
        except (IOError, OSError, email.errors.MessageError):
            continue

    # Check to make sure we're in our own dir
    if pkg_metadata.get('Name', None) != package_name:
        return None
    return pkg_metadata.get('Version', None)

try:
    from pbr.packaging import _get_version_from_pkg_metadata as get_version_from_meta
except ImportError:
    get_version_from_meta = _get_version_from_meta


def parse_boolean(val, true_values=('1', 'yes', 'y', 'true', 't')):
    return val.lower() in true_values
