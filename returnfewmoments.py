import aiohttp,asyncio,json,time

token=""#not bot
server_id=""
channel_id=""

async def get_members(token,server,channel):
    session = aiohttp.ClientSession()
    async with session.ws_connect("wss://gateway.discord.gg/?v=10&encoding=json") as ws:
        users=[]
        async for msg in ws: 
            response=json.loads(msg.data)
            if response["t"]==None:
                await ws.send_json({"op":2,"d":{"token":token,"capabilities":16381,"properties":{"os":"Android","browser":"Discord Android","device":"Android","system_locale":"ja-JP","browser_user_agent":"Discord-Android/223015","browser_version":"","os_version":"","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":223015,"client_event_source":None},"presence":{"status":"invisible","since":0,"activities":[],"afk":False},"compress":False,"client_state":{"guild_versions":{},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1,"private_channels_version":"0","api_code_version":0}}})
            elif response["t"]=="READY_SUPPLEMENTAL":
                await ws.send_json({"op":14,"d":{"guild_id":server,"typing":True,"activities":True,"threads":True,"channels":{channel:[[0,99]]}}})
            elif response["t"]=="GUILD_MEMBER_LIST_UPDATE":
                for _ in response["d"]["ops"]:
                    if _["op"]=="SYNC":
                        for i in _["items"]:
                            if "member" in i:
                                users.append(i["member"]["user"]["id"])
                        await session.close()
                        return users


async def main():
    print(await get_members(token,server_id,channel_id))

asyncio.run(main())
