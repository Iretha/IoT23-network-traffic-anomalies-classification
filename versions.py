import platform
import socket
import uuid
import re
import logging
import wmi

import sklearn
import numpy
import pandas
import matplotlib
import seaborn
import psutil
import scikitplot


def print_versions():
    print('scikit-learn v{},'.format(sklearn.__version__))
    print('NumPy v{},'.format(numpy.__version__))
    print('Pandas v{},'.format(pandas.__version__))
    print('Matplotlib v{},'.format(matplotlib.__version__))
    print('Seaborn v{},'.format(seaborn.__version__))
    print('Psutil v{},'.format(psutil.__version__))
    print('Scikitplot, v{}'.format(scikitplot.__version__))


def print_system_info():
    info = {'platform': platform.system(),
            'platform-release': platform.release(),
            'platform-version': platform.version(),
            'architecture': platform.machine(),
            'hostname': socket.gethostname(),
            'ip-address': socket.gethostbyname(socket.gethostname()),
            'mac-address': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            'processor': platform.processor(),
            'ram': str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"}

    computer = wmi.WMI()
    os_info = computer.Win32_OperatingSystem()[0]
    os_name = platform.system() + ' ' + platform.release()
    os_version = ' '.join([os_info.Version, os_info.BuildNumber])
    proc_info = computer.Win32_Processor()[0]
    gpu_info = computer.Win32_VideoController()[0]
    system_ram = float(os_info.TotalVisibleMemorySize) / 1048576  # KB to GB

    print('OS Name: {0}'.format(os_name))
    print('OS Version: {0}'.format(os_version))
    print('Architecture: {0}'.format(platform.machine()))
    print('CPU: {0}'.format(proc_info.Name))
    print('RAM: {0} GB'.format(round(system_ram)))
    print('Graphics Card: {0}'.format(gpu_info.Name))

    print(info)


print_versions()
print_system_info()


p = psutil.Process()
info = p.memory_percent()
print(info)

print('The end.')
quit()
