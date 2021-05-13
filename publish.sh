#! /bin/bash

cp /home/baalajimaestro/kernel_oneplus_sm8150/out/arch/arm64/boot/Image /home/baalajimaestro/AnyKernel3
find /home/baalajimaestro/kernel_oneplus_sm8150/out/arch/arm64/boot/dts -name '*.dtb' -exec cat {} + > /home/baalajimaestro/AnyKernel3/dtb
cd /home/baalajimaestro/AnyKernel3
export ZIPNAME="Retarded-Kernel-CI-GCC-$(date +%Y%m%d).zip"
zip -r9 "${ZIPNAME}" -- *
ZIPURL=$(curl -sL bashupload.com -T ${ZIPNAME} | grep wget)
echo "DOWNLOAD: $ZIPURL"
curl -s -X POST https://api.telegram.org/bot"${TELEGRAM_TOKEN}"/sendMessage -d text="${ZIPURL}" -d chat_id="518221376"
echo "If you attempt to download the bashupload link, please dont ask for support"
echo "These are untested builds which are built automatically on push!"
echo "Expect NO WARRANTY of any sort if you land on data crashes/bootloops"
