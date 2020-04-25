from django.db import models
from django.forms import ModelForm
from join.models import MyUser
from django.core.validators import FileExtensionValidator
from frutonp.utils import file_size, add_photo_default, image_crop, getUploadTimeDiff
from datetime import timedelta
from django.utils import timezone

VEG = ['bitter-gourd', 'cabbage', 'cauli', 'ladies-finger', 'pumpkin']
FRUIT = ['apple', 'banana', 'litchi', 'mango', 'orange']
outerFoodType = {
    # Fruits
    'apple': 'Apple',
    'banana': 'Banana',
    'litchi': 'Litchi',
    'mango': 'Mango',
    'orange': 'Orange',
    # Vegetables
    'bitter-gourd': 'Bitter Gourd',
    'cabbage': 'Cabbage',
    'cauli': 'Cauliflower',
    'ladies-finger': 'Ladies Finger',
    'pumpkin': 'Pumpkin',
}

class Post(models.Model):
    myuser = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    desc = models.TextField(verbose_name='Description')
    foodType = models.CharField(max_length=30, verbose_name='Food Type')
    price = models.BigIntegerField()
    quantity = models.CharField(max_length=30)
    expire = models.DateTimeField(null=True)
    phone2 = models.CharField(max_length=10, null=True)
    location = models.CharField(max_length=150, null=True)
    thumbnail = models.CharField(max_length=255, null=True)
    uploaded_at = models.DateTimeField(verbose_name='Uploaded At', auto_now=True)
    category = models.CharField(max_length=20, null=True)

    def save(self, *args, **kwargs):
        self.category = self.getCategory()
        super(Post, self).save(*args, **kwargs)

    def getCategory(self):
        """ Return category of foodType either vegetable or fruit

            @return: string "vegetable" or "fruit"        
        """
        return self.foodType in VEG and "vegetable" or "fruit"
    
    def uploaded_time(self):
        return getUploadTimeDiff(self)

    def getUniversalDate(self):
        """ To use external function getUploadTimeDiff in every model, return datetime field of to be calculated
        date time """
        return self.uploaded_at

    def outerFood(self):
        return outerFoodType[self.foodType]
    

class Photo(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='photos')
    photos = models.ImageField(verbose_name='Photos', upload_to='post/', validators=[file_size, FileExtensionValidator(['jpg', 'jpeg', 'png',])], null=True, blank=True)

    def null_save(self, *args, **kwargs):
        default_img = add_photo_default(self.post.foodType)
        self.photos = default_img
        super(Photo, self).save(*args, **kwargs)  
        # Add thumbnail after photo is saved
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
