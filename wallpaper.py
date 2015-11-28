#!/usr/bin/env python3

"""
Wallpaper switcher using subreddits.

Source code: https://github.com/DStewart1997/wallpaper-changer
"""

import getpass
import os
from sys import platform
import urllib.request
import praw
import zipfile


class FileMgmt(object):
    """Sets file paths and creates non-existant paths."""

    def __init__(self):
        """Sets the paths depending on operating system and creates them if
        they don't exist."""
        username = getpass.getuser()

        if platform == 'linux':
            self.imagedir = '/home/' + username + '/Pictures/wp_switcher/'
            self.tmpdir = '/home/' + username + '/Downloads/tmp/'
        elif platform == 'win32':
            self.imagedir = 'C:\\Users\\' + username + \
                '\\Pictures\\wp_switcher\\'
            self.tmpdir = 'C:\\Users\\' + username + '\\Downloads\\tmp\\'

        # If paths do not exist - make them.
        if not os.path.exists(self.imagedir):
            os.makedirs(self.imagedir)
        if not os.path.exists(self.tmpdir):
            os.makedirs(self.tmpdir)


class Downloader(object):
    """Parses various links to download images from them.
    Currently supported is imgur (and albums) and DeviantArt."""

    def __init__(self, link):
        self.link = link

    def download_imgur_album(self):
        """Parses imgur album links.
        Downloads the album as a zip, extracts it, then cleans up."""

        zip_name = "wp_images.zip"
        urllib.request.urlretrieve(self.link + "/zip", fm.imagedir + zip_name)

        zip_ref = zipfile.ZipFile(fm.imagedir + zip_name, 'r')
        zip_ref.extractall(fm.imagedir)
        zip_ref.close()

        os.remove(fm.imagedir + zip_name)
        os.rmdir(fm.tmpdir)

        print("Imgur album:", self.link)

    def download_imgur(self):
        """Donwloads imgur links, detects links that don't have file
        extensions and fixes them."""

        print("Regular imgur:", self.link)

    def download_deviantart(self):
        """Downloads images from DeviantArt links.
        Gets the source code of the web page and parses line 347 to get direct
        image link - seems to be reliable but a better method should be
        used down the line."""

        print("Deviant Art:", self.link)

# Sets PRAW info.
user_agent = "Wallpaper switcher"
subreddit = 'minimalwallpaper'
r = praw.Reddit(user_agent=user_agent)
submissions = r.get_subreddit(subreddit).get_hot(limit=50)

fm = FileMgmt()

images = []
for submission in submissions:
    images.append(Downloader(submission.url))

for img in images:
    if "imgur.com/a" in img.link:
        Downloader.download_imgur_album(img)
    elif "imgur.com" in img.link:
        Downloader.download_imgur(img)
    elif "deviantart.com" in img.link:
        Downloader.download_deviantart(img)
    else:
        print("Other:", img.link)
