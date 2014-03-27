# -*- coding: utf-8 -*-

# sudo apt-get install python-pip
# sudo pip install pyvkoauth vkontakte

from pyvkoauth import auth
import vkontakte
import urllib
import re
import os.path
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.ini')
user_email = config.get('vk-auth', 'login')
user_password = config.get('vk-auth', 'pass')
group_id = 54935444  # edit
data_source = 'wall'  # [wall|group_music]


def prettify(fname):
    fname = re.sub('[/]', '', fname)
    fname = re.sub('&amp;', '&', fname)
    return fname


def get_music(vk):
    if data_source == 'group_music':
        get_group_music(vk)
    elif data_source == 'wall':
        get_wall_music(vk)


def get_group_music(vk):
    download = []
    music = vk.audio.get(gid=group_id)
    for i in music:
        filename = prettify(i['artist'] + " - " + i['title'] + ".mp3")
        download.append({'url': i['url'],
                         'filename': filename})
    wget_music(download)


def get_wall_music(vk):
    download = []
    vk_max_count = 100
    music = vk.wall.get(owner_id=-(group_id), count=vk_max_count)
    songs_num = music[0]
    for i in xrange(0, songs_num / 100 + 1):
        download += get_wall_music_more(vk, myoffset=i * vk_max_count)


def get_wall_music_more(vk, myoffset=0):
    download = []
    music = vk.wall.get(owner_id=-(group_id), count=100, offset=myoffset)
    for i in music[1:]:
        if 'attachments' in i.keys():
            for att in i['attachments']:
                if 'audio' in att.keys():
                    filename = prettify(att['audio']['artist'] + " - " +
                                        att['audio']['title'] + ".mp3")
                    download.append({'url': att['audio']['url'],
                                     'filename': filename})
    wget_music(download)


def wget_music(music_dict):
    for song in music_dict:
        if not os.path.isfile(song['filename']):
            print song['filename']
            urllib.urlretrieve(song['url'], song['filename'])


def main():
    client_id = 4268618
    scope = 49151

    response = auth(user_email, user_password, client_id, scope)
    access_token = response['access_token']

    vk = vkontakte.API(token=access_token)
    get_music(vk)


if __name__ == "__main__":
        main()
