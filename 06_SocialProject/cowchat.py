#!/usr/bin/env python3
import asyncio
import cowsay
import shlex

clients = {}
cows_to_peers = {}
peers_to_cows = {}

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                match shlex.split(q.result().decode()):
                    case ["who", ]:
                        await clients[me].put(f"{list(cows_to_peers.keys())}")
                    case ["cows", ]:
                        await clients[me].put(f"{[cow for cow in cowsay.list_cows() if cow not in cows_to_peers]}")
                    case ["login", cow]:
                        if cow in cowsay.list_cows():
                            if cow in cows_to_peers:
                                await clients[me].put("Cow name is already taken")
                            else:
                                cows_to_peers[cow] = clients[me]
                                peers_to_cows[clients[me]] = cow
                        else:
                            await clients[me].put("Unacceptable cow name")
                    case ["say", cow, *text]:
                        if cow in cows_to_peers:
                            await cows_to_peers[cow].put(cowsay.cowsay("".join(text), cow=peers_to_cows[clients[me]]))
                        else:
                            await clients[me].put("There is no cow with such name")
                    case ["yield", *text]:
                        for cow in cows_to_peers:
                            if cows_to_peers[cow] != clients[me]:
                                await cows_to_peers[cow].put(cowsay.cowsay("".join(text), cow=peers_to_cows[clients[me]]))
                    case ["quit"]:
                        cow = peers_to_cows[clients[me]]
                        cows_to_peers.pop(cow)
                        peers_to_cows.pop(clients[me])
                        send.cancel()
                        receive.cancel()
                        print(me, "DONE")
                        del clients[me]
                        writer.close()
                        await writer.wait_closed()

            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())