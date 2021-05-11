#! /bin/bash

git clone https://github.com/arter97/arm64-gcc.git --quiet -b master --depth=1 /home/baalajimaestro/gcc
git clone https://github.com/arter97/arm32-gcc.git --quiet -b master --depth=1 /home/baalajimaestro/gcc32
git clone https://github.com/baalajimaestro/AnyKernel3.git --quiet --depth=1 /home/baalajimaestro/anykernel3
export PATH="/home/baalajimaestro/gcc/bin:/home/baalajimaestro/gcc32/bin:$PATH"
make -j$(nproc) O=out ARCH=arm64 SUBARCH=arm64 CROSS_COMPILE="aarch64-elf-" CROSS_COMPILE_ARM32="arm-eabi-" sm8150_defconfig 
make -j$(nproc) O=out ARCH=arm64 SUBARCH=arm64 CROSS_COMPILE="aarch64-elf-" CROSS_COMPILE_ARM32="arm-eabi-"