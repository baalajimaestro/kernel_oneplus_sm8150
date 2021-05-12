import asyncio
import logging
import os
import subprocess
from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions, executor

API_TOKEN = os.environ.get("TELEGRAM_TOKEN")

logging.basicConfig(level=logging.ERROR)

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot)

async def send_message(user_id: int, text: str):
    message = await bot.send_message(user_id, text, disable_notification=False, parse_mode=types.ParseMode.MARKDOWN_V2)
    return message

async def edit_message(user_id: int, text: str, message: str, parse_mode=types.ParseMode.MARKDOWN_V2):
    old_text =  message.md_text
    await message.edit_text(old_text + '\n' + text)

async def runner():
    try:
        print("Retarded CI: Warming Up!")
        from git import Repo
        message = "`Retarded CI`\n"
        message += "`Spinning Build for commit:` [" + os.environ.get("SEMAPHORE_GIT_SHA")[:6] + "](https://github.com/baalajimaestro/kernel_oneplus_sm8150/commit/" + os.environ.get("SEMAPHORE_GIT_SHA") +")\n"
        message += "`Downloading Dependenices....`"
        message_track = await send_message(518221376, message)

        print("Retarded CI: Getting GCC Cross Compilers")
        gcc = Repo.clone_from("https://github.com/arter97/arm64-gcc", "/home/baalajimaestro/gcc", branch='master')
        gcc32 = Repo.clone_from("https://github.com/arter97/arm32-gcc", "/home/baalajimaestro/gcc32", branch='master')
        anykernel3 = Repo.clone_from("https://github.com/baalajimaestro/AnyKernel3", "/home/baalajimaestro/AnyKernel3", branch='master')
        print("Retarded CI: Downloaded Necessary Dependencies")
        message = "`Downloaded Dependenices....`"
        await edit_message(518221376, message, message_track)

        defconfig = 'make -j' + str(os.cpu_count()) + ' O=out ARCH=arm64 SUBARCH=arm64 CROSS_COMPILE="aarch64-elf-" CROSS_COMPILE_ARM32="arm-eabi-" sm8150_defconfig'
        make = 'make -j' + str(os.cpu_count()) + ' O=out ARCH=arm64 SUBARCH=arm64 CROSS_COMPILE="aarch64-elf-" CROSS_COMPILE_ARM32="arm-eabi-"'
        
        list_defconfig = defconfig.split(" ")
        list_make = make.split(" ")

        message = "`Started Make....`"
        print("Retarded CI: Strarting Build!")

        process = subprocess.run(list_defconfig)
        if process.returncode != 0:
            exit(127)

        process = subprocess.run(list_make)
        if process.returncode != 0:
            exit(127)

    except:
        print("Our Build Failed, but your traceback should help you!")
        import traceback
        traceback.print_exc()
        await send_message(518221376, "Build Failed\!")
        exit(127)

if __name__ == '__main__':
    executor.start(dp, runner())