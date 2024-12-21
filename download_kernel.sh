#!/bin/bash

set -u

rm -rf linux
VERSION='linux-6.13-rc3'
wget "https://git.kernel.org/torvalds/t/${VERSION}.tar.gz"
tar -xvzf "${VERSION}.tar.gz"
rm "${VERSION}.tar.gz"
mv "${VERSION}" linux

pushd linux
echo Setting up config, might not work depending from your distribution, do by hand if neccessary
cp /boot/config-"$(uname -r)" .config
make defconfig
popd
