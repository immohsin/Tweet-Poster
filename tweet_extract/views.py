import os
import json
import oauth2
import facebook

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect


from tweet_extract.form import TweetInputForm, LoginForm


@login_required(login_url='/login/')
def extract_tweet(request):
    try:
        para = []
        if request.method == 'GET':
            form = TweetInputForm()
        else:
            form = TweetInputForm(request.POST)

            if form.is_valid():
                tweet_id, counter = form.cleaned_data['tweet_id']
                consumer = oauth2.Consumer(key=os.environ.get('CONSUMER_KEY'), secret=os.environ.get('CONSUMER_SECRET'))
                token = oauth2.Token(key=os.environ.get('ACCESS_KEY'), secret=os.environ.get('ACCESS_SECRET'))
                client = oauth2.Client(consumer, token)
                for tweet in range(counter):
                    resp, content = client.request(settings.TWITTER_URL.format(int(tweet_id[tweet])), method='GET')
                    data = json.loads(content)
                    tweet_message = data['full_text']
                    para.append(tweet_message)
                    graph = facebook.GraphAPI(access_token=os.environ.get('Page_ACCESS_KEY'))
                    graph.put_object("page id", "feed", message=para)
                    messages.success(request, "Successfully posted to facebook")
        return render(request, 'tweet_extract/tweet_extractor.html', {'form': form})
    except Exception:
        return render(request, 'tweet_extract/error.html')
    
    
def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
            else:
                messages.error(request, 'username or password not correct')
    else:
        login_form = LoginForm()
    return render(request, 'tweet_extract/login.html', {'form': login_form})