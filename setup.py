from distutils.core import setup
from distutils.extension import Extension


setup(
    name='ImageBlur',
    version='1.0',
    packages=['imageblurring'],
    package_data={'imageblurring': ['cython_blur.c',
                                    "cython_blur.cp37-win_amd64.pyd",
                                    "cython_blur.cpython-37m-x86_64-linux-gnu.so",
                                    "cython_blur.pyx"]}
)
