from django.shortcuts import render
from django.http import HttpResponse
from .forms import firstForm
from .models import firstModel
from django.core import serializers
from django.http import JsonResponse
from .forms import userForm
from .models import userModel
from django.contrib.auth.forms import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import postModel
from .forms import postForm
from .models import commentModel
from django.db.models import F
from django.shortcuts import get_object_or_404
from .models import categoryModel
from .models import messagesModel
from django.db.models import Q


def homePageView(request):
    return render(request, 'index.html', {'name': 'ReCom'})


def wallPageView(request):
    if 'email' not in request.session:
        return render(request, 'login.html', {'name': 'Login'})

    session_email = request.session['email']
    entries = postModel.objects.all().order_by('-last_modified')
    comments = commentModel.objects.all().order_by('-last_modified')
    cat_list = categoryModel.objects.all()

    print(entries.count())
    print(comments)
    form_param = {}
    form_param['form'] = postForm()
    user1 = userModel.objects.filter(email=session_email)
    return render(request, 'body.html', {'name': 'ReCom Home', 'user': user1, 'form': form_param, 'posts': entries, 'comments': comments, 'category': 'General', 'catList': cat_list})


def wallPageView_cat(request, category):
    if 'email' not in request.session:
        return render(request, 'login.html', {'name': 'Login'})

    print(category)

    if category == 'General':
        return HttpResponseRedirect("/home/")

    entries_check = categoryModel.objects.filter(category=category).count()

    if entries_check == 0:
        return HttpResponseRedirect("/home/")

    cat_id = categoryModel.objects.filter(category=category)[0].catId
    session_email = request.session['email']
    entries = postModel.objects.filter(
        category=cat_id).order_by('-last_modified')
    comments = commentModel.objects.all().order_by('-last_modified')
    cat_list = categoryModel.objects.all()

    print(entries)
    print(comments)
    form_param = {}
    form_param['form'] = postForm()
    user1 = userModel.objects.filter(email=session_email)
    return render(request, 'body.html', {'name': 'ReCom Home', 'user': user1, 'form': form_param, 'posts': entries, 'comments': comments, 'category': category, 'catList': cat_list})


def registerView(request):

    form_param = {}
    form = userForm(request.POST)

    if 'email' not in request.POST:
        form_param = {}
        form_param['form'] = userForm()
        return render(request, 'register.html', {'name': 'Register', 'form': form_param})

    if form.is_valid():
        print(request.POST['email'])
        entryCheck = userModel.objects.filter(
            email=request.POST['email']).count()

        if request.POST['password'] != request.POST['password2']:
            form_param = {}
            form_param['form'] = userForm()
            return render(request, 'register.html', {'name': 'Register', 'form': form_param, 'response': 'password'})
        elif entryCheck == 0:
            form.save()
            form_param = {}
            form_param['form'] = userForm()
            return render(request, 'register.html', {'name': 'Register', 'form': form_param, 'response': 'success'})
    else:
        form_param = {}
        form_param['form'] = userForm()
        return render(request, 'register.html', {'name': 'Register', 'form': form_param, 'response': 'email'})


def postCheck(request):

    form_param = {}
    form = postForm(request.POST, request.FILES or None)

    user1 = userModel.objects.get(email=request.session['email'])

    catIdInt = request.POST['category']
    check = 0
    # entries_check = categoryModel.objects.filter(catId=request.POST['category']).count()
    print(catIdInt)
    try:
        val = int(catIdInt)
    except ValueError:
        print("That's not an int!")
        check = 1

    if check == 1:
        catInstance = categoryModel.objects.create(
            category=request.POST['category'], posts=0)
        catIdInt = catInstance.pk
        print('Setting')

    if not 'image' in request.FILES:
        foo_instance = postModel.objects.create(
            user_name=user1.f_name+' '+user1.l_name, user=user1, post_message=request.POST['post_message'], location=request.POST['location'], category=catIdInt)
    else:
        print(request.FILES['image'])
        foo_instance = postModel.objects.create(
            user_name=user1.f_name+' '+user1.l_name, user=user1, post_message=request.POST['post_message'], location=request.POST['location'], category=catIdInt, image=request.FILES['image'])

    # if form.is_valid():
    #     print(request.GET['location'])
    #     form.save()
    # else:
    #     print(form.errors)
    image_id = postModel.objects.get(pk=foo_instance.pk)

    form_param = {}
    form_param['form'] = postForm()

    if not image_id.image:
        return JsonResponse({'postId': foo_instance.pk, 'image': ' '})

    else:
        return JsonResponse({'postId': foo_instance.pk, 'image': image_id.image.url})


def commentCheck(request):

    form_param = {}
    form = postForm(request.GET or None)

    user1 = userModel.objects.get(email=request.session['email'])
    post1 = postModel.objects.get(postId=request.GET['post_id'])

    print(request.GET['comment_message'])
    foo_instance = commentModel.objects.create(
        postId=post1, userId=user1, user=user1.f_name+' '+user1.l_name, comment_message=request.GET['comment_message'])
    print(foo_instance.pk)
    form_param = {}
    form_param['form'] = postForm()
    return JsonResponse({
        'name': user1.f_name+' '+user1.l_name, 'comment_message': request.GET['comment_message'], 'cmtId': foo_instance.pk
    })


