from pbr.core import pbr


def packman(dist, attr, value):
    pbr(dist, attr, value)


# additional_files = set()
#
#
# def list_files(dir_name):
#     return additional_files

# setuptools.file_finders =
#     wrap = wrap.core:list_files