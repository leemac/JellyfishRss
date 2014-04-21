from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout

from rss.polling import sitepoller

from rss.models import Subscription
from rss.models import SubscriptionItem
from rss.models import User
from rss.models import SubscriptionUserRelation
from rss.models import Folder

import logging
import json

logger = logging.getLogger('logview.userrequest')

#-----BASIC

def home(request):
    context = RequestContext(request)

    if request.user.is_authenticated:
        user = User.objects.all()[0];
    else:
        logger.info("User made request (test logging)")

        from django.contrib.auth.forms import AuthenticationForm

        context['form'] = AuthenticationForm()

    return render_to_response('static/index.html', context_instance=context)


def about(request):
    return render_to_response('static/index.html')


def login_redirect(request):
    return render_to_response('static/login.html')


#-----API

# POST

def add_subscription(request):
    if (request.is_ajax()):
        user_id = request.POST["user_id"]
        subscription_url = request.POST["url"]

        existingSubscriptionCount = Subscription.objects.filter(url=subscription_url).count()

        # Only add and poll if it does not exist
        if existingSubscriptionCount == 0:
            poller = sitepoller.SitePoller()
            poller.add_site_and_poll(subscription_url)
        else:
            thisSubscription = Subscription.objects.get(url=subscription_url)
            existingRelation = SubscriptionUserRelation.objects.filter(user_id=user_id, subscription_id=thisSubscription.id)

            if existingRelation.exists():
                return HttpResponse(json.dumps("ok"), mimetype='application/json')

        # Get default folder
        existingFolderCount = Folder.objects.filter(user_id=user_id).count()

        if existingFolderCount == 0:
            folder = Folder()
            folder.title = "Feeds"
            folder.user_id = user_id
            folder.save()
        else:
            # TODO: for now...
            folder = Folder.objects.filter(user_id=user_id)[0];

        # Get subscription
        subscription = Subscription.objects.get(url=subscription_url)

        # Add relation
        relation = SubscriptionUserRelation()
        relation.folder_id = folder.id
        relation.user_id = user_id
        relation.subscription_id = subscription.id;
        relation.save()

        return HttpResponse(json.dumps("ok"), mimetype='application/json')

    return HttpResponse(json.dumps("Direct access is forbidden"), mimetype='application/json')


# GET

def get_subscription_items(request):
    # TODO: Filter this based on user's subscription
    if (request.is_ajax()):
        subscription_id = request.POST["subscription_id"]
        user_id = request.POST["user_id"]
        page_size = request.POST["page_size"]

        if int(subscription_id) == 0:

            subscription_ids = []

            for relation in SubscriptionUserRelation.objects.filter(user_id=user_id):
                subscription_ids.append(relation.subscription_id)

            itemset = SubscriptionItem.objects.filter(subscription_id__in=subscription_ids, is_read=False)
        else:
            subscriptions = Subscription.objects.get(id=subscription_id)
            itemset = subscriptions.item.filter(is_read=False)

        results = [ob.as_json() for ob in itemset.order_by('-published')[:page_size]]

        return HttpResponse(json.dumps(results), mimetype='application/json')

    return HttpResponse(json.dumps("Direct access is forbidden"), mimetype='application/json')


def get_folders(request):
    if (request.is_ajax()):
        user_id = request.POST["user_id"]

        folders = Folder.objects.filter(user_id=user_id)

        results = []

        # Could be replaced by built-in json in models
        for folder in folders.all():
            subscriptions = []

            for relation in SubscriptionUserRelation.objects.filter(folder_id=folder.id):
                subObj = {}
                subObj["title"] = relation.subscription.title
                subObj["id"] = relation.subscription.id
                subObj["favicon_url"] = relation.subscription.favicon_url
                subscriptions.append(subObj)

            folderObj = {}
            folderObj["title"] = folder.title
            folderObj["subscriptions"] = subscriptions

            results.append(folderObj)

        # TODO:

        # Need Structure like:

        # Folder A
        # -- Subscription 1
        # -- Subscription 2
        # Folder B
        # -- Subscription 3
        # Folder C
        # (...)

        return HttpResponse(json.dumps(results), mimetype='application/json')

    return HttpResponse(json.dumps("Direct access is forbidden"), mimetype='application/json')


# MISC

def mark_subscription_read(request):
    # TODO Need mechanism to properly mark the items 'as read'
    if (request.is_ajax()):
        subscription_id = request.POST["subscription_id"]

        if int(subscription_id) == 0:
            itemset = SubscriptionItem.objects.all().order_by('-published')

            for item in itemset:
                item.is_read = True
                item.save()

            itemset = SubscriptionItem.objects.filter(is_read=False).order_by('-published')
            results = [ob.as_json() for ob in itemset]

            return HttpResponse(json.dumps(results), mimetype='application/json')
        else:
            subscription = Subscription.objects.get(id=subscription_id)
            itemset = subscription.item.all().order_by('-published')

            for item in itemset:
                item.is_read = True
                item.save()

            itemset = subscription.item.filter(is_read=False).order_by('-published')
            results = [ob.as_json() for ob in itemset]

            return HttpResponse(json.dumps(results), mimetype='application/json')

    return HttpResponse(json.dumps("Direct access is forbidden"), mimetype='application/json')


def unsubscribe(request):
    if (request.is_ajax()):
        subscription_id = request.POST["subscription_id"]
        user_id = request.POST["user_id"]

        relations = SubscriptionUserRelation.objects.filter(subscription_id=subscription_id, user_id=user_id)

        for relation in relations:
            relation.delete()

        return HttpResponse(json.dumps("ok"), mimetype='application/json')

    return HttpResponse(json.dumps("Direct access is forbidden"), mimetype='application/json')


def change_subscription_color(request):
    if (request.is_ajax()):
        subscription_id = request.POST["subscription_id"]
        color = request.POST["color"]

        subscription = Subscription.objects.get(id=subscription_id)

        subscription.color = color

        subscription.save()

        return HttpResponse(json.dumps("ok"), mimetype='application/json')

    return HttpResponse(json.dumps("Direct access is forbidden"), mimetype='application/json')


#-----AUTHENTICATION

def login_user(request):
    logout(request)
    username = password = ""

    context = RequestContext(request)

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            logger.info("User " + username + " authenticated successfully.")
            if user.is_active:
                login(request, user)
                return render_to_response('static/login.html', context_instance=context)

    logger.info("Showing user index with login form....")

    from django.contrib.auth.forms import AuthenticationForm

    context['form'] = AuthenticationForm()

    return render_to_response('static/index.html', context_instance=context)


def logout_user(request):
    logout(request)

    context = RequestContext(request)
    return render_to_response('static/index.html', context_instance=context)