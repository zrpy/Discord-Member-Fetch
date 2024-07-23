import aiohttp,asyncio,json,time

token=""#not bot
server_id=""
channel_id=""

async def get_members(token,server,channel):
    session = aiohttp.ClientSession()
    async with session.ws_connect("wss://gateway.discord.gg/?v=9&encoding=json") as ws:
        users=[]
        async for msg in ws: 
            response=json.loads(msg.data)
            if response["t"]==None:
                await ws.send_json({"op":2,"d":{"token":token,"capabilities":16381,"properties":{"os":"Windows","browser":"Discord Client","release_channel":"stable","client_version":"1.0.9154","os_version":"10.0.1.19045","os_arch":"x64","app_arch":"x64","system_locale":"ja","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36","browser_version":"30.1.0","client_build_number":311885,"native_build_number":49586,"client_event_source":None},"presence":{"status":"invisible","since":0,"activities":[],"afk":False},"compress":False,"client_state":{"guild_versions":{},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1,"private_channels_version":"0","api_code_version":0}}})
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
