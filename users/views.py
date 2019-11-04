from django.shortcuts import render, redirect
from . import models as u_models
from posts import models as p_models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
import urllib
# import urllib2
import json
from django.db import connection

# Create your views here.


def log_login(user):
    user_profile = u_models.UserProfile.objects.get(user=user)
    try:
        log_object = u_models.LoginLog.objects.get(user=user_profile)
        log_object.save()
    except:
        new = u_models.LoginLog(user=user_profile)
        new.save()


def Login(request):
    if request.user.is_authenticated:
        log_login(request.user)
        return redirect('profile')
    else:
        if request.method == 'POST':
            data = request.POST
            username = data['username']
            password = data['password']
            # print(username, password)
            user = authenticate(request, username=username, password=password)
            # print(user)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                user = request.user
                user_id = user.id
                user_object = User.objects.get(id=user_id)
                user_profile = u_models.UserProfile.objects.get(user=user)
                log_login(user)
                if user_profile.is_active == False:
                    user_profile.is_active = True
                    user_profile.save()
                    log_login(user)
                    return render(request, 'profile.html', {'data': 'Account has been reactivated'})
                else:
                    return redirect('profile')
            else:

                return redirect('login')
        else:
            return render(request, 'login212.html')


def Logout(request):
    logout(request)
    return redirect('login')


def Signup(request):
    if request.method == "POST":
        data = request.POST
        username = data['username']
        email = data['email']
        password = data['password']
        password1 = data['password1']
        dob = data['dob']
        contact = data['contact']
        if password != password1:
            return render(request, 'signup.html', {'error': "Passwords Don’t Match"})
        else:
            password_hashed = make_password(password)
            user = u_models.User(username=username, password=password_hashed)
            user.save()
            user_profile = u_models.UserProfile(
                user=user, birth_date=dob, contact=contact)
            user_profile.save()
            return redirect('login')
    else:
        return render(request, 'signup.html')


def Profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print("LOL", request.POST.keys())
            if 'view_followers' in request.POST.keys():
                print("VIEW FOLLOWERS")
                return redirect('followers', username=request.POST['username'])
            else:
                pass
            if 'view_following' in request.POST.keys():
                print("VIEW FOLLOWING")
                return redirect('following', username=request.POST['username'])
            else:
                pass
            if 'login' in request.POST.keys():
                return redirect('login')
            else:
                pass
            if 'logout' in request.POST.keys():
                return redirect('logout')
            else:
                pass
            if 'follow' or 'unfollow' in request.POST.keys():
                return redirect('profile')
            else:
                pass
            
    

        else:
            user = request.user
            user_profile = u_models.UserProfile.objects.get(user=user)
            user_profile_picture = user_profile.picture
            user_profile_picture_url = user_profile_picture.url
            user_pp_clean = user_profile_picture_url[7:]
            user = request.user
            # for every user's id in Django User Model the UserProfile has user's id +1
            user_id = user.id #changed
            cursor = connection.cursor()
            print(user_id)
            cursor.execute(
                'select count(user_follower_id) from users_following where user_following_id = {}'.format(user_profile.id))
            count_following = int((cursor.fetchone()[0]))  # 1 for test1
            print(count_following)
            cursor.execute(
                'select count(user_following_id) from users_following where user_follower_id = {}'.format(user_profile.id))
            count_follower = int((cursor.fetchone()[0]))
            # for i in count_
            return render(request, 'profile.html', {'User': user, 'UserProfile': user_profile, 'UserProfilePictureurl': user_pp_clean, 'count_follower': count_follower, 'count_following': count_following})
    else:
        print("SO SAD")
        return render(request, 'login212.html')


