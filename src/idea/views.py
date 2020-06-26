from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime, random

from the_impossible.utils import *

from .forms import *

from .utils import *

from the_impossible.ERROR import *

from .ajax_encrypt import encrypt

from usermgmt.models import (
	Notification,
	Profile,
)
from .models import (
	Tag, 
	Idea
)

MINIMUM_DATE = datetime.datetime.date(datetime.datetime(2020, 4, 9))
ITEM_PER_PAGE = 12

def explore_page(request,week_num,page_num):
	ctx = {} # Context variables
	ctx["date"] = date = Date()
	ctx["week_num"] = week_num
	ctx["page_num"] = page_num
	today = date.now()

	# Explore Section
	# Note: current date is not normal date format, its year/week/1
	current_date = int_date(f"{today.strftime('%Y')}-{week_num}-1")
	ctx['from_date'] = timestamp_from = current_week_dates(*current_date)
	ctx['to_date'] = timestamp_to = timestamp_from + datetime.timedelta(days=7)
	# Check if previous and next week numbers are valid
	if timestamp_from > MINIMUM_DATE: ctx["previous_week_num"] = week_num - 1
	if week_num < current_week(): ctx["next_week_num"] = week_num + 1
	if request.user.is_authenticated: 
		ctx["profile"] = Profile.objects.filter(user=request.user).first()
		ctx["encrypted_string"] = encrypt(request.user.username)
	# Filter by date
	# https://stackoverflow.com/questions/4923612/filter-by-timestamp-in-query
	ideas = Idea.objects.filter(
		timestamp__gte = timestamp_from,
		timestamp__lt = timestamp_to,
		publish_status = 3
	).distinct().order_by("id").reverse()
	# Split data into pages
	ideas = Paginator(ideas,ITEM_PER_PAGE)
	ctx["max_page"] = ideas.num_pages
	try: current_page = ideas.page(page_num) # Get the ideas on the current page
	except: raise Http404()
	ctx["masonary_ideas"] = current_page 

	# Discover Section
	# Retrieve all ideas from the past 6 months
	ideas = Idea.objects.filter(
		timestamp__gte = date.now() - datetime.timedelta(days=182),
		timestamp__lte = date.now() + datetime.timedelta(days=1),
		publish_status = 3
	).exclude(header_img=None)
	random.seed(datetime.datetime.now())
	ctx["random_ideas"] = random.sample(list(ideas), min(ideas.count(), 10))
	template_file = "idea/explore.html"
	return render(request,template_file,ctx)

@login_required
def detail_page(request,pk):
	ctx = {} # Context variables
	ctx["date"] = Date()
	ctx["idea"] = idea = get_object_or_404(Idea, pk=pk)
	# Add view count
	ctx["profile"] = profile = get_object_or_404(Profile, user=request.user)
	idea.viewed_user.add(profile)
	ctx["encrypted_string"] = encrypt(request.user.username)
	template_file = "idea/detail.html"
	return render(request,template_file,ctx)

@login_required
def create_view(request):
	date = Date()
	profile = get_object_or_404(Profile,user=request.user)
	
	if profile.daily_limit <= 0 and profile.daily_limit_timestamp.strftime("%Y-%m-%d") == str(date.now()): 
		return redirect("home_page")
	else:
		profile.daily_limit = 5
		profile.daily_limit_timestamp = date.now()
		profile.save()
	
	obj = Idea.objects.create(
		name="untitled",
		short_description="",
		full_description="",
		author=profile
	)
	obj.save()
	profile.daily_limit -= 1
	profile.save()
	return redirect("idea_edit_page",pk=obj.id)

