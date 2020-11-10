from django.shortcuts import render, redirect
from . import stock_api
from .models import Stock, Profile, Activity
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views.generic import TemplateView
from .edit_form import ProfileForm
from django.http import HttpResponseRedirect

def chart(request):
	return render(request, 'circhart.html')
# View for the home page - a list of 20 of the most active stocks
def index(request):
	# Query the stock table, filter for top ranked stocks and order by their rank.
	data = Stock.objects.filter(top_rank__isnull=False).order_by('top_rank')
	return render(request, 'index.html', {'page_title': 'Main', 'data': data })


# View for the single stock page
# symbol is the requested stock's symbol ('AAPL' for Apple)
# def single_stock(request, symbol):
#
# 	data = stock_api.get_stock_info(symbol)
#
# 	allStocks = Stock.objects.filter(top_rank__isnull=False).order_by('top_rank')
# 	data["allStocks"] = allStocks
# 	return render(request, 'single_stock.html', {'page_title': 'Stock Page - %s' % symbol, 'data': data, 'time_range':"1m"})
#

def single_stock_data(request, symbol):
	data = stock_api.get_stock_info(symbol)
	return JsonResponse({'data': data})


def register(request):
	# If post -> register the user and redirect to main page
	if request.user.is_authenticated:
		if request.method == 'POST':
			firstname = request.POST.get('firstname')
			lastname = request.POST.get('lastname')
			email = request.POST.get('email')
			password = request.POST.get('password')

			newuser = User.objects.create_user(username=email, email=email, password=password)
			newuser.first_name = firstname
			newuser.last_name = lastname
			newuser.save()
			return redirect('index')
		else:
			# If not post (regular request) -> render register page
			return render(request, 'register.html', {'page_title': 'Register'})
	return redirect('login')



def logout_view(request):
	if request.user.is_authenticated:
		logout(request)
	return redirect('index')


# API for a stock's price over time
# symbol is the requested stock's symbol ('AAPL' for Apple)
# The response is JSON data of an array composed of "snapshot" objects (date + stock info + ...), usually one per day
# def single_stock_historic(request, symbol):
# 	data = stock_api.get_stock_historic_prices(symbol, time_range='1m')
# 	return JsonResponse({'data': data})

def single_stock_historic(request, symbol, time_range):
	data = stock_api.get_stock_historic_prices(symbol, time_range=time_range)
	return JsonResponse({'data': data})

def single_stock(request, symbol, time_range="1m"):

	data = stock_api.get_stock_info(symbol)

	allStocks = Stock.objects.filter(top_rank__isnull=False).order_by('top_rank')
	data["allStocks"] = allStocks
	return render(request, 'single_stock.html', {'page_title': 'Stock Page - %s' % symbol, 'data': data, 'time_range':"1m"})


def my_profile(request):
	if request.user.is_authenticated:
		fav_stocks = Stock.objects.filter(current_user = request.user)
		lst = request.user.stock_set.all()
		activities = Activity.objects.filter(user=request.user)
		return render(request,'profile.html', {'user': request.user, 'fav_stocks': lst, 'activities':activities})
	return redirect('login')

def edit_profile(request):
	if request.user.is_authenticated:
		profile = request.user.profile
		form = ProfileForm(instance=profile)

		if request.method == 'POST':
			form = ProfileForm(request.POST, request.FILES, instance=profile)
			if form.is_valid():
				form.save()
			return redirect('accounts/profile')
		args = {'form': form}
		return render(request, 'edit_profile.html', args)
	return redirect('login')



def favorite(request,symbol=''):

	if request.user.is_authenticated:

		stock = Stock.objects.get(pk=symbol)
		Stock.make_favorite(request.user, stock)
		return redirect('profile')
	return redirect('login')





# return render(request,'profile.html', {'user': request.user})


def unfavorite(request,symbol=''):
	if request.user.is_authenticated:
		# stk, created = Stock.objects.get_or_create(current_user=request.user)
		# stk.favorite.remove(Stock.objects.get(pk=symbol))


		user = User.objects.get(pk=request.user.pk)
		# stock = Stock()
		# stock.favorite.remove(user)
		# lst = Stock.objects.

		stock =Stock.objects.get(pk=symbol)
		stock.favorite.remove(user)
		# print('list of users loving this stock:',stock.favorite.all())
		# print('this stock current user', stock.current_user)
		print('the list of stocks that this user loves',user.stock_set.all())
		# print('this is the list::::::::::::::',Stock.objects.filter(current_user = request.user))
		stock.save()
		return redirect('profile')
# return render(request,'profile.html', {'user': request.user})
	return redirect('login')

def single_stock_financials(request, symbol):
	if request.is_ajax and request.method == "GET":
		data = stock_api.get_stock_financials_report(symbol)
	return JsonResponse({'data': data})


