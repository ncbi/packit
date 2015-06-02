from subprocess import Popen, PIPE


def shell_version_generator(cmdline, **kwargs):
    p = Popen(cmdline, shell=True, stdout=PIPE)
    line = p.stdout.readlines()[0]
    p.wait()
    return line.strip().decode('utf-8')