def UserProfile(request, username):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        current_user = request.user
        logged_in_user = u_models.UserProfile.objects.get(user=current_user)
        user = User.objects.get(username=username)
        followed_account = u_models.UserProfile.objects.get(user=user)
        # print(logged_in_user.user.username,followed_account.user.username, current_user.username)
        '''
        - get the User model object using the username from the html
        - get the UserProfile object using the User object
        - create the new Following object
        - save it
        '''
        if username != current_user.username:
            if "follow" in data.keys():
                '''
                user_following is the logged in user
                user_follower is the followed account
                '''

                try:
                    person = u_models.Following.objects.get(
                        user_following=logged_in_user, user_follower=followed_account)
                except:
                    add_follower = u_models.Following(
                        user_following=logged_in_user, user_follower=followed_account)
                    add_follower.save()
                    return redirect('userprofile', username=username)
            elif "unfollow" in data.keys():
                u_models.Following.objects.filter(
                    user_following=logged_in_user, user_follower=followed_account
                ).delete()
                return redirect('userprofile', username=username)
        else:
            redirect('profile')
    else:
        current_user = request.user
        logged_in_user = u_models.UserProfile.objects.get(user=current_user)
        user = User.objects.get(username=username)
        user_profile = u_models.UserProfile.objects.get(user=user)
        user_profile_picture = user_profile.picture
        user_profile_picture_url = user_profile_picture.url
        user_pp_clean = user_profile_picture_url[7:]
        user_posts = p_models.Post.objects.all().filter(user_profile=user_profile)
        following = u_models.Following.objects.all().filter(
            user_following=logged_in_user, user_follower=user_profile)
        # for every user's id in Django User Model the UserProfile has user's id +1
        current_user_id = user.id #changed
        current_user_profile = u_models.UserProfile.objects.get(user=current_user)
        cursor = connection.cursor()
        # print(user_id)
        cursor.execute(
            'select count(user_follower_id) from users_following where user_following_id = {}'.format(current_user_profile.id,))
        count_following = int((cursor.fetchone()[0]))  # 1 for test1
        # print(count_following)
        cursor.execute(
            'select count(user_following_id) from users_following where user_follower_id = {}'.format(current_user_profile.id))
        count_follower = int((cursor.fetchone()[0]))
        # for i in count_
        if following is None:
            return render(request, 'profile.html', {'User': user, 'UserProfile': user_profile, 'UserProfilePictureurl': user_pp_clean, 'count_follower': count_follower, 'count_following': count_following, 'following': ''})
        # print(user_post.user_profile.picture.url, user_pp_clean)
        return render(request, 'profile.html', {'User': user, 'UserProfile': user_profile, 'UserProfilePictureurl': user_pp_clean, 'count_follower': count_follower, 'count_following': count_following, 'following': following})


def Settings(request):
    user = request.user
    user_id = user.id
    user_object = User.objects.get(id=user_id)
    print(user_object.password)
    user_profile = u_models.UserProfile.objects.get(user=user)
    if request.method == 'POST':
        data = request.POST

        if 'change_username' in data.keys():
            new_username = data['username']
            try:
                new_user = u_models.UserProfile.objects.get(
                    username=new_username)
                if new_user is not None:
                    return render(request, 'settings.html', {"username_error": "Username already exists."})
            except:
                user_object.username = new_username
                user_object.save()

                return redirect('settings')
        if 'change_pp' in data.keys():
            print(request.POST)
            new_image = request.FILES.get('image', False)
            user_profile.picture = new_image
            user_profile.save()
            return redirect('settings')

        if 'change_password' in data.keys():
            new_password = data['newpwd']
            new_password1 = data['newpwd1']
            if new_password == new_password1:
                old_password = data['oldpwd']
                # print(new_password, new_password1, old_password)
                if check_password(old_password, user_object.password):
                    new_password_hashed = make_password(new_password)
                    user_object.password = new_password_hashed
                    user_object.save()
                    return redirect('login')
                    # return render(request, 'settings.html', {'password_error': 'Current password entered is wrong.'})

                else:
                    return render(request, 'settings.html', {'password_error': 'Current password entered is wrong.'})
            else:
                return render(request, 'settings.html', {'password_error': 'Passwords dont match.'})
        if "deactivate_account" in data.keys():
            old_passworddeactiv = data['deactivate_password']
            if check_password(old_passworddeactiv, user_object.password):
                user_profile.is_active = False
                user_profile.save()
                return redirect('logout')
            else:
                return render(request, 'settings.html', {'password_error': 'Current password entered is wrong.'})
        if "delete_account" in data.keys():
            old_passworddelete = data['delete_password']
            if check_password(old_passworddelete, user_object.password):
                user_object.delete()
            return redirect('login')

    else:
        user = request.user
        user_profile = u_models.UserProfile.objects.get(user=user)
        user_profile_picture = user_profile.picture
        user_profile_picture_url = user_profile_picture.url
        user_pp_clean = user_profile_picture_url[7:]
        # print(user_profile_picture.user.user.username,user_profile_picture.image.url)
        return render(request, 'settings.html', {'User': user, 'UserProfile': user_profile, 'UserProfilePictureurl': user_pp_clean})