def postDelete(request):

    user1 = userModel.objects.get(email=request.session['email'])
    print(user1)

    if request.method == 'POST':
        print(request.POST['postId'])
        postModel.objects.filter(pk=request.POST['postId']).delete()

    return JsonResponse({})


def commentDelete(request):

    user1 = userModel.objects.get(email=request.session['email'])
    print(user1)

    if request.method == 'POST':
        print(request.POST['cmtId'])
        commentModel.objects.filter(pk=request.POST['cmtId']).delete()

    return JsonResponse({})


def commentLike(request):

    if request.method == 'POST':
        print(request.POST['cmtId'])
        likes_count = commentModel.objects.get(pk=request.POST['cmtId']).likes
        cmt = commentModel.objects.filter(
            pk=request.POST['cmtId']).update(likes=likes_count+1)

    return JsonResponse({'newCount': likes_count+1})


def commentDisLike(request):

    if request.method == 'POST':
        print(request.POST['cmtId'])
        likes_count = commentModel.objects.get(
            pk=request.POST['cmtId']).dislike
        cmt = commentModel.objects.filter(
            pk=request.POST['cmtId']).update(dislike=likes_count+1)

    return JsonResponse({'newCount': likes_count+1})


def loginCheck(request):

    if request.method == 'POST':
        user = userModel.objects.filter(
            email=request.POST['email'], password=request.POST['password']).exists()

        if user == True:
            form_param = {}
            form_param['form'] = postForm()
            print(user)
            entries = postModel.objects.all().order_by('-last_modified')
            comments = commentModel.objects.all().order_by('-last_modified')
            user1 = userModel.objects.filter(
                email=request.POST['email'], password=request.POST['password'])
            request.session['email'] = request.POST['email']

            # foo_instance = commentModel.objects.create(postId=entries, userId='subhed@gmail.com',user='Jack', comment_message='Hie')
            # return render(request, 'body.html', {'name': 'ReCom Home', 'user': user1, 'form': form_param, 'posts': entries, 'comments': comments})

            return HttpResponseRedirect("/home/")

        else:
            return render(request, 'login.html', {'name': 'Login', 'response': 'not'})
    else:
        return render(request, 'login.html', {'name': 'Login'})


def logout(request):
    try:
        del request.session['email']
    except:
        pass
    return render(request, 'logout.html', {'name': 'Logout'})


def chatIndex(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'user_name': request.session['email']
    })


def getMessage(request):
    if request.method == "POST":
        print(request.POST['roomName'])
        entries_check = categoryModel.objects.filter(
            category=request.POST['roomName']).count()
        if entries_check > 0:
            cat_id = categoryModel.objects.filter(
                category=request.POST['roomName'])[0].catId
            entries = messagesModel.objects.filter(
                catId=cat_id).order_by('-last_modified')[:10]
            r_entries = reversed(entries)

            return JsonResponse(serializers.serialize('json', r_entries), safe=False)
    return JsonResponse({'check': 'check'})


def chatRooms(request):
    entries_check = categoryModel.objects.all()[:10]
    return JsonResponse(serializers.serialize('json', entries_check), safe=False)


def search(request, location):
    if 'email' not in request.session:
        return render(request, 'login.html', {'name': 'Login'})

    session_email = request.session['email']
    entries = postModel.objects.filter(Q(location__contains=location) | Q(post_message__contains=location) ).order_by('-last_modified')
    comments = commentModel.objects.all().order_by('-last_modified')
    cat_list = categoryModel.objects.all()
    print(entries.count())
    print(comments)
    form_param = {}
    form_param['form'] = postForm()
    user1 = userModel.objects.filter(email=session_email)
    user_filter = userModel.objects.filter(email__contains=location).count()
    user_entries = userModel.objects.filter(Q(email__contains=location) | Q(f_name__contains=location) | Q(l_name__contains=location) )

    return render(request, 'search.html', {'name': 'ReCom Home', 'user': user1, 'form': form_param, 'posts': entries, 'comments': comments, 'category': 'General', 'catList': cat_list,'user_entries':user_entries})
  

def user(request, user):
    if 'email' not in request.session:
        return render(request, 'login.html', {'name': 'Login'})
    session_email = request.session['email']
    user1 = userModel.objects.filter(email=user)
    user1_pk = userModel.objects.filter(email=user)[0].pk
    entries = postModel.objects.filter(user=user1_pk).order_by('-last_modified')
    comments = commentModel.objects.all().order_by('-last_modified')
    cat_list = categoryModel.objects.all()
    return render(request, 'user.html', {'name': 'ReCom Home', 'user': user1, 'posts': entries, 'comments': comments, 'category': 'General', 'catList': cat_list})