@login_required
def edit_page(request,pk):
	ctx = {} # Context variables
	template_file = "idea/edit.html"
	ctx["date"] = date = Date()
	ctx["idea"] = idea = get_object_or_404(Idea, pk=pk)
	if idea.author.user == request.user:
		ctx["form"] = form = IdeaForm(request.POST or None)
		# Set default values
		form.fields["name"].initial = idea.name
		form.fields["short_description"].initial = idea.short_description
		form.fields["full_description"].initial = idea.full_description
		form.fields["tags"].queryset = idea.tags
		form.fields["publish_status"].initial = idea.publish_status
		# Show avaliable tags
		qs = Tag.objects.all().distinct()
		for tag in idea.tags.all():
			qs = qs.exclude(name=tag.name)
		ctx["tags"] = qs
		form.fields["tags_remain"].widget = forms.SelectMultiple(choices=[(choice.id, choice) for choice in qs])
		
		usernames_before_edit = at_filter(idea.full_description)

		# Form validation
		if form.is_valid():
			data = form.cleaned_data
			if data.get("delete") == 2:
				idea.delete()
				return redirect("idea_explore_page",date.week(),1)
			# Changed idea content
			idea.name = data.get("name")
			idea.short_description = data.get("short_description")
			idea.full_description = data.get("full_description")

			# Search description for @ users
			usernames = set(at_filter(data.get("full_description"))) - set(usernames_before_edit)
			for username in usernames:
				user = User.objects.filter(username=username).first()
				if user:
					profile = Profile.objects.filter(user=user).first()
					# Send the mentioned user a notification
					message = f"@{request.user.username} mentioned you in \"{idea.name}\""
					msg = Notification.objects.create(message=message,message_status=2)
					msg.save()
					# Notify mentioned user
					profile.notification.add(msg)
				else: 
					# Tell the current user that their mentioned user does not exsist
					profile = get_object_or_404(user=request.user)
					message = f"@{username} user does not exsist"
					msg = Notification.objects.create(message=message,message_status=1)
					msg.save()
					profile.notification.add(msg)

			# Change publish setting
			idea.publish_status = data.get("publish_status")
			# Add tags
			for tag in eval(data.get('tags_remain') or "[]"): # convert
				idea.tags.add(tag)
			# Remove tags
			for tag in data.get('tags'):
				idea.tags.remove(tag)
			idea.save()
			# Refresh page
			return redirect("idea_edit_page", pk=idea.id)
	else:
		return redirect("access_error_page")
	return render(request,template_file,ctx)

def like_view(request):
	data = {}
	try:
		# Check if request is send by the correct user
		if request.GET.get('encrypted_string') == encrypt(request.GET.get('username')) and request.is_ajax():
			# Get object pk
			pk = request.GET.get('pk', None)
			username = request.GET.get('username', None)
			# Retrieve objects
			idea = Idea.objects.filter(pk=pk).first()
			user = User.objects.filter(username=username).first()
			profile = Profile.objects.filter(user=user).first()
			# Add like
			if profile in idea.liked_user.all(): 	
				data["action"] = "unliked"			
				idea.liked_user.remove(profile) 	
			else: 											
				idea.liked_user.add(profile)		
				data["action"] = "liked"			
		else:
			raise CustomError("AjaxInvalid")
	except:
		data['failed'] = True
	return JsonResponse(data)

def star_view(request):
	data = {}
	try:
		# Check if request is send by the correct user
		if request.GET.get('encrypted_string') == encrypt(request.GET.get('username')) and request.is_ajax():
			# Get object pk
			pk = request.GET.get('pk', None)
			username = request.GET.get('username', None)
			# Retrieve objects
			idea = Idea.objects.filter(pk=pk).first()
			user = User.objects.filter(username=username).first()
			profile = Profile.objects.filter(user=user).first()
			# Add like
			if profile in idea.starred_user.all(): 	
				data["action"] = "unstarred"		
				idea.starred_user.remove(profile)
			else: 											
				idea.starred_user.add(profile)		
				data["action"] = "starred"			
		else:
			raise CustomError("AjaxInvalid")
	except:
		data['failed'] = True
	return JsonResponse(data)
