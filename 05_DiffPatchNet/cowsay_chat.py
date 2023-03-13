import asyncio
import cowsay

clients = {}
cows_list = cowsay.list_cows()


async def chat(reader, writer):
    is_registered = False
    me = ""
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                message = q.result().decode().split()
                command = message[0]

                if not is_registered:
                    if command == 'login':
                        if (message[1] in cows_list):
                            me = message[1]
                            cows_list.remove(message[1])

                            clients[me] = asyncio.Queue()
                            print("Registered: ", me)
                            writer.write("You are registered!\n".encode())
                            await writer.drain()
                            is_registered = True
                            receive.cancel()
                            receive = asyncio.create_task(clients[me].get())
                        else:
                            writer.write("Invalid name!\n".encode())
                            await writer.drain()
                    elif command == 'quit':
                        send.cancel()
                        receive.cancel()
                        writer.close()
                        await writer.wait_closed()
                        return
                    elif command == 'cows':
                        writer.write(
                            f"Available cows: {', '.join(cows_list)}\n".encode())
                        await writer.drain()
                    else:
                        writer.write("Invalid command!\n".encode())
                        await writer.drain()
                else:
                    if command == 'quit':
                        send.cancel()
                        receive.cancel()
                        del clients[me]
                        print("Unregistered: ", me)
                        cows_list.append(me)
                        writer.close()
                        await writer.wait_closed()
                        return
                    elif command == 'who':
                        writer.write(
                            f"Users: {', '.join(clients.keys())}\n".encode())
                        await writer.drain()
                    elif command == 'say':
                        if message[1] in clients.keys():
                            await clients[message[1]].put(f"From: {me}\n {cowsay.cowsay((' '.join(message[2:])).strip(), cow=me)}")
                            await writer.drain()
                        else:
                            writer.write("Invalid username!\n".encode())
                            await writer.drain()
                    elif command == 'yield':
                        for out in clients.values():
                            if out is not clients[me]:
                                await out.put(f"From: {me}\n {cowsay.cowsay(' '.join(message[1:]).strip(), cow=me)}")
                        await writer.drain()

            elif q is receive and is_registered:
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
