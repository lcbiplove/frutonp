from re import match as reMatch
import urllib
import json
import string
from django.conf import settings
from random import choice
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.shortcuts import get_object_or_404
from PIL import Image, ExifTags
from django.utils import timezone


def getExpireOfCookie(max_age):
    """ To return expire date time in string
    
        Param: (int)max_age, in seconds

        Return: string
     """
    return timezone.datetime.strftime(timezone.localtime() + timezone.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")


def randomToken(stringLength=48):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase+string.digits
    return ''.join(choice(letters) for i in range(stringLength))

def getCaptcha(postedCaptcha):
    url = f"https://www.google.com/recaptcha/api/siteverify?secret={settings.RECAPTCHA_SECRET_KEY}&response={postedCaptcha}"
    response = urllib.request.urlopen(url)
    last = json.loads(response.read().decode())
    return last

''' Raise validation error on file greater than given size '''
def file_size(value, max_size=20971520): # 20 MiB 20971520
    if value.size > max_size:
        raise ValidationError(f"File too large. Size should not exceed {max_size/1024/1024} MiB.")

''' Returns True if extension matches False, otherwise  '''
def right_ext(ext_of, accept_ext=[]):
    len_of_ext = len(accept_ext)
    for i in range(len_of_ext):
        if i==(len_of_ext-1):
            if not ext_of.endswith(accept_ext[i]):
                return False
        if ext_of.endswith(accept_ext[i]):
            return True

def validate_name(value):
    """
    Validate name
    """
    if reMatch('^[a-zA-Z-_ ]+$', value) is None or len(value) <=4 or len(value) >= 48:
        raise ValidationError("Name should be greater than 4 and less than 48 with underscores, whitespace and hyphen only.")
        

def validate_phone(value):
    """
    Raise error if validation faild
    """
    if len(str(value)) != 10:
        raise ValidationError(f"Phone number should be of 10 digits, you gave {len(str(value))} digit number.")

def add_post_date(day):
    """
    Return the added datetime according to the day

    @param: day
    
    @return: String 
    """
    return timezone.localtime()+timezone.timedelta(days=day)

def image_crop(obj):
    """ Crop image of the object.

        Must: Have get_image() function inside class which returns photo_attribute.path
    
        Param: object, object where one of attribute must have image field

        Return: None
     """
    img = Image.open(obj.get_image())
    width, height = img.size  # Get dimensions 
    
    ''' When a picture is taller than it is wide, it means the camera was rotated. Some cameras can detect this and write that info
        in the picture's EXIF metadata. Some viewers take note of this metadata and display the image appropriately. 
        To check the orientation and rotate if needed
        https://stackoverflow.com/questions/4228530/pil-thumbnail-is-rotating-my-image
    '''
    try:
        for orientation in ExifTags.TAGS.keys() : 
            if ExifTags.TAGS[orientation]=='Orientation' : break 
        exif=dict(img._getexif().items())

        if   exif[orientation] == 3 : 
            img=img.rotate(180)
        elif exif[orientation] == 6 : 
            img=img.rotate(270)
        elif exif[orientation] == 8 : 
            img=img.rotate(90)  
    except:
        pass     

    if width > 250 and height > 250:
        # keep ratio but shrink down
        img.thumbnail((width, height))

    # check which one is smaller
    if height < width:
        # make square by cutting off equal amounts left and right
        left = (width - height) / 2
        right = (width + height) / 2
        top = 0
        bottom = height
        img = img.crop((left, top, right, bottom))

    elif width < height:
        # make square by cutting off bottom
        left = 0
        right = width
        top = (height - width)/2
        bottom = (height + width)/2
        img = img.crop((left, top, right, bottom))

    if width > 250 and height > 250:
        img.thumbnail((250, 250))

    return img.save(obj.get_image())

def getUploadTimeDiff(par, isComment=False):
    """ Take object and return time difference """
    diff = timezone.now()-par.getUniversalDate()
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if seconds < 60 and minutes == 0 and hours == 0:
        out = f"{seconds} sec ago"
    elif minutes < 60 and hours == 0:
        out = f"{minutes} min ago"
    elif hours < 6:
        if isComment:
            out = f"{hours} hr ago"
        else:            
            if minutes == 0:
                out = f"{hours} hr ago"
            else:
                out = f"{hours} hr {minutes} min ago"
    elif hours < 24:
        out = f"{hours} hr ago"
    else:
        if days == 1:
            out = f"{days} day ago"
        else:
            out = f"{days} days ago"

    if isComment:
        num = out.find(" ")
        out = out[:(num+2)]
        out = out.replace(" ", "")
    return out

def getWeightNumForCalc(weight):
    if weight[-2:] == 'gm':
        return int(weight[:-2])/1000
    elif weight[-2:] == 'kg':
        try:
            return int(weight[:-2])
        except:
            return 1
    else:
        return 100