"""
System Commands - Owner only (eval, exec, restart)
"""

import sys
import os
import asyncio
import traceback
from telethon import events
from config import OWNER_ID, CMD_PREFIX
from utils.helpers import edit_or_reply, command_pattern, is_owner


def register(client):
    @client.on(command_pattern("eval(?: |$)([\\s\\S]*)"))
    async def evaluate(event):
        if OWNER_ID and event.sender_id != OWNER_ID:
            return
        code = event.pattern_match.group(1).strip()
        if not code:
            return await edit_or_reply(event, "❌ Provide code to evaluate")

        try:
            result = eval(code, {"__builtins__": {}}, {
                "client": client,
                "event": event,
                "asyncio": asyncio,
            })
            if asyncio.iscoroutine(result):
                result = await result
            await edit_or_reply(event, f"**Eval Result:**\n```\n{result}\n```")
        except Exception as e:
            await edit_or_reply(event, f"**Error:**\n```\n{traceback.format_exc()}\n```")

    @client.on(command_pattern("exec(?: |$)([\\s\\S]*)"))
    async def execute(event):
        if OWNER_ID and event.sender_id != OWNER_ID:
            return
        cmd = event.pattern_match.group(1).strip()
        if not cmd:
            return await edit_or_reply(event, "❌ Provide shell command")

        try:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            output = stdout.decode() + stderr.decode()
            if len(output) > 4000:
                output = output[:4000] + "\n... (truncated)"
            await edit_or_reply(event, f"**Exec Output:**\n```\n{output or 'No output'}\n```")
        except Exception as e:
            await edit_or_reply(event, f"**Error:** `{e}`")

    @client.on(command_pattern("restart$"))
    async def restart(event):
        if OWNER_ID and event.sender_id != OWNER_ID:
            return
        await edit_or_reply(event, "🔄 Restarting Tanya UserBot...")
        os.execl(sys.executable, sys.executable, *sys.argv)

    @client.on(command_pattern("logs$"))
    async def get_logs(event):
        if OWNER_ID and event.sender_id != OWNER_ID:
            return
        await edit_or_reply(
            event,
            "**📜 Logs**\n\n"
            "Logs are printed to Render dashboard.\n"
            "Check your Render service logs for detailed output."
        )
