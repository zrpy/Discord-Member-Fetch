import aiohttp,asyncio,json,time

token=""#not bot
server_id=""
channel_id=""

async def get_members(token,server,channel):
    session = aiohttp.ClientSession()
    async with session.ws_connect("wss://gateway.discord.gg/?v=10&encoding=json") as ws:
        users=[]
        member_count=0
        multiple=0
        channel_user=[[0,99]]
        count=99
        async for msg in ws: 
            response=json.loads(msg.data)
            if response["t"]==None:
                await ws.send_json({"op":2,"d":{"token":token,"capabilities":16381,"properties":{"os":"Android","browser":"Discord Android","device":"Android","system_locale":"ja-JP","browser_user_agent":"Discord-Android/223015","browser_version":"","os_version":"","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":223015,"client_event_source":None},"presence":{"status":"invisible","since":0,"activities":[],"afk":False},"compress":False,"client_state":{"guild_versions":{},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1,"private_channels_version":"0","api_code_version":0}}})
            elif response["t"]=="READY":
                for _ in response["d"]["guilds"]:
                    member_count=_["member_count"]
            elif response["t"]=="READY_SUPPLEMENTAL":
                await ws.send_json({"op":14,"d":{"guild_id":server,"typing":True,"activities":True,"threads":True,"channels":{channel:[[0,99]]}}})
            elif response["t"]=="GUILD_MEMBER_LIST_UPDATE":
                for _ in response["d"]["ops"]:
                    if _["op"]=="SYNC":
                        for i in _["items"]:
                            if "member" in i:
                                users.append(i["member"]["user"]["id"])
                    elif _["op"]=="UPDATE":
                        users.append(_["item"]["member"]["user"]["id"])
                    if count<member_count:
                        start_num = int(100*multiple)
                        end_num=start_num+99
                        ranges = [[0,99],[start_num, end_num]]
                        count=end_num
                        await ws.send_json({"op":14,"d":{"guild_id":server,"typing":True,"activities":True,"threads":True,"channels":{channel:ranges}}})
                        multiple+=1
                        time.sleep(0.5)
                    else:break
        await session.close()
        return users


async def main():
    print(await get_members(token,server_id,channel_id))

asyncio.run(main())
