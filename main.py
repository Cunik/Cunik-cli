#!/usr/bin/env python3
import sys
import requests

all_commands = ['list', 'stop', 'remove', 'help', 'create', 'info']

need_oprand = ['stop', 'remove', 'create', 'info']

base_url = 'http://127.0.0.1:5000/'


class CunikCLI:
    @staticmethod
    def match(id):
        list_of_cunik = CunikCLI.list()
        cnt = 0
        for i in list_of_cunik:
            if str(id) == str(i)[:len(str(id))]:
                cnt += 1
        if cnt > 1:
            print('Multiple matches')
            return None
        elif cnt == 1:
            for i in list_of_cunik:
                if str(id) == str(i)[:len(str(id))]:
                    return id
        else:
            print('No match found')
            return None

    @staticmethod
    def list():
        r = requests.get(base_url + 'cunik/list')
        if r.status_code == 200:
            for id in list(r.text):
                print(id)
                CunikCLI.info(id)
            return r.text
        else:
            print('ERROR')
            return []

    @staticmethod
    def stop(id):
        r = requests.post(base_url + 'cunik/stop', data={'cid': id})
        if r.status_code == 200:
            print('Stopped')
        else:
            print('ERROR')

    @staticmethod
    def start(id):
        r = requests.post(base_url + 'cunik/start', data={'cid': id})
        if r.status_code == 200:
            print('Started')
        else:
            print('ERROR')

    @staticmethod
    def remove(id):
        r = requests.post(base_url + 'cunik/remove', data={'cid': id})
        if r.status_code == 200:
            print('Removed')
        else:
            print('ERROR')

    @staticmethod
    def info(id):
        r = requests.post(base_url + 'cunik/info', data={'cid': id})
        if r.status_code == 200:
            print(json.loads(r.text))
        else:
            print('ERROR')

    @staticmethod
    def create(image_name, ipv4_addr):
        data = {}
        data['image_name'] = image_name
        data['ipv4_addr'] = ipv4_addr
        r = requests.post(base_url + 'cunik/create', data=data)

    @staticmethod
    def help():
        print("Usage: cunik-cli [list | info | create | stop | remove | help] <name>")
        print("list - Return all created cunik and its simple information")
        print("info - Return all informations about a cunik")
        print("create - Create a new cunik")
        print("stop - Stop a running cunik")
        print("remove - Remove a created cunik")


def main():
    if len(sys.argv) <= 1:
        return
    if sys.argv[1] not in all_commands:
        print('Invalid command')
        print('call help()')
        return
    if sys.argv[1] in need_oprand:
        if len(sys.argv) <= 2:
            return
    if sys.argv[1] == 'help':
        return CunikCLI.help()
    elif sys.argv[1] == 'list':
        return CunikCLI.list()
    elif sys.argv[1] == 'create':
        return CunikCLI.create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'stop':
        return CunikCLI.stop(sys.argv[2])
    elif sys.argv[1] == 'start':
        return CunikCLI.start(sys.argv[2])
    elif sys.argv[1] == 'remove':
        return CunikCLI.remove(sys.argv[2])
    else:
        print('Invalid command')
        return help()


if __name__ == '__main__':
    main()
