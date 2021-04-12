# Spack repository of the Scientific Software Center

[Spack](https://github.com/spack/spack.git) is a package manager that
allows to build consistent scientific software stacks from source. Spack is the state of the
art for system administrators in HPC centers but is also increasingly popular
in end user scenarios. One particular strength of Spack is the handling of
build variants of packages and their dependencies.

This repository defines some package recipes that are maintained
by the Scientific Software Center of Heidelberg University.

## Setting up Spack with this repository

The following instructions are the same regardless of which package
you are interested to build:

```
git clone -b v0.16.1 https://github.com/spack/spack.git
git clone https://github.com/ssciwr/ssc-spack-repository.git
source spack/share/spack/setup-env.sh
spack repo add ssc-spack-repository
```

Each time you are using `spack`, you will need to add it to your
current shell environment by running:

```
source <path-to-spack>/share/spack/setup-env.sh
```

If you are using Spack on a regular basis, you might want to consider
to permanently add `spack` to your environment by appending above line
to your `~/.bashrc` file.

## Instructions for individual packages

### FunCEP

This is the lecture material for the lecture *Fundamentals of Computational Environmental Physics*
given annually by Prof. Peter Bastian and Prof. Kurt Roth at Heidelberg University. Given
you set up Spack like described above, these commands will build the lecture material and
all of its dependencies:

```
git clone https://parcomp-git.iwr.uni-heidelberg.de/Teaching/dune-funcep.git
cd dune-funcep
spack dev-build --jobs 1 funcep@master
```

If your computer has a enough RAM, you can increase the number of concurrent build jobs.
After installation, a CMake build directory `spack-build-<hash>` will contain the built
course material.

## Troubleshooting

If you experience problems with this repository, try the following:

* Clear all build caches `spack clean -a`
* Remove `~/.spack` (note you need to re-add the repository afterwards: `spack repo add <path-to-ssc-spack-repository>`)
* Try rebuilding the package

If your problem persists, please open an issue on this repository.

## Packaging your software project

If you are a member of Heidelberg University and you think it may be beneficial
to package your software for Spack as well, please [contact the SSC](mailto:ssc@iwr.uni-heidelberg.de).
