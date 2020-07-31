from django.contrib import admin
from .models import firstModel
from .models import userModel
from .models import postModel
from .models import commentModel
from .models import categoryModel
from .models import messagesModel

# Register your models here.
admin.site.register(firstModel)
admin.site.register(userModel)
admin.site.register(postModel)
admin.site.register(commentModel)
admin.site.register(categoryModel)
admin.site.register(messagesModel)