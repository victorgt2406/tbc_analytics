import asyncio
from utils.elk_msgraph import ElkMsgraph


em = ElkMsgraph()
async def auto_update():
    await asyncio.gather(
        em.auto_update_basicdata()
        # em.auto_update_logins()
    )

asyncio.run(auto_update())