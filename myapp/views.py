from django.shortcuts import render, redirect
from . import stock_api
from .models import Stock, Profile, Activity, Portfolio, Notification
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views.generic import TemplateView
from .edit_form import ProfileForm
import datetime
from django.http import HttpResponseRedirect
from itertools import chain
from django.utils import timezone


def chart(request):
    return render(request, 'circhart.html')
# View for the home page - a list of 20 of the most active stocks


def index(request):
    # Query the stock table, filter for top ranked stocks and order by their rank.
    data = Stock.objects.filter(
        top_rank__isnull=False).order_by('top_rank')[:20]
    return render(request, 'index.html', {'page_title': 'Main', 'data': data})


# View for the single stock page
# symbol is the requested stock's symbol ('AAPL' for Apple)
def single_stock(request, symbol, time_range="1m"):
    fav = 'favorite'
    data = stock_api.get_stock_info(symbol)
    if request.user.is_authenticated:
        stock = Stock.objects.get(pk=symbol)
        lst = request.user.fav_set.all()
        fav = 'unfavorite' if stock in lst else 'favorite'
    allStocks = Stock.objects.filter(
        top_rank__isnull=False).order_by('top_rank')
    data["allStocks"] = allStocks
    return render(request, 'single_stock.html', {'page_title': 'Stock Page - %s' % symbol, 'data': data, 'time_range': time_range, 'fav': fav})


def register(request):
    # If post -> register the user and redirect to main page
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        newuser = User.objects.create_user(
            username=email, email=email, password=password)
        newuser.first_name = firstname
        newuser.last_name = lastname
        newuser.save()
        return redirect('index')
    else:
        # If not post (regular request) -> render register page
        return render(request, 'register.html', {'page_title': 'Register'})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')


def search(request):
    if request.method == 'POST':
        filter_by, search_data = request.POST.get(
            'filter-checkbox'), request.POST.get('stock_name')
        print(filter_by, search_data)
        if filter_by == "symbol":
            data = Stock.objects.filter(symbol__iexact=search_data)
        elif filter_by == "name":
            data = Stock.objects.filter(name__iexact=search_data)
        elif filter_by == "price":
            if 'price-icon' in request.POST:
                data = Stock.objects.filter(price__lte=search_data)
            else:
                data = Stock.objects.filter(price__gte=search_data)
        elif filter_by == "change":
            if 'change-icon' in request.POST:
                data = Stock.objects.filter(change_percent__lte=0)
            else:
                data = Stock.objects.filter(change_percent__gte=0)
        else:
            data = None
        return render(request, 'index.html', {'page_title': 'Main', 'data': data})


def view_all(request):
    if request.method == 'GET':
        api_data = stock_api._get_all_stocks()
        index = 1
        for stock in api_data:
            stock_model, created = Stock.objects.update_or_create(symbol=stock['symbol'], defaults={
                'name': stock['companyName'],
                'top_rank': index,
                'price': stock['latestPrice'],
                'change': stock['change'],
                'change_percent': stock['changePercent'],
                'market_cap': stock['marketCap'],
                'primary_exchange': stock['primaryExchange'],
            })
            stock_model.save()
            index += 1
        data = Stock.objects.all()
        return render(request, 'index.html', {'page_title': 'All Stocks', 'data': data})


def single_stock_data(request, symbol):
    data = stock_api.get_stock_info(symbol)
    return JsonResponse({'data': data})


# API for a stock's price over time
# symbol is the requested stock's symbol ('AAPL' for Apple)
# The response is JSON data of an array composed of "snapshot" objects (date + stock info + ...), usually one per day
def single_stock_historic(request, symbol, time_range):
    data = stock_api.get_stock_historic_prices(symbol, time_range=time_range)
    return JsonResponse({'data': data})


def my_profile(request):
    if request.user.is_authenticated:
        fav_stocks = Stock.objects.filter(current_user=request.user)
        lst = request.user.fav_set.all()
        activities = Activity.objects.filter(user=request.user)
        return render(request, 'profile.html', {'user': request.user, 'fav_stocks': lst, 'activities': activities})
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


