# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Funcep(CMakePackage):
    """Lecture material for the lecture 'FUNdamentals of Computational Environmental Physics
    
    The lecture is given annually at Heidelberg University by Peter Bastian and Kurt Roth.
    The software stack is based on the Distributed and Unified Numerics Environment (DUNE).
    """

    homepage = "https://www.dune-project.org"
    git      = "https://parcomp-git.iwr.uni-heidelberg.de/Teaching/dune-funcep.git"

    version('master', branch='master')

    patch('remove-custom-findhdf5.patch')

    depends_on('dune+typetree+uggrid+alugrid+functions+pdelab@2.7')
    depends_on('dune-randomfield@master')
    depends_on('hdf5@1.8.18:+mpi')
    depends_on('fftw@3.3.4:+mpi precision=double')

    def cmake_args(self):
        flags = CMakePackage.cmake_args(self)
        flags += ['-DCMAKE_CXX_FLAGS="-DH5_USE_16_API"']
        return flags
