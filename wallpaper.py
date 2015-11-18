import ctypes, praw, urllib.request, zipfile, os, getpass, imghdr
from PIL import Image
from sys import platform

#  Set wallpaper to change for each platform and each DE.
if platform == 'linux':
    username = getpass.getuser()
    imagedir = '/home/' + username + '/Downloads/'
    tmpdir = '/home/' + username + '/Downloads/tmp/'
elif platform == 'win32':
    username = getpass.getuser()
    imagedir = 'C:\\Users\\' + username + '\\Pictures\\wp_switcher\\'
    tmpdir = 'C:\\Users\\' + username + '\\Pictures\\wp_switcher\\tmp\\'


# If paths do not exist - make them.
if not os.path.exists(imagedir):
        os.makedirs(imagedir)
if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)

        
class Image(object):
    def __init__(self, link):
        self.link = link

    def download_imgur_album(self):
        print()


user_agent = "Wallpaper switcher"
subreddit = 'minimalwallpaper'
r = praw.Reddit(user_agent=user_agent)
submissions = r.get_subreddit(subreddit).get_hot(limit=25)

images = []
for submission in submissions:
    images.append(Image(submission.url))
