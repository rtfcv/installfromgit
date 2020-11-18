import urllib.request
import os
import platform
import io
import json
import pandas as pd
import subprocess
pre = 'https://api.github.com/repos/'
suf = '/releases/latest'

project = 'VSCodium/vscodium'
dl_regex = r'.*amd64.deb$'


try:
    with urllib.request.urlopen(pre+project+suf) as response:
        body = json.loads(response.read())
        headers = response.getheaders()
        status = response.getcode()

        print(headers)
        # print(body)
        print(status)

except urllib.error.URLError as e:
    print('-'*8+'error'+'-'*8)
    print(e.reason)

assets = pd.DataFrame(body['assets'])
print(assets.name)

_download_index = assets.name.str.match(dl_regex)

for _url in assets[_download_index].browser_download_url:
    print(_url)

tempdf = pd.DataFrame(
    {"project": [project], "dl_regex": [dl_regex], 'prev_url': _url})
tempdf.to_csv('tempcsv.csv')


_PLATFORM = platform.system()
if (_PLATFORM == 'Windows'):
    print('Windows')
elif (_PLATFORM == 'Linux'):
    print('Linux')
    # _data = urllib.request.urlopen(_url)
    # with io.open("/tmp/temp.deb", "wb") as file:
    #     file.write(_data.read())
    # subprocess.check_call(['sudo', 'apt', 'install', '/tmp/temp.deb'])
else:
    print('Unknown Platform')

