from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime

from .utils import *

from .models import (
	Idea,
)

from usermgmt.models import (
	Profile,
)

MINIMUM_DATE = datetime.datetime.date(datetime.datetime(2020, 4, 9))
ITEM_PER_PAGE = 10

def explore_page(request,week_num,page_num):
	ctx = {} # Context variables
	ctx["week_num"] = week_num
	ctx["page_num"] = page_num
	today = datetime.datetime.now().date()
	# Note: current date is not the date, its year/week/1
	current_date = int_date(f"{today.strftime('%Y')}-{week_num}-1")
	ctx['from_date'] = timestamp_from = current_week_dates(*current_date)
	ctx['to_date'] = timestamp_to = timestamp_from + datetime.timedelta(days=7)
	# Check if previous and next week numbers are valid
	if timestamp_from > MINIMUM_DATE: ctx["previous_week_num"] = week_num - 1
	if week_num < current_week(): ctx["next_week_num"] = week_num + 1
	if True: # request.user.is_authenticated
		# Filter by date
		# https://stackoverflow.com/questions/4923612/filter-by-timestamp-in-query
		ideas = Idea.objects.filter(
			timestamp__gte = timestamp_from,
    		timestamp__lt = timestamp_to,
		).distinct()
		# print(timestamp_from,timestamp_to)
		# if ideas.count() > 1:
		# Split data into pages
		ideas = Paginator(ideas,ITEM_PER_PAGE)
		ctx["max_page"] = ideas.num_pages
		try: current_page = ideas.page(page_num) # Get the ideas on the current page
		except: raise Http404()
		ctx["ideas"] = current_page 
	template_file = "idea/explore.html"
	return render(request,template_file,ctx)

@login_required
def detail_page(request,pk):
	ctx = {} # Context variables
	ctx["idea"] = idea = get_object_or_404(Idea, pk=pk)
	# Add view count
	profile = get_object_or_404(Profile, user=request.user)
	idea.viewed_user.add(profile)
	template_file = "idea/detail.html"
	return render(request,template_file,ctx)

@login_required
def like_view(request):
	data = {}
	try:
		# Get data
		pk = request.GET.get('pk', None)
		username = request.GET.get('username', None)
		# Retrieve objects
		idea = Idea.objects.filter(pk=pk).first()
		user = User.objects.filter(username=username).first()
		profile = Profile.objects.filter(user=user).first()
		# Add like
		idea.liked_user.add(profile)
		data['like_count'] = idea.liked_user.count()
	except:
		data['failed'] = True
	return JsonResponse(data)