def my_portfolio(request):
    if request.user.is_authenticated:
        # fav_stocks = Stock.objects.filter(current_user = request.user)
        # lst = Portfolio.objects.filter()
        lst = request.user.port_set.all()
        for stock in lst:
            port = Portfolio.objects.filter(stock=stock)
            print('port: ', port)
        return render(request, 'portfolio.html', {'data': lst})
    return redirect('login')


def buy(request, symbol=''):
    if request.user.is_authenticated:
        stock = Stock.objects.get(pk=symbol)
        stock.portfolio_list.add(request.user, through_defaults={
            'first_price': stock.price,
            'date': datetime.datetime.now(),
            'shares': 2
        })
        stock.save()
        return redirect('portfolio')
    return redirect('login')


def favorite(request, symbol=''):
    if request.user.is_authenticated:
        stock = Stock.objects.get(pk=symbol)
        stock.current_user = request.user
        stock.favorite.add(request.user)
        stock.save()
        # Stock.make_favorite(request.user, stock)
        return redirect('profile')
    return redirect('login')


def unfavorite(request, symbol=''):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        stock = Stock.objects.get(pk=symbol)
        stock.favorite.remove(user)
        stock.save()
        return redirect('profile')
    return redirect('login')


# def favorite(request, symbol=''):
#
#     if request.user.is_authenticated:
#
#         stock = Stock.objects.get(pk=symbol)
#         Stock.make_favorite(request.user, stock)
#         return redirect('profile')
#     return redirect('login')
#
#
# # return render(request,'profile.html', {'user': request.user})
#
#
# def unfavorite(request, symbol=''):
#     if request.user.is_authenticated:
#         # stk, created = Stock.objects.get_or_create(current_user=request.user)
#         # stk.favorite.remove(Stock.objects.get(pk=symbol))
#
#         user = User.objects.get(pk=request.user.pk)
#         # stock = Stock()
#         # stock.favorite.remove(user)
#         # lst = Stock.objects.
#
#         stock = Stock.objects.get(pk=symbol)
#         stock.favorite.remove(user)
#         # print('list of users loving this stock:',stock.favorite.all())
#         # print('this stock current user', stock.current_user)
#         print('the list of stocks that this user loves', user.stock_set.all())
#         # print('this is the list::::::::::::::',Stock.objects.filter(current_user = request.user))
#         stock.save()
#         return redirect('profile')
# # return render(request,'profile.html', {'user': request.user})
#     return redirect('login')


def get_notifications(request):
    if request.is_ajax and request.method == "GET" and request.user.is_authenticated:
        data = {}
        time_range = "1d"
        lst = request.user.port_set.all()
        lst2 = request.user.fav_set.all()
        notifications = request.user.notifications_set.all()
        for n in notifications:

            if (n.was_created_recently()):
                data[n.stock.symbol] = {
                    "raise_percent": n.stock_raise, "date": n.date}
            else:
                n.delete()

        for stock in chain(lst, lst2):
            if stock.symbol not in data:
                stockData = stock_api.get_stock_historic_prices(
                    stock.symbol, time_range=time_range)
                notification = get_notifications_data(stockData)
                if(notification != None):
                    data[stock.symbol] = notification

                    n = Notification(
                        stock=stock, stock_raise=notification["raise_percent"])
                    n.save()
                    n.notifications.add(request.user)
                notification = None

    return JsonResponse({'data': data})


def get_notifications_data(stockData):
    i = 0
    firstValue = None
    lastValue = None
    lenData = len(stockData)
    current_date = ""
    while(firstValue == None or lastValue == None and i < lenData):
        firstValue = stockData[i]["close"]
        lastValue = stockData[lenData - i - 1]["close"]
        current_date = stockData[i]["date"]
        i = i + 1

    raise_percent = (lastValue / firstValue)*100
    if(raise_percent > 101 or raise_percent < 99):
        result = {"raise_percent": raise_percent - 100, "date": current_date}
    else:
        result = None

    return result
