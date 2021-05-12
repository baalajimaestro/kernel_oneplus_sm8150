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
    message = await bot.send_message(user_id, text, disable_notification=False, disable_web_page_preview=True, parse_mode=types.ParseMode.MARKDOWN_V2)
    return message

async def edit_message(user_id: int, text: str, message: str):
    old_text =  message.md_text
    await message.edit_text(old_text + '\n' + text, disable_web_page_preview=True, parse_mode=types.ParseMode.MARKDOWN_V2)

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        print(stdout_line) 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        return return_code, popen.stdout
    else:
        return 0, None

async def runner():
    try:
        print("Retarded CI: Warming Up!")
        from git import Repo
        message = "`Retarded CI`\n"
        message += "`Spinning Build for commit:` [" + os.environ.get("SEMAPHORE_GIT_SHA")[:6] + "](https://github.com/baalajimaestro/kernel_oneplus_sm8150/commit/" + os.environ.get("SEMAPHORE_GIT_SHA") +")\n"
        job_id =  os.environ.get("SEMAPHORE_JOB_ID")
        job_id = job_id.replace("-", '\\-')
        message += "`Job ID: `" + job_id + "\n"
        message += "`Runner: " + os.environ.get("SEMAPHORE_AGENT_MACHINE_TYPE") + " With " + str(os.cpu_count()) + " Threads`\n"
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

        return_code, log = execute(list_defconfig)
        if return_code != 0:
            import requests
            nekobin_key = requests.post("https://nekobin.com/api/documents", json={"content":log[-200:]}).content.key
            await edit_message(518221376, "[Build Log](https://nekobin.com/" + nekobin_key + ")", message_track)
            raise RuntimeError

        message = "`Started Make....`"
        await edit_message(518221376, message, message_track)

        return_code, log = execute(list_make)
        if return_code != 0:
            nekobin_key = requests.post("https://nekobin.com/api/documents", json={"content":log[-200:]}).content.key
            await edit_message(518221376, "[Build Log](https://nekobin.com/" + nekobin_key + ")", message_track)
            raise RuntimeError

    except:
        print("Our Build Failed, but your traceback should help you!")
        import traceback
        traceback.print_exc()
        await send_message(518221376, "Build Failed\!")
        await bot.log_out()
        exit(127)

if __name__ == '__main__':
    executor.start(dp, runner())