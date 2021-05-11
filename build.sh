#! /bin/bash

git clone https://github.com/arter97/arm64-gcc.git --quiet -b master --depth=1 /home/baalajimaestro/gcc
git clone https://github.com/arter97/arm32-gcc.git --quiet -b master --depth=1 /home/baalajimaestro/gcc32
git clone https://github.com/baalajimaestro/AnyKernel3.git --quiet --depth=1 /home/baalajimaestro/anykernel3
export CROSS_COMPILE="/home/baalajimaestro/gcc/bin/aarch64-elf-"
export CROSS_COMPILE_ARM32="/home/baalajimaestro/gcc32/bin/arm-eabi-"
export ARCH=arm64
export SUBARCH=arm64
make -j$(nproc) sm8150_defconfig O=out
make -j$(nproc) O=out