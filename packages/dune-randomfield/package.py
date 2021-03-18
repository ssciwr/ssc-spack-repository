# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DuneRandomfield(CMakePackage):
    """Generation of Gaussian random fields in arbitrary dimensions, based on circulant embedding"""

    homepage = "https://www.dune-project.org"
    git      = "https://gitlab.dune-project.org/oklein/dune-randomfield.git"

    version('master', branch='master')
    version('2.6', branch='releases/2.6')

    patch('install_files.patch', when="@2.6")

    depends_on('dune@2.7', when="@master")
    depends_on('dune@2.6', when="@2.6")
    depends_on('gsl')
    depends_on('hdf5@1.8.18:+mpi')
    depends_on('fftw@3.3.4:+mpi precision=double')
