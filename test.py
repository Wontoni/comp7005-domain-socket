import asyncio

messages = ['This is the message. ',
            'It will be sent ',
            'in parts.',
            ]
server_address = ('localhost', 8080)

async def send_messages(server_address, messages):
    reader, writer = await asyncio.open_connection(*server_address)
    for message in messages:
        print(f'Sending: {message}')
        writer.write(message.encode())
        await writer.drain()  # Ensure message is sent
        data = await reader.read(1024)
        print(f'Received: {data.decode()}')
    # print('Close the connection')
    writer.close()
    await writer.wait_closed()

async def main():
    tasks = [send_messages(server_address, messages) for _ in range(2)]
    await asyncio.gather(*tasks)

asyncio.run(main())
