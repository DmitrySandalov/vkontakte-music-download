# sudo apt-get install python-pip
# sudo pip install pyvkoauth vkontakte

from pyvkoauth import auth
import vkontakte
import urllib

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
    title = str(i['artist'] + " - " + i['title']).translate(None, '/') + ".mp3"

    print '[', counter, '/', len(music), ']', title
    counter += 1

    urllib.urlretrieve(url, title)
