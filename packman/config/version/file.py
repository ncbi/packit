def file_version_generator(filename):
    return open(filename, 'rb').readline().decode('utf-8').strip()
