#!/usr/bin/env python3
import urllib.request
import os
import platform
import io
import json
import pandas as pd
import subprocess

_pre = 'https://api.github.com/repos/'
_suf = '/releases/latest'

pkgdatafile = 'pkg.csv'
packagedata = pd.read_csv(pkgdatafile)


for i in packagedata.index:
    _project = packagedata.project[i]
    _dl_regex = packagedata.dl_regex[i]
    _prev_url = packagedata.prev_url[i]

    try:
        with urllib.request.urlopen(_pre+_project+_suf) as response:
            body = json.loads(response.read())
            # headers = response.getheaders()
            # status = response.getcode()

            # print(headers)
            # print(body)
            # print(status)

    except urllib.error.URLError as e:
        print('-'*8+'error'+'-'*8)
        print(e.reason)

    assets = pd.DataFrame(body['assets'])
    # print(assets.name)

    _download_index = assets.name.str.match(_dl_regex)

    if len(assets[_download_index].browser_download_url) > 1:
        print(f'You have to reconsider the regex for specifying \
              the asset file you would like to install for \
              package: {_project}')
        continue

    for _url in assets[_download_index].browser_download_url:
        print(f'Checking update for {_project}...')

    if _url == _prev_url:
        print(f'{_project} is up to date')
        continue
    else:
        tempdf = pd.DataFrame(
            {"project": [_project],
             "dl_regex": [_dl_regex],
             'prev_url': _url})

        # begin downoad and installations
        print(f'updating {_project}')

        _PLATFORM = platform.system()
        if (_PLATFORM == 'Windows'):
            print('Windows')
        elif (_PLATFORM == 'Linux'):
            print('Linux')
            print(f'downloading from {_url}')
            _data = urllib.request.urlopen(_url)
            with io.open("/tmp/temp.deb", "wb") as file:
                file.write(_data.read())
            subprocess.check_call(['sudo', 'apt', 'install', '/tmp/temp.deb'])

            # do below on success
            packagedata.prev_url[i] = _url
            packagedata.to_csv(pkgdatafile, index=False)
        else:
            print('Unknown Platform')

