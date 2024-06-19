import asyncio
import requests
import argparse


class AsyncCheck:
    def __init__(self, targets, concurrent):
        self.targets = targets
        self.semaphore = asyncio.Semaphore(concurrent)

    async def send_request(self, host, port):
        async with self.semaphore:
            try:
                reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=90)
                return [host, port, True]
            except (ConnectionRefusedError, asyncio.TimeoutError, Exception):
                return [host, port, False]
            finally:
                if 'writer' in locals():
                    writer.close()

    async def manage(self):
        tasks = [self.send_request(target[0], target[1]) for target in self.targets]
        results = await asyncio.gather(*tasks)

        message = ''
        for result in results:
            status = result[2]
            if not status:
                message += f'{result[0]}:{result[1]} --> Closed\n'
        return message


async def run(targets, concurrent):
    return await AsyncCheck(targets, concurrent).manage()


def parse_handler():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, help='port list path to check')
    parser.add_argument('-c', '--concurrent', default=10, type=int, help='concurrent to request')
    parser.add_argument('-t', '--token', required=True, help='telegram bot token')
    parser.add_argument('-i', '--id', required=True, help='telegram chat id')
    args = parser.parse_args()
    return args.file, args.concurrent, args.token, args.id


def load_targets(file):
    with open(file) as f:
        lines = f.readlines()
        ret = [line.strip().split(':') for line in lines if line.strip()]
        return ret


if __name__ == '__main__':
    file_path, concurrent, token, chat_id = parse_handler()

    targets = load_targets(file_path)

    msg = asyncio.run(run(targets, concurrent))

    if msg:
        msg = 'IP:PORT Scan Results:\n' + msg
        print('发送 telegram 消息通知')
        try:
            # r = requests.post(f'https://api.telegram.org/bot{token}/sendMessage',
            #                   json={"chat_id": chat_id, "text": msg},
            #                   proxies={"http": f"http://192.168.31.220:7890", 'https': 'http://192.168.31.220:7890'})
            r = requests.post(f'https://api.telegram.org/bot{token}/sendMessage',
                              json={"chat_id": chat_id, "text": msg})
            if r.status_code == 200:
                print('发送 telegram 消息成功')
            else:
                print('发送 telegram 消息失败')
        except Exception as e:
            print(f'发送 telegram 消息失败: {e}')
    else:
        print('所有对象均可达，无需发送消息')

