# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os
import shutil


class Arpackpp(Package):
    """ ArpackPP is a C++ interface to the Arpack library """

    homepage = "https://github.com/m-reuter/arpackpp"
    url = "https://github.com/m-reuter/arpackpp/archive/2.3.0.tar.gz"

    version('2.3.0', sha256='288fb4cd2dd08e02ed29db579bc1278023a06415dd2f63b1fdc323c7993fcb1a')
    version('2.2.0', sha256='03eca722b23b23aa8e99bde0f56458ddb8c99c7136cab17d631bf8edbc26c545')
    version('2.1.1', sha256='1e68a79744add6e7e9a61b84084ace5ead2d2ccf288b5dedcaf152e63b16cd60')
    version('2.1.0', sha256='5da2f40ac3fbc2d0febfd1c7901d2a92c3edf6840727d0b69550140eb958664e')
    version('2.0.0', sha256='816ea2440b3a1776613221b6232829d879324c900877609d99dc0c9494d9e36d')
    version('1.2.0', sha256='0264dbba5423215f21405db1d90a0a51d7acc8512da372d139055191b208cfeb')

    depends_on("arpack-ng")

    def install(self, spec, prefix):
        os.makedirs(os.path.join(prefix, "include", "arpackpp"))
        for inc in os.listdir("include"):
            shutil.copy(os.path.join("include", inc), os.path.join(prefix, "include", "arpackpp"))
