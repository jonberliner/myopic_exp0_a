from distutils.core import setup
from distutils.extension import Extension
import numpy
from Cython.Distutils import build_ext
setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
        Extension("jbgp", ["jbgp.pyx"]),
        Extension("jbgp_fit", ["jbgp_fit.pyx"])
    ],
    include_dirs=[numpy.get_include()]
)
