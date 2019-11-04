from django.shortcuts import render, redirect
from users import models as u_models
from . import models as p_models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import connection

import datetime
# Create your views here.


'''def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        row = cursor.fetchone()

    return row


def get_records(query, *args):
    cursor = connection.cursor()
    cursor.execute(query, args)
    return cursor.fetchall()'''


@login_required
def Post(request):
    if request.method == 'POST':
        user = request.user
        user_id = user.id
        user_object = User.objects.get(id=user_id)
        user_profile = u_models.UserProfile.objects.get(user=user)
        data = request.POST
        posttype = data['posttype']
        posttopic = data['posttopic']
        text = data['text']
        header = data['header']
        link = data['link']
        # image = data['image']
        new_post = p_models.Post(user_profile=user_profile, header=header, text=text,
                                 link=link, post_type=posttype, post_topic=posttopic)
        new_post.save()
        return redirect('home')

    else:
        return render(request, 'post.html')


@login_required
def Feed(request):
    user = request.user
    user_id = user.id # was -1
    print(user_id)
    user_profile = u_models.UserProfile.objects.get(user=user)
    user_posts = p_models.Post.objects.all().filter(user_profile=user_profile)

    # getting the timestamp of last log in by user
    '''login_timestamp_object = u_models.LoginLog.objects.get(user=user_profile)
    login_timestamp = str(login_timestamp_object.timestamp)
    current_timestamp = str(timezone.now())
    get_all_followers = 'select user_following from users_following where user_follower = "%s"'
    print(login_timestamp, current_timestamp)
    # all the users that this user follows
    following_accounts = u_models.Following.objects.raw(
        'select user_following_id from users_following where user_follower_id = "%s', [user_id])
    # following account posts

    get_all_posts = 'select * from posts_post where (user_profile in {following_accounts}) and (timestamp between {last_logged_in} and {current_time}) order by timestamp'.format(
        following_accounts=following_accounts, last_logged_in=login_timestamp, current_time=timezone.now())'''
    login_timestamp_object = u_models.LoginLog.objects.get(user=user_profile)
    login_timestamp = str(login_timestamp_object.timestamp)
    current_timestamp = str(timezone.now())
    cursor = connection.cursor()
    cursor.execute(
        'SELECT  user_follower_id FROM users_following where user_following_id in (%s)' % (user_id,))
    res = cursor.fetchall()
    following_account_id = []
    for i in res:
        for j in i:
            following_account_id.append(j)

    following_account_id = tuple(following_account_id)
    print(following_account_id)
    '''print(following_account_id)
    if login_timestamp[:11] == current_timestamp[:11]:
        q = "select * from posts_post where(user_profile_id in {}) and (timestamp between '2019-09-22 16:08:44.904824+00:00' and '{}') order by timestamp".format(
            following_account_id, current_timestamp)
        cursor.execute(q)
        posts = cursor.fetchall()
        print(posts)
    else:
        q = "select * from posts_post where(user_profile_id in {}) and (timestamp between '{}' and '{}') order by timestamp".format(
            following_account_id, login_timestamp, current_timestamp)
        cursor.execute(q)
        posts = cursor.fetchall()
        followers_posts = {}
        for post in posts:
            pass'''
    login_date = login_timestamp[:11]
    current_date = current_timestamp[:11]
    if login_date == current_date:
        q = "select * from posts_post where(user_profile_id in {}) and (timestamp between DATE_SUB('{}', INTERVAL -1 DAY) and '{}') order by timestamp desc".format(
            following_account_id, login_timestamp, current_timestamp)
        following_ppl_posts = p_models.Post.objects.raw(q)
    else:
        q = "select * from posts_post where(user_profile_id in {}) and (timestamp between '{}' and '{}') order by timestamp desc".format(
            following_account_id, login_timestamp, current_timestamp)
        following_ppl_posts = p_models.Post.objects.raw(q)
    
    for i in following_ppl_posts:
        print(i.header)
    try:
        return render(request, 'home.html', {'posts': user_posts, 'followers_posts': following_ppl_posts})
    except:
        error = "You are upto date"
        return render(request, 'home.html', {'error': error})
    
