# -*- coding: utf-8 -*-

# sudo apt-get install python-pip
# sudo pip install pyvkoauth vkontakte

from pyvkoauth import auth
import vkontakte
import urllib
import re

user_email = 'me@vk.com'  # edit
user_password = 'mypassword'  # edit
group_id = 54935444  # edit

client_id = 4268618
scope = 49151

response = auth(user_email, user_password, client_id, scope)
access_token = response['access_token']

vk = vkontakte.API(token=access_token)

music = vk.audio.get(gid=group_id)
counter = 0
for i in music:

    url = i['url']
    title = i['artist'] + " - " + i['title'] + ".mp3"
    filename = re.sub('[/]', '', title)

    print '[', counter, '/', len(music), ']', filename.encode('utf-8')
    counter += 1

    urllib.urlretrieve(url, filename)
