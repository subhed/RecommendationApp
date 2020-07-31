
from django.db import models


class firstModel(models.Model):
    sender = models.CharField(max_length=200)
    receiver = models.CharField(max_length=200)
    message = models.TextField()
    last_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender
        self.fields['myfield'].widget.attrs.update({'class': 'form-control'})


class userModel(models.Model):
    f_name = models.CharField(max_length=200)
    l_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    password = models.TextField()
    password2 = models.TextField()
    last_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
        self.fields['myfield'].widget.attrs.update(
            {'class': 'form-control mb-4'})

class postModel(models.Model):
    postId = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=200)
    user = models.ForeignKey('userModel', on_delete=models.CASCADE)
    post_message = models.TextField()
    location = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200)
    image = models.ImageField(upload_to='uploads/', blank=True)
    last_modified = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.postId)
        self.fields['myfield'].widget.attrs.update({'class': 'form-control'})
        self.fields['location'].required=False


class commentModel(models.Model):
    commentId = models.AutoField(primary_key=True)
    postId = models.ForeignKey('postModel', on_delete=models.CASCADE)
    userId = models.ForeignKey('userModel', on_delete=models.CASCADE)
    user = models.CharField(max_length=200)
    comment_message = models.TextField()
    likes = models.IntegerField(null=True, blank=True,default='0') 
    dislike = models.IntegerField(null=True, blank=True,default='0') 
    last_modified = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.commentId)
        self.fields['myfield'].widget.attrs.update({'class': 'form-control'})


class categoryModel(models.Model):
    catId = models.AutoField(primary_key=True)
    category = models.CharField(max_length=200)
    last_modified = models.DateTimeField(auto_now_add=True)
    posts = models.IntegerField(null=True, blank=True,default='0') 

    def __str__(self):
        return self.category
        self.fields['myfield'].widget.attrs.update(
            {'class': 'form-control mb-4'})



class messagesModel(models.Model):
    mId = models.AutoField(primary_key=True)
    message = models.CharField(max_length=500)
    userId = models.ForeignKey('userModel', on_delete=models.CASCADE)
    catId = models.ForeignKey('categoryModel', on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
    def last_30_messages(self):
        return messagesModel.objects.order_by('-last_modified').all()[:30]


