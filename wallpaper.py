import ctypes, praw, urllib.request, zipfile, os, getpass, imghdr
from PIL import Image
from sys import platform

# ToDo: Add argparse to set no. of images, which subreddit and which resolution.
#   Set wallpaper to change for each platform and each DE.

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


def get_image_size(image_name):
    file = open(imagedir + image_name, 'rb')
    img = Image.open(file)
    img.load()
    size = img.size
    file.close()

    return size

def download_album(link):
    zip_name = "images.zip"

    urllib.request.urlretrieve(link, imagedir + zip_name)  # Download the album as a zip file

    zip_ref = zipfile.ZipFile(imagedir + zip_name, 'r')  # Extract the zip file
    zip_ref.extractall(imagedir)
    zip_ref.close()

    os.remove(imagedir + zip_name)  # Delete the remaining zip file

def download_image(link, path=imagedir):
    image_name = link.rpartition('/')[2]
    urllib.request.urlretrieve(link, path + image_name)

    # print(get_image_size(image_name))

# Gets page source - Line 347 has the download link - seems to always be at this line no matter the image
def download_deviantart(link):
    response = urllib.request.urlopen(link)
    link_line = ""
    for line_number, line in enumerate(response):

        if line_number == 346:  # Zero-based
            link_line = str(line)

        elif line_number > 346:
            break

    image_link = link_line.split()[3].partition('"')[-1].rpartition('"')[0]
    image_name = image_link.rpartition('/')[-1]
    urllib.request.urlretrieve(image_link, imagedir + image_name)

    print(get_image_size(image_name))


user_agent = "Wallpaper switcher"
subreddit = 'minimalwallpaper'

r = praw.Reddit(user_agent=user_agent)
submissions = r.get_subreddit(subreddit).get_hot(limit=25)

for submission in submissions:
    if "imgur.com/a" in submission.url:
        download_album(submission.url + "/zip")  # Can append /zip to url to download zip of album
    elif "i.imgur.com" in submission.url:
        download_image(submission.url)
    elif "imgur.com" in submission.url:
        download_image(submission.url + ".png", tmpdir)  # Download separately and rename to correct extension later.
    elif "deviantart.com" in submission.url:
        download_deviantart(submission.url)
    else:
        print("Other: " + submission.url)  # Other image hosts and self-posts


# Fix files with wrong extensions. Some files are detected as 'None' type - so far only jpegs.
for file in os.listdir(tmpdir):
    ext = imghdr.what(tmpdir + file)
    os.rename(tmpdir + file, imagedir + file.split('.')[0] + '.' + str(ext))


# Set the wallpaper
# image_path = "C:\\Bird.jpg"
# SPI_SETDESKWALLPAPER = 20
# ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 0)
