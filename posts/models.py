from django.db import models
from django.forms import ModelForm
from join.models import MyUser
from django.core.validators import FileExtensionValidator
from frutonp.utils import file_size, image_crop, getUploadTimeDiff, getWeightNumForCalc
from datetime import timedelta
from django.utils import timezone

class Post(models.Model):
    VEG = ['bitter-gourd', 'cabbage', 'cauliflower', 'ladies-finger', 'pumpkin']
    FRUIT = ['apple', 'banana', 'litchi', 'mango', 'orange']
    FOOD_CHOICES = (
        ('apple', 'Apple'),
        ('banana', 'Banana'),
        ('litchi', 'Litchi'),
        ('mango', 'Mango'),
        ('orange', 'Orange'),
        ('bitter-gourd', 'Bitter Gourd'),
        ('cabbage', 'Cabbage'),
        ('cauliflower', 'Cauliflower'),
        ('ladies-finger', 'Ladies Finger'),
        ('pumpkin', 'Pumpkin'),
    )
    QUANTITY = ['kg', '250gm', '200gm', '500gm', '2kg', '5kg', '10kg', '25kg', '50kg', 'quintal']
    QUANTITY_CHOICES = (
        ('kg', '1 kg'),
        ('250gm', '250 gm'),
        ('200gm', '200 gm'),
        ('500gm', '500 gm'),
        ('2kg', '2 kg'),
        ('5kg', '5 kg'),
        ('10kg', '10 kg'),
        ('25kg', '25 kg'),
        ('50kg', '50 kg'),
        ('quintal', '1 quintal'),
    )
    EXPIRE = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
    EXPIRE_CHOICES = (
        ('1', '1 day'),
        ('2', '2 days'),
        ('3', '3 days'),
        ('4', '4 days'),
        ('5', '5 days'),
        ('6', '6 days'),
        ('7', '7 days'),
        ('8', '8 days'),
        ('9', '9 days'),
        ('10', '10 days'),
        ('10', '10 days'),
        ('11', '11 days'),
        ('12', '12 days'),
        ('13', '13 days'),
        ('14', '14 days'),
        ('15', '15 days'),
    )
    myuser = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    desc = models.TextField(verbose_name='Description')
    foodType = models.CharField(max_length=50, verbose_name='Food Type', choices=FOOD_CHOICES)
    price = models.BigIntegerField()
    quantity = models.CharField(max_length=30, choices=QUANTITY_CHOICES)
    expire = models.CharField(null=True, max_length=10, choices=EXPIRE_CHOICES, default='10')
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

    def outerFood(self):
        return self.get_foodType_display()
        
    def priceToWeightRatio(self):
        return self.price/getWeightNumForCalc(self.quantity)
    
class Photo(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='photos')
    photos = models.ImageField(verbose_name='Photos', upload_to='post/', validators=[file_size, FileExtensionValidator(['jpg', 'jpeg', 'png',])], null=True, blank=True)

    def default_path(self):
        return f"post/default/{self.post.foodType}.jpg"

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

    def uploaded_time(self):
        output = getUploadTimeDiff(self, isComment=True)
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

class Reply(models.Model):
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, related_name='reply')
    myuser = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, related_name='reply')
    text = models.TextField(verbose_name='Reply', null=False)
    replied_at = models.DateTimeField(auto_now=True)

    def uploaded_time(self):
        output = getUploadTimeDiff(self, isComment=True)
        return output

    def getUniversalDate(self):
        """ To use external function getUploadTimeDiff in every model, return datetime field of to be calculated
        date time """
        return self.replied_at
