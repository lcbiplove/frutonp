from django.db import models
from django.forms import ModelForm
from join.models import MyUser
from django.core.validators import FileExtensionValidator
from frutonp.utils import file_size, image_crop, getUploadTimeDiff, getWeightNumForCalc, getSlicedNotificationMessages
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext as __
import gettext
from bikram import samwat
from django.utils.translation import get_language as current_language
from django.utils import timezone
from home.templatetags.number_translator import translate_num_eng_to_nep

def getFoodChoice(food_code, food):
    return food_code+'_NE_'+gettext.translation('django', 'posts/locale', ['ne'], fallback=True).gettext(food)

class Post(models.Model):
    NUM_OF_FRUIT = 5
    NUM_OF_VEG = 5
    CATEGORIES = ['Vegetable', 'Fruit']
    VEG =  [
        getFoodChoice('bitter-gourd', 'Bitter Gourd'),
        getFoodChoice('cabbage', 'Cabbage'),
        getFoodChoice('cauliflower', 'Cauliflower'),
        getFoodChoice('ladies-finger', 'Ladies Finger'),
        getFoodChoice('pumpkin', 'Pumpkin')
    ]
    FRUIT = [
        getFoodChoice('apple', 'Apple'), 
        getFoodChoice('banana', 'Banana'), 
        getFoodChoice('litchi', 'Litchi'), 
        getFoodChoice('mango', 'Mango'), 
        getFoodChoice('orange', 'Orange')
    ]
    FOOD_CHOICES = (
        (getFoodChoice('bitter-gourd', 'Bitter Gourd'), __('Bitter Gourd')),
        (getFoodChoice('cabbage', 'Cabbage'), __('Cabbage')),
        (getFoodChoice('cauliflower', 'Cauliflower'), __('Cauliflower')),
        (getFoodChoice('ladies-finger', 'Ladies Finger'), __('Ladies Finger')),
        (getFoodChoice('pumpkin', 'Pumpkin'), __('Pumpkin')),
        (getFoodChoice('apple', 'Apple'), __('Apple')),
        (getFoodChoice('banana', 'Banana'), __('Banana')),
        (getFoodChoice('litchi', 'Litchi'), __('Litchi')),
        (getFoodChoice('mango', 'Mango'), __('Mango')),
        (getFoodChoice('orange', 'Orange'), __('Orange')),
    )
    QUANTITY = ['kg', '250gm', '200gm', '500gm', '2kg', '5kg', '10kg', '25kg', '50kg', 'quintal']
    QUANTITY_CHOICES = (
        ('kg', __('1 kg')),
        ('250gm', __('250 gm')),
        ('200gm', __('200 gm')),
        ('500gm', __('500 gm')),
        ('2kg', __('2 kg')),
        ('5kg', __('5 kg')),
        ('10kg', __('10 kg')),
        ('25kg', __('25 kg')),
        ('50kg', __('50 kg')),
        ('quintal', __('1 quintal')),
    )
    myuser = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)
    desc = models.TextField(verbose_name='Description')
    foodType = models.CharField(max_length=50, verbose_name='Food Type', choices=FOOD_CHOICES)
    price = models.BigIntegerField()
    quantity = models.CharField(max_length=30, choices=QUANTITY_CHOICES)
    phone2 = models.CharField(max_length=10, null=True)
    location = models.CharField(max_length=150, null=True)
    thumbnail = models.CharField(max_length=255, null=True)
    uploaded_at = models.DateTimeField(verbose_name='Uploaded At', auto_now=True)
    
    class Meta:
        ordering = ['-uploaded_at']

    def uploaded_time(self):
        return getUploadTimeDiff(self)

    def getUniversalDate(self):
        """ To use external function getUploadTimeDiff in every model, return datetime field of to be calculated
        date time """
        return self.uploaded_at
    
    def getEnglishOnlyFoodChoice(self):
        return self.foodType.split('_NE_')[0]

    def foodCategory(self):
        if self.foodType in Post.VEG:
            return Post.CATEGORIES[0]
        return Post.CATEGORIES[1]
        
    def outerFood(self):
        return self.get_foodType_display()

    def outerQuantity(self):
        return self.get_quantity_display()
        
    def priceToWeightRatio(self):
        return self.price/getWeightNumForCalc(self.quantity)

    def upload_date_nepali(self):
        upload_date = self.uploaded_at
        if current_language() == "ne":
            return samwat.from_ad(upload_date.date()).strftime("%dne %Bne, %Yne") 
        return upload_date.strftime("%b %d, %Y")

    def uploaded_datetime_nepali(self):
        upload_date = self.uploaded_at
        if current_language() == "ne":
            localdatetime = timezone.localtime(upload_date)
            upload_date = samwat.from_ad(upload_date.date()).strftime("%dne %Bne, %Yne") + f", {translate_num_eng_to_nep(str(localdatetime.time())[0:5])}"
        return upload_date
    
class Photo(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='photos')
    photos = models.ImageField(verbose_name='Photos', upload_to='post/', validators=[file_size, FileExtensionValidator(['jpg', 'jpeg', 'png',])], null=True, blank=True)

    def default_path(self):
        return f"post/default/{self.post.foodType.split('_NE_')[0]}.jpg"

    def null_save(self, *args, **kwargs):
        default_img = self.default_path()
        self.photos = default_img
        super(Photo, self).save(*args, **kwargs)  
        post_thumbnail = Post(pk=self.post.id)
        post_thumbnail.thumbnail = default_img
        post_thumbnail.save(update_fields=['thumbnail'])
        
    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)  
        return image_crop(self)
    
    def get_image(self):
        return self.photos.path    

class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ('photos', )

class PostView(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='post_views')
    user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, related_name='user_views')
    def __str__(self):
        return str(self.user.id)

class Comment(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comment')
    myuser = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField(verbose_name='Comment', null=False)
    editted = models.BooleanField(default=False)
    commented_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def uploaded_time(self):
        output = getUploadTimeDiff(self, isComment=True)
        return output

    def uploaded_time_for_notif(self):
        output = getUploadTimeDiff(self, longStatus=True)
        return output

    def getUniversalDate(self):
        """ To use external function getUploadTimeDiff in every model, return datetime field of to be calculated
        date time """
        return self.commented_at

    def get_last_two(self):
        try:
            return self.reply.all()[:2]
        except:
            pass

    def comment_for_notif(self):
        return getSlicedNotificationMessages(self.text)

class Reply(models.Model):
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, related_name='reply')
    myuser = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, related_name='reply')
    text = models.TextField(verbose_name='Reply', null=False)
    replied_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def uploaded_time(self):
        output = getUploadTimeDiff(self, isComment=True)
        return output
        
    def uploaded_time_for_notif(self):
        output = getUploadTimeDiff(self, longStatus=True)
        return output

    def getUniversalDate(self):
        """ To use external function getUploadTimeDiff in every model, return datetime field of to be calculated
        date time """
        return self.replied_at
    
    def reply_for_notif(self):
        return getSlicedNotificationMessages(self.text)
