#!/usr/bin/env python3
#cython: language_level=3
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext


ext = Extension("cython_blur", sources=["cython_blur.pyx"])
setup(ext_modules=[ext],
      cmdclass={'build_ext': build_ext})
