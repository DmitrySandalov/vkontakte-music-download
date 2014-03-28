#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sudo apt-get install python-pip
# sudo pip install pyvkoauth vkontakte

from pyvkoauth import auth
import vkontakte
import urllib
import re
import os.path
import ConfigParser
import argparse
import sys

config = ConfigParser.RawConfigParser()
config_folder = os.path.dirname(os.path.realpath(__file__))
config.read(config_folder + '/config.ini')
user_email = config.get('vk-auth', 'login')
user_password = config.get('vk-auth', 'pass')
counter = 0


def prettify(fname):
    fname = re.sub('[/]', '', fname)
    fname = re.sub('&amp;', '&', fname)
    return fname


def get_music(vk, wall, group_id):
    if wall:
        get_wall_music(vk, group_id)
    elif not wall:
        get_group_music(vk, group_id)


def get_group_music(vk, group_id):
    download = []
    music = vk.audio.get(gid=group_id)
    songs_num = len(music)
    for i in music:
        filename = prettify(i['artist'] + " - " + i['title'] + ".mp3")
        download.append({'url': i['url'],
                         'filename': filename})
    wget_music(download, total=songs_num)


def get_wall_music(vk, group_id):
    download = []
    vk_max_count = 100
    music = vk.wall.get(owner_id=-(group_id), count=vk_max_count)
    songs_num = music[0]
    for i in xrange(0, songs_num / vk_max_count):
        download += get_wall_music_more(vk, group_id, songs_num,
                                        myoffset=i * vk_max_count)


def get_wall_music_more(vk, group_id, songs_num, myoffset=0):
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
    wget_music(download, total=songs_num)


def wget_music(music_dict, total):
    global counter
    for song in music_dict:
        counter += 1
        if not os.path.isfile(song['filename']):
            print "[", counter, "/", total, "]", song['filename']
            try:
                urllib.urlretrieve(song['url'], song['filename'])
            except KeyboardInterrupt:
                os.remove(song['filename'])
                sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Downloads music from Vk.')
    parser.add_argument('-w', '--wall', action="store_true",
                        help='get songs from wall (default: group songs)')
    parser.add_argument('group', type=int, help="vk group id")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    wall = True if args.wall else False

    client_id = 4268618
    scope = 49151

    response = auth(user_email, user_password, client_id, scope)
    access_token = response['access_token']

    vk = vkontakte.API(token=access_token)
    get_music(vk, wall, args.group)


if __name__ == "__main__":
    main()
