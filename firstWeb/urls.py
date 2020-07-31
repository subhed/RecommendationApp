"""firstWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from firstApp.views import homePageView
from firstApp.views import loginCheck
from firstApp.views import registerView
from firstApp.views import wallPageView
from firstApp.views import logout
from firstApp.views import postCheck
from firstApp.views import commentCheck
from firstApp.views import postDelete
from firstApp.views import commentDelete
from firstApp.views import commentLike
from firstApp.views import commentDisLike



from firstApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homePageView, name='Home'),
    path('login/', loginCheck, name='Login'),
    path('register/', registerView, name='Register'),
    path('registerCheck/', registerView, name='Register Check'),
    path('postCheck/', views.postCheck, name='Post Check'),
    path('postDelete/', postDelete, name='Post Delete'),
    path('home/<str:category>/', views.wallPageView_cat, name=''),
    path('commentCheck/', commentCheck, name='Comment Check'),
    path('commentDelete/', commentDelete, name='Comment Delete'),
    path('commentLike/', commentLike, name='Comment Like'),
    path('commentDisLike/', commentDisLike, name='Comment Dislike'),
    path('loginCheck/', loginCheck, name='Login Check'),
    path('home/', wallPageView, name='Home'),
    path('logout/', logout, name='Home'),
    path('chat/', views.chatIndex, name='Chat Index'),
    path('chat/<str:room_name>/', views.room, name='room'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