def Search(request):
    if request.method == 'POST':
        data = request.POST
        if 'search' in data.keys():
            search_username = data['search']

            # get_all_usernames = 'select username from auth_user where username like "{}%"'.format(search_username,)
            # all_users = u_models.User.objects.raw(get_all_usernames)

            cursor = connection.cursor()
            cursor.execute(
                'select id from auth_user where username like "{}%"'.format(search_username,))
            all_users = cursor.fetchall()
            all_user_ids = []
            for i in all_users:
                for j in i:
                    all_user_ids.append(j)

            all_user_ids = tuple(all_user_ids)  # ('facepalm','fac','faculty')
            # print(all_user_ids)
            if len(all_user_ids) == 1:
                id_of_one = int(all_user_ids[0])
                all_user_profiles = u_models.UserProfile.objects.raw(
                    "select * from users_userprofile where user_id = {}".format(id_of_one))
            else:
                all_user_profiles = u_models.UserProfile.objects.raw(
                    "select * from users_userprofile where user_id in {}".format(all_user_ids))
            '''for i in all_user_profiles:
                print(i.user.username)
                print(i.birth_date)'''

            # NEED TO GET THE INFO IF THE SEARCHED USER IS FOLLOWED BY LOGGED IN USER
            user = u_models.User.objects.get(id=request.user.id)
            user_profile = u_models.UserProfile.objects.get(user=user)
            cursor.execute(
                'select user_follower_id from users_following where user_following_id = {}'.format(user_profile.id,))
            following_users = cursor.fetchall()
            following_user_ids = []
            for i in following_users:
                following_user_ids.append(i[0])
            following_user_ids = tuple(following_user_ids)

            # print(following_user_ids)
            return render(request, 'search.html', {'users': all_user_profiles, 'following_users': following_user_ids})
        else:
            current_user = request.user
            logged_in_user = u_models.UserProfile.objects.get(
                user=current_user)
            username = data['username']
            user = User.objects.get(username=username)
            followed_account = u_models.UserProfile.objects.get(user=user)
            if username != current_user.username:
                if "follow" in data.keys():
                    '''
                    user_following is the logged in user
                    user_follower is the followed account
                    '''

                    try:
                        person = u_models.Following.objects.get(
                            user_following=logged_in_user, user_follower=followed_account)
                    except:
                        add_follower = u_models.Following(
                            user_following=logged_in_user, user_follower=followed_account)
                        add_follower.save()
                        return redirect('userprofile', username=username)
                elif "unfollow" in data.keys():
                    u_models.Following.objects.filter(
                        user_following=logged_in_user, user_follower=followed_account
                    ).delete()
                    return redirect('userprofile', username=username)
    else:
        return render(request, 'search.html')

