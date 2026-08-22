#MADE_BY_NOBITA

import asyncio
from telethon import Button
from telethon.errors import UserNotParticipantError, ChatAdminRequiredError
from telethon.tl.functions.channels import GetParticipantRequest
from config import CHECK_CHANNELS, JOIN_URLS, logger

async def check_channel_joined(bot, uid, is_admin_func):
    """Force-join disabled — always returns True (all users treated as joined)."""
    return True

async def get_unjoined_channels(bot, uid):
    """Returns list of (url, index) for channels the user has NOT joined."""
    unjoined = []
    for i, ch in enumerate(CHECK_CHANNELS):
        try:
            ch_id = int(ch.strip()) if str(ch).strip().lstrip('-').isdigit() else ch.strip()
            try:
                await bot(GetParticipantRequest(channel=ch_id, participant=uid))
            except ValueError:
                entity = await bot.get_entity(ch_id)
                await bot(GetParticipantRequest(channel=entity, participant=uid))
        except UserNotParticipantError:
            if i < len(JOIN_URLS):
                unjoined.append((JOIN_URLS[i], i + 1))
        except ChatAdminRequiredError:
            # Bot lost admin / never had it in this channel — real error, not "unjoined"
            logger.error(f"Bot is not admin in channel: {ch}")
            if i < len(JOIN_URLS):
                unjoined.append((JOIN_URLS[i], i + 1))
        except Exception as e:
            # Previously this branch swallowed ANY error silently and treated it
            # identically to "not joined" — no trace in logs. Now it's logged.
            logger.error(f"Channel Check Error for {ch} (uid={uid}): {type(e).__name__}: {e}")
            if i < len(JOIN_URLS):
                unjoined.append((JOIN_URLS[i], i + 1))
    return unjoined
