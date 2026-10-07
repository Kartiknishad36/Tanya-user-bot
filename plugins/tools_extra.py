"""Extra Tools - calc hash base64"""
import ast, operator
from utils.helpers import edit_or_reply, command_pattern
from utils.tools import md5, sha256, b64encode, b64decode, random_string
from core.decorators import errors_handler

SAFE_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg, ast.Mod: operator.mod}

def safe_eval(expr):
    def _eval(node):
        if isinstance(node, ast.Expression): return _eval(node.body)
        if isinstance(node, ast.Constant): return node.value
        if isinstance(node, ast.BinOp): return SAFE_OPS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp): return SAFE_OPS[type(node.op)](_eval(node.operand))
        raise ValueError("Unsupported")
    return _eval(ast.parse(expr, mode="eval"))

def register(client):
    @client.on(command_pattern("calc(?: |$)(.*)"))
    @errors_handler
    async def calculator(event):
        expr = event.pattern_match.group(1).strip()
        if not expr: return await edit_or_reply(event, "❌ Usage: `.calc 2+2*5`")
        try: await edit_or_reply(event, f"**🧮 Result:** `{safe_eval(expr)}`")
        except Exception as e: await edit_or_reply(event, f"❌ `{e}`")

    @client.on(command_pattern("md5(?: |$)(.*)"))
    @errors_handler
    async def md5_hash(event):
        text = event.pattern_match.group(1).strip() or ((await event.get_reply_message()).text if event.is_reply else "")
        if not text: return await edit_or_reply(event, "❌ Provide text")
        await edit_or_reply(event, f"**MD5:** `{md5(text)}`")

    @client.on(command_pattern("sha(?: |$)(.*)"))
    @errors_handler
    async def sha_hash(event):
        text = event.pattern_match.group(1).strip() or ((await event.get_reply_message()).text if event.is_reply else "")
        if not text: return await edit_or_reply(event, "❌ Provide text")
        await edit_or_reply(event, f"**SHA256:** `{sha256(text)}`")

    @client.on(command_pattern("b64e(?: |$)(.*)"))
    @errors_handler
    async def b64e(event):
        text = event.pattern_match.group(1).strip() or ((await event.get_reply_message()).text if event.is_reply else "")
        if not text: return await edit_or_reply(event, "❌ Provide text")
        await edit_or_reply(event, f"**Base64:** `{b64encode(text)}`")

    @client.on(command_pattern("b64d(?: |$)(.*)"))
    @errors_handler
    async def b64d(event):
        text = event.pattern_match.group(1).strip() or ((await event.get_reply_message()).text if event.is_reply else "")
        if not text: return await edit_or_reply(event, "❌ Provide text")
        await edit_or_reply(event, f"**Decoded:** `{b64decode(text)}`")

    @client.on(command_pattern("random(?: |$)(.*)"))
    @errors_handler
    async def rand(event):
        args = event.pattern_match.group(1).strip()
        length = min(int(args), 64) if args.isdigit() else 12
        await edit_or_reply(event, f"**Random:** `{random_string(length)}`")

    @client.on(command_pattern("reverse(?: |$)(.*)"))
    @errors_handler
    async def rev(event):
        text = event.pattern_match.group(1).strip() or ((await event.get_reply_message()).text if event.is_reply else "")
        if not text: return await edit_or_reply(event, "❌ Provide text")
        await edit_or_reply(event, text[::-1])