def Following(request,username):
    if request.method == 'POST':
        data = request.POST
        current_user = request.user
        logged_in_user = u_models.UserProfile.objects.get(
            user=current_user)
        username = data['username']
        user = User.objects.get(username=username)
        followed_account = u_models.UserProfile.objects.get(user=user)
        if username != current_user.username:
            if "follow" in data.keys():
                '''
                user_following is the logged in user
                user_follower is the followed account
                '''

                try:
                    person = u_models.Following.objects.get(
                        user_following=logged_in_user, user_follower=followed_account)
                except:
                    add_follower = u_models.Following(
                        user_following=logged_in_user, user_follower=followed_account)
                    add_follower.save()
                    return redirect('userprofile', username=username)
            elif "unfollow" in data.keys():
                u_models.Following.objects.filter(
                    user_following=logged_in_user, user_follower=followed_account
                ).delete()
                return redirect('userprofile', username=username)
    else:
        current_user = request.user
        logged_in_user = u_models.UserProfile.objects.get(
            user=current_user)
        cursor = connection.cursor()
        cursor.execute(
            'select user_follower_id from users_following where user_following_id = %s', (logged_in_user.id,))
        loggedin_user_following = cursor.fetchall()
        loggedin_user_following_ids = []
        for i in loggedin_user_following:
            loggedin_user_following_ids.append(i[0])
        loggedin_user_following_ids = tuple(loggedin_user_following_ids)
        user_object = User.objects.get(username=username)
        user_profile = u_models.UserProfile.objects.get(user=user_object)
        print(user_object.id)
        cursor.execute(
                'select user_follower_id from users_following where user_following_id = %s', (user_profile.id,))
        following_users = cursor.fetchall()
        following_user_ids = []
        for i in following_users:
            following_user_ids.append(i[0])
        following_user_ids = tuple(following_user_ids)
        print(following_user_ids)
        
        if len(following_user_ids) == 1:
            id_of_one = int(following_user_ids[0])
            following_user_profiles = u_models.UserProfile.objects.raw('select * from users_userprofile where id = {}'.format(id_of_one,))
        else:
            following_user_profiles = u_models.UserProfile.objects.raw('select * from users_userprofile where id in {}'.format(following_user_ids,))
        return render(request, 'view_accounts.html', {'users': following_user_profiles, 'following_users':loggedin_user_following_ids})
    # get user profiles whom user is following


def Followers(request,username):
    if request.method == 'POST':
        data = request.POST
        current_user = request.user
        logged_in_user = u_models.UserProfile.objects.get(
            user=current_user)
        username = data['username']
        user = User.objects.get(username=username)
        followed_account = u_models.UserProfile.objects.get(user=user)
        if username != current_user.username:
            if "follow" in data.keys():
                '''
                user_following is the logged in user
                user_follower is the followed account
                '''

                try:
                    person = u_models.Following.objects.get(
                        user_following=logged_in_user, user_follower=followed_account)
                except:
                    add_follower = u_models.Following(
                        user_following=logged_in_user, user_follower=followed_account)
                    add_follower.save()
                    return redirect('userprofile', username=username)
            elif "unfollow" in data.keys():
                u_models.Following.objects.filter(
                    user_following=logged_in_user, user_follower=followed_account
                ).delete()
                return redirect('userprofile', username=username)
    else:
        current_user = request.user
        logged_in_user = u_models.UserProfile.objects.get(
            user=current_user)
        cursor = connection.cursor()
        cursor.execute(
            'select user_follower_id from users_following where user_following_id = %s',(logged_in_user.id,))
        loggedin_user_following = cursor.fetchall()
        loggedin_user_following_ids = []
        for i in loggedin_user_following:
            loggedin_user_following_ids.append(i[0])
        loggedin_user_following_ids = tuple(loggedin_user_following_ids)
        user_object = User.objects.get(username=username)
        user_profile = u_models.UserProfile.objects.get(user=user_object)
        print(user_object.id)
        cursor.execute(
                'select user_following_id from users_following where user_follower_id = %s',(user_profile.id,))
        follower_users = cursor.fetchall()
        follower_user_ids = []
        for i in follower_users:
            follower_user_ids.append(i[0])
        follower_user_ids = tuple(follower_user_ids)
        print(follower_user_ids)
        if len(follower_user_ids) == 1:
            id_of_one = int(follower_user_ids[0])
            follower_user_profiles = u_models.UserProfile.objects.raw('select * from users_userprofile where id = {}'.format(id_of_one,))
        else:
            follower_user_profiles = u_models.UserProfile.objects.raw('select * from users_userprofile where id in {}'.format(follower_user_ids,))
        return render(request, 'view_accounts.html', {'users': follower_user_profiles,'following_users':loggedin_user_following_ids})
    # get user profiles whom user is followed by

    # facepalm0069@gmail.com
    # pwd=samshnik
    # https://www.freenom.com/en/freeandpaiddomains.html


# if_following = select user_follower_id from users_following where user = (user_id)
