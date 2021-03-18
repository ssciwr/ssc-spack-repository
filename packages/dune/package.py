# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install dune
#
# You can edit this file again by typing:
#
#     spack edit dune
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os
from pathlib import Path
from spack import *


class Dune(CMakePackage):
    """
    DUNE, the Distributed and Unified Numerics Environment is a modular toolbox for solving partial differential equations (PDEs) with grid-based methods.
    """
    homepage = "https://www.dune-project.org"
    git = "https://gitlab.dune-project.org/core/dune-common.git"

    # This defines a mapping of available versions of the dune Spack package
    # and the branch name in the Dune repositories this refers to. This is a
    # list instead of a dictionary to ensure iteration order (first entry is
    # the default version) in Python3.
    dune_versions_to_branch = [
      ("2.7", "releases/2.7"),
      ("2.6", "releases/2.6"),
      ("master" , "master"),
    ]

    # This defines the mapping of the variant names for Dune modules and the
    # resource names that we assign later on.
    dune_variants_to_resources = {
        'alugrid' : 'dune-alugrid',
        'codegen' : 'dune-codegen',
        'fem' : 'dune-fem',
        'foamgrid' : 'dune-foamgrid',
        'functions': 'dune-functions',
        'gridglue' : 'dune-grid-glue',
        'multidomaingrid' : 'dune-multidomaingrid',
        'pdelab' : 'dune-pdelab',
        'polygongrid' : 'dune-polygongrid',
        'spgrid' : 'dune-spgrid',
        'testtools' : 'dune-testtools',
        'typetree' : 'dune-typetree',
        'uggrid' : 'dune-uggrid',
    }

    # Define the inverse mapping
    dune_resources_to_variants = {v: k for k, v in dune_variants_to_resources.items()}

    # Dependencies between modules - not necessarily the full set
    # as the closure of module dependencies is built later on.
    # dune-common does not need to be named.
    dune_module_dependencies = {
        'dune-alugrid': ['dune-grid'],
        'dune-codegen': ['dune-pdelab', 'dune-testtools', 'dune-alugrid'],
        'dune-fem': ['dune-grid'],
        'dune-fempy': ['dune-fem'],
        'dune-foamgrid': ['dune-grid'],
        'dune-functions': ["dune-grid", "dune-typetree", "dune-localfunctions", "dune-istl"],
        'dune-grid': ['dune-geometry'],
        'dune-grid-glue': ['dune-grid'],
        'dune-localfunctions': ['dune-geometry'],
        'dune-multidomaingrid': ['dune-grid', 'dune-typetree'],
        'dune-pdelab': ['dune-istl', 'dune-functions'],
        'dune-polygongrid': ['dune-grid'],
    }

    # Build the closure of above module dependency list.
    # We need to use cryptic variable names here because
    # Spack behaves in weird ways if we accidentally use
    # names (like 'module') that are used in seemingly
    # unrelated places.
    for _mod in dune_module_dependencies:
        _closure = set(dune_module_dependencies[_mod])
        _old_closure = set()
        while (len(_closure) > len(_old_closure)):
            _old_closure = _closure.copy()

            for _res in _old_closure:
                for _m in dune_module_dependencies.get(_res, []):
                    _closure.add(_m)

        dune_module_dependencies[_mod] = list(_closure)

    # Variants for the general build process
    variant('shared', default=True, description='Enables the build of shared libraries.')

    # Some variants for customization of Dune
    variant('doc', default=False, description='Build and install documentation')
    variant('python', default=False, description='Build with Python bindings')

    # Variants for upstream dependencies. Note that we are exposing only very
    # costly upstream dependencies as variants. All other upstream dependencies
    # are installed unconditionally. This happens in an attempt to limit the total
    # number of variants of the dune package to a readable amount. An exception
    # to this rule is ParMETIS, which has a variant because of it's semi-free license.
    variant('parmetis', default=False, description='Build with ParMETIS support')
    variant('petsc', default=False, description='Build with PetSc support')
    variant('tbb', default=False, description='Build with Intel TBB support')

    # Define one variant for each non-core Dune module that we have.
    for var, res in dune_variants_to_resources.items():
        variant(var, default=False, description='Build with the %s module' % res)

    # Define conflicts between Dune module variants. These conflicts are of the following type:
    # conflicts('dune~functions', when='+pdelab') -> dune-pdelab cannot be built without dune-functions
    for var, res in dune_variants_to_resources.items():
        for dep in dune_module_dependencies.get(res, []):
            if dep in dune_resources_to_variants:
                conflicts('dune~%s' % dune_resources_to_variants[dep], when='+%s' % var)

    # Iterate over all available Dune versions and define resources for all Dune modules
    # If a Dune module behaves differently for different versions (e.g. dune-python got
    # merged into dune-common post-2.7), define the resource outside of this loop.
    for _vers, _branch in dune_versions_to_branch:
        version(_vers, branch=_branch)

        resource(
            name='dune-geometry',
            git='https://gitlab.dune-project.org/core/dune-geometry.git',
            branch=_branch,
            when='@%s' % _vers,
        )

        resource(
            name='dune-grid',
            git='https://gitlab.dune-project.org/core/dune-grid.git',
            branch=_branch,
            when='@%s' % _vers,
        )

        resource(
            name='dune-istl',
            git='https://gitlab.dune-project.org/core/dune-istl.git',
            branch=_branch,
            when='@%s' % _vers,
        )

        resource(
            name='dune-localfunctions',
            git='https://gitlab.dune-project.org/core/dune-localfunctions.git',
            branch=_branch,
            when='@%s' % _vers,
        )

        resource(
            name='dune-functions',
            git='https://gitlab.dune-project.org/staging/dune-functions.git',
            branch=_branch,
            when='@%s+functions' % _vers,
        )

        resource(
            name='dune-typetree',
            git='https://gitlab.dune-project.org/staging/dune-typetree.git',
            branch=_branch,
            when='@%s+typetree' % _vers,
        )

        resource(
            name='dune-alugrid',
            git='https://gitlab.dune-project.org/extensions/dune-alugrid.git',
            branch=_branch,
            when='@%s+alugrid' % _vers,
        )

        resource(
            name='dune-uggrid',
            git='https://gitlab.dune-project.org/staging/dune-uggrid.git',
            branch=_branch,
            when='@%s+uggrid' % _vers,
        )

        resource(
            name='dune-spgrid',
            git='https://gitlab.dune-project.org/extensions/dune-spgrid.git',
            branch=_branch,
            when='@%s+spgrid' % _vers,
        )

        resource(
            name='dune-testtools',
            git='https://gitlab.dune-project.org/quality/dune-testtools.git',
            branch=_branch,
            when='@%s+testtools' % _vers,
        )

        resource(
            name='dune-polygongrid',
            git='https://gitlab.dune-project.org/extensions/dune-polygongrid.git',
            branch=_branch,
            when='@%s+polygongrid' % _vers,
        )

        resource(
            name='dune-foamgrid',
            git='https://gitlab.dune-project.org/extensions/dune-foamgrid.git',
            branch=_branch,
            when='@%s+foamgrid' % _vers,
        )

        resource(
            name='dune-multidomaingrid',
            git='https://gitlab.dune-project.org/extensions/dune-multidomaingrid.git',
            branch=_branch,
            when='@%s+multidomaingrid' % _vers,
        )

        resource(
            name='dune-fem',
            git='https://gitlab.dune-project.org/dune-fem/dune-fem.git',
            branch=_branch,
            when='@%s+fem' % _vers,
        )

        resource(
            name='dune-fempy',
            git='https://gitlab.dune-project.org/dune-fem/dune-fempy.git',
            branch=_branch,
            when='@%s+fem+python' % _vers,
        )

        resource(
            name='dune-pdelab',
            git='https://gitlab.dune-project.org/pdelab/dune-pdelab.git',
            branch=_branch,
            when='@%s+pdelab' % _vers,
        )

        # The dune-grid-glue package does not yet have a 2.7-compatible release
        resource(
            name='dune-grid-glue',
            git='https://gitlab.dune-project.org/extensions/dune-grid-glue.git',
            branch=_branch,
            when='@%s+gridglue' % _vers,
        )

    # The dune-python package migrated to dune-common after the 2.7 release
    resource(
        name='dune-python',
        git='https://gitlab.dune-project.org/staging/dune-python.git',
        branch='releases/2.7',
        when='@2.7+python',
    )

    resource(
        name='dune-python',
        git='https://gitlab.dune-project.org/staging/dune-python.git',
        branch='releases/2.6',
        when='@2.6+python',
    )

    # The dune-codegen package does not have a 2.6-compatible release
    resource(
        name='dune-codegen',
        git='https://gitlab.dune-project.org/extensions/dune-codegen.git',
        branch='master',
        when='@master+codegen',
        submodules=True,
    )

    resource(
        name='dune-codegen',
        git='https://gitlab.dune-project.org/extensions/dune-codegen.git',
        branch='releases/2.7',
        when='@2.7+codegen',
        submodules=True,
    )

    conflicts('dune@2.6', when='+codegen')

    # Make sure that Python components integrate well into Spack
    extends('python')
    python_components = [ 'dune' ]

    # Specify upstream dependencies (often depending on variants)
    depends_on('amgx', when='+fem+petsc')
    depends_on('arpackpp')
    depends_on('benchmark', when='+codegen')
    depends_on('blas')
    depends_on('cmake@3.1:', type='build')
    depends_on('eigen', when='+fem')
    depends_on('eigen', when='+pdelab')
    depends_on('papi', when='+fem')
    depends_on('doxygen', type='build', when='+doc')
    depends_on('gawk')
    depends_on('gmp')
    depends_on('intel-tbb', when='+tbb')
    depends_on('lapack')
