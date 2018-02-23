#!/ust/local/bin python3

from distutils.core import setup, Extension

module1 = Extension('dcc', sources=['gertbot_pi_uart.c', 'command.c'])

setup (name = 'DCC',
        version = '1.0',
        description = 'DCC control package',
        ext_modules = [module1])
