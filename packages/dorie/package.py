# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dorie(CMakePackage):
    """DUNE-Operated Richards equation solving Environment"""

    homepage = "http://ts.iup.uni-heidelberg.de/research/terrestrial-systems/dorie/"
    git      = "https://ts-gitlab.iup.uni-heidelberg.de/dorie/dorie"

    # List of GitHub accounts to notify when the package is updated.
    maintainers = ['SoilRos']

    version('master', branch='master', submodules=True)

    depends_on('muparser')
    depends_on('yaml-cpp')
    depends_on('fftw@3.3.4:+mpi precision=double')
    depends_on('dune@2.6+uggrid+typetree+functions+pdelab')
    depends_on('dune-randomfield@2.6')
    depends_on('spdlog@1.5:')

    extends('python')
    python_components = [ 'dorie' ]

    # We remove documentation building as it's Python setup clashes with our approach in Spack
    patch('disable-documentation.patch')

    # DORiE needs a lot RAM for each build job. With this option it will take longer but will save headaches to many people.
    parallel = False

    def cmake_args(self):
        """Populate cmake arguments."""
        cmake_args = []

        # We install the Python CLI of dorie into Spack's Python environment
        cmake_args.append('-DDUNE_PYTHON_INSTALL_LOCATION:STRING=system')

        return cmake_args
