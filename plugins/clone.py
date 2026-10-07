"""Clone Plugin"""
import os
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from utils.helpers import edit_or_reply, command_pattern
from core.decorators import owner_only, errors_handler

ORIGINAL = {}

def register(client):
    @client.on(command_pattern("clone(?: |$)(.*)"))
    @owner_only
    @errors_handler
    async def clone_user(event):
        if not event.is_reply:
            return await edit_or_reply(event, "❌ Reply to a user to clone")
        reply = await event.get_reply_message()
        user = await event.client.get_entity(reply.sender_id)
        full = await client(GetFullUserRequest(user.id))
        me = await client.get_me()
        my_full = await client(GetFullUserRequest(me.id))
        ORIGINAL["first_name"] = me.first_name or "User"
        ORIGINAL["last_name"] = me.last_name or ""
        ORIGINAL["about"] = my_full.full_user.about or ""
        await client(UpdateProfileRequest(first_name=user.first_name or "User", last_name=user.last_name or "", about=(full.full_user.about or "")[:70]))
        try:
            photos = await client.get_profile_photos(user.id, limit=1)
            if photos:
                file = await client.download_media(photos[0], file="data/clone_photo.jpg")
                await client(UploadProfilePhotoRequest(file=await client.upload_file(file)))
                os.remove(file)
        except: pass
        await edit_or_reply(event, f"**✅ Cloned** [{user.first_name}](tg://user?id={user.id})\nUse `.revert` to restore.")

    @client.on(command_pattern("revert$"))
    @owner_only
    @errors_handler
    async def revert_profile(event):
        if not ORIGINAL: return await edit_or_reply(event, "❌ Nothing to revert")
        await client(UpdateProfileRequest(first_name=ORIGINAL.get("first_name", "User"), last_name=ORIGINAL.get("last_name", ""), about=ORIGINAL.get("about", "")[:70]))
        ORIGINAL.clear()
        await edit_or_reply(event, "**✅ Profile reverted**")