#    depends_on('likwid', when='+codegen') likwid cannot be built in spack v0.14.2 due to the lua dependency being broken
    depends_on('mpi')
    depends_on('parmetis', when='+parmetis')
    depends_on('petsc', when='+petsc')
    depends_on('pkg-config', type='build')
    depends_on('python@3.0:', type=('build', 'run'))
    depends_on('py-setuptools', type='build', when='+python')
    depends_on('py-numpy', type=('build', 'run'), when='+python')
    depends_on('py-pip', type=('build', 'run'))
    depends_on('py-sphinx', type=('build', 'run'), when='+doc')
    depends_on('py-wheel', type='build')
    depends_on('scotch+mpi')
    depends_on('suite-sparse')
    depends_on('superlu')
    depends_on('vc')
    depends_on('zlib', when='+alugrid')
    depends_on('zoltan', when='+alugrid')

    # Apply patches
    patch('virtualenv_from_envvariable.patch', when='+testtools')
    patch('pdelab_2.6_update_cmake.patch', when='@2.6+pdelab', working_dir= 'dune-pdelab')

    def setup_build_environment(self, env):
        # We reset the DUNE_CONTROL_PATH here because any entries in this
        # path that contain Dune modules will break the Spack build process.
        env.set('DUNE_CONTROL_PATH', '')

    def setup_run_environment(self, env):
        # Some scripts search the DUNE_CONTROL_PATH for Dune modules (e.g. duneproject).
        # We need to set it correctly in order to allow multiple simultaneous
        # installations of the dune package.
        env.set('DUNE_CONTROL_PATH', self.prefix)

        # Additionally, we need to set the workspace for the Python bindings to something
        # that is unique to this build of the dune module (it defaults to ~/.cache)
        if '+python' in self.spec:
            env.set('DUNE_PY_DIR', join_path(Path.home(), '.cache', 'dune-py', self.spec.dag_hash()))

        # For those modules that typically work with the Dune Virtualenv,
        # we export the location of the virtualenv as an environment variable.
        if '+testtools' in self.spec:
            env.set('DUNE_PYTHON_VIRTUALENV_PATH', join_path(Path.home(), '.cache', 'dune-python-env', self.spec.dag_hash()))

    def cmake_args(self):
        """Populate cmake arguments."""
        spec = self.spec
        def variant_bool(feature, on='ON', off='OFF'):
            """Ternary for spec variant to ON/OFF string"""
            if feature in spec:
                return on
            return off 

        def nvariant_bool(feature):
            """Negated ternary for spec variant to OFF/ON string"""
            return variant_bool(feature, on='OFF', off='ON')

        cmake_args = [ 
            '-DCMAKE_BUILD_TYPE:STRING=%s' % self.spec.variants['build_type'].value,
            '-DBUILD_SHARED_LIBS:BOOL=%s' % variant_bool('+shared'),
            '-DDUNE_GRID_GRIDTYPE_SELECTOR:BOOL=ON',
            '-DCMAKE_DISABLE_FIND_PACKAGE_Doxygen:BOOL=%s' % nvariant_bool('+doc'),
            '-DCMAKE_DISABLE_FIND_PACKAGE_LATEX:BOOL=%s' % nvariant_bool('+doc'),
            '-DCMAKE_DISABLE_FIND_PACKAGE_ParMETIS:BOOL=%s' % nvariant_bool('+parmetis'),
#            '-DCMAKE_DISABLE_FIND_PACKAGE_TBB=%s' % nvariant_bool('+tbb'), Disabled until upstream fix of dune-common#205.
        ]

        if '+testtools' in spec:
            cmake_args.append('-DDUNE_PYTHON_VIRTUALENV_SETUP:BOOL=ON')
            cmake_args.append('-DDUNE_PYTHON_ALLOW_GET_PIP:BOOL=ON')
            cmake_args.append('-DDUNE_PYTHON_VIRTUALENV_PATH:STRING="%s"' % join_path(Path.home(), '.cache', 'dune-python-env', self.spec.dag_hash()))
            cmake_args.append('-DDUNE_PYTHON_INSTALL_LOCATION:STRING="system"')

        if '+python' in spec:
            if '@2.7' not in spec:
                cmake_args.append('-DDUNE_ENABLE_PYTHONBINDINGS:BOOL=TRUE')
            cmake_args.append('-DDUNE_GRID_EXPERIMENTAL_GRID_EXTENSIONS:BOOL=TRUE')
            cmake_args.append('-DDUNE_PYTHON_INSTALL_LOCATION:STRING="system"')

        return cmake_args

    def cmake(self, spec, prefix):
        # dune-codegen delivers its own set of patches for its submodules
        # that we can apply with a script delivered by dune-codegen.
        if '+codegen' in self.spec:
            with working_dir(join_path(self.root_cmakelists_dir, 'dune-codegen')):
                Executable('patches/apply_patches.sh')()

        # Write an opts file for later use
        with open(join_path(self.stage.source_path, "..", "dune.opts"), "w") as optFile:
            optFile.write('CMAKE_FLAGS="')
            for flag in self.cmake_args():
                optFile.write(flag.replace("\"", "'")+" ")
            optFile.write('-DCMAKE_INSTALL_PREFIX=%s' % prefix)
            optFile.write('"')

        installer = Executable('bin/dunecontrol')
        options_file = join_path(self.stage.source_path, "..", "dune.opts")

        # The 'cmake' command of dunecontrol was added in 2.7
        commandname = 'cmake'
        if '@2.6' in self.spec:
            commandname = 'configure'

        installer('--builddir=%s'%self.build_directory ,  '--opts=%s' % options_file, commandname)

    def install(self, spec, prefix):
        installer = Executable('bin/dunecontrol')
        options_file = join_path(self.stage.source_path, "..", "dune.opts")
        installer('--builddir=%s'%self.build_directory ,  '--opts=%s' % options_file, 'make', 'install')

    def build(self, spec, prefix):
        installer = Executable('bin/dunecontrol')
        options_file = join_path(self.stage.source_path, "..", "dune.opts")
        installer('--builddir=%s'%self.build_directory ,  '--opts=%s' % options_file, 'make')

