#!/usr/bin/env bash

# File: build.sh
# Author: Henry R. Winterbottom
# Date: 25 January 2024

# Description: This script builds the Python extension modules.

# Usage: ./build.sh

# ----

# Execute the application accordingly.
set +x -e
# shellcheck disable=SC2034
start=$($(command -v date) -u)
echo "Beginning Python extension module building."
export OBSufs="${PWD}"

# AOML package.
cd "${OBSufs}/sorc/obsio/sonde/"
$(command -v f2py) -c -m aoml aoml.f90
# shellcheck disable=SC2034
status=$?

# Sondelib package.
cd "${OBSufs}/sorc/obsio/sonde/"
$(command -v f2py) -c -m sondelib sondelib.f thermo_subs.f
# shellcheck disable=SC2034
status=$?

stop=$($(command -v date) -u)
echo "${stop}: Completed application ${OBSufs}."
