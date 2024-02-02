# File: Docker/ubuntu20.04.ufs_obs.dockerfile
# Author: Henry R. Winterbottom
# Date: 29 October 2023

# -------------------------
# * * * W A R N I N G * * *
# -------------------------

# It is STRONGLY urged that users do not make modifications below this
# point; changes below are not supported.

# -------------------------
# * * * W A R N I N G * * *
# -------------------------

FROM ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_pyutils:latest
ENV UFS_OBS_GIT_URL="https://www.github.com/HenryWinterbottom-NOAA/ufs_obs.git"
ENV UFS_OBS_GIT_BRANCH="develop"
ENV OBS_ROOT="/opt/ufs_obs"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV PATH="/opt/miniconda/bin:${PATH}"

RUN $(command -v apt-get) update -y && \
    $(command -v apt-get) install -y --no-install-recommends \
    g++ \
    gcc \
    make \
    gfortran \
    cmake && \
    $(command -v rm) -rf /var/lib/apt/lists/* && \
    export CC=$(command -v gcc) && \
    export FC=$(command -v gfortran)

RUN $(command -v git) clone --recursive "${UFS_OBS_GIT_URL}" --branch "${UFS_OBS_GIT_BRANCH}" "${OBS_ROOT}" && \
    $(command -v pip) install -r "${OBS_ROOT}/requirements.txt" && \
    cd "${OBS_ROOT}" && \
    ./build.sh && \
    echo "export OBS_ROOT=${OBS_ROOT}" >> /root/.bashrc

ENV PYTHONPATH="${OBS_ROOT}/sorc:${PYTHONPATH}"