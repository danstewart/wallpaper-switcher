#!/usr/bin/env python3

"""Wallpaper switcher using subreddits.
Source code: https://github.com/DStewart1997/wallpaper-changer"""

import getpass
import os
from sys import platform
import praw

class FileMgmt(object):
    def set_paths():
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


class Downloader(object):
    def __init__(self, link):
        self.link = link

    def download_imgur_album(self):
        print("Album:", self.link)

    def download_imgur(self):
        print("Regular imgur:", self.link)

    def download_deviantart(self):
        print("Deviant Art:", self.link)


user_agent = "Wallpaper switcher"
subreddit = 'minimalwallpaper'
r = praw.Reddit(user_agent=user_agent)
submissions = r.get_subreddit(subreddit).get_hot(limit=25)

FileMgmt.set_paths()

images = []
for submission in submissions:
    images.append(Downloader(submission.url))

for img in images:
    if "imgur/a" in img.link:
        Downloader.download_imgur_album(img)
    elif "imgur.com" in img.link:
        Downloader.download_imgur(img)
    elif "deviantart.com" in img.link:
        Downloader.download_deviantart(img)
    else:
        print("Other:", img.link)
