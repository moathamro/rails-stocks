from django.shortcuts import render, redirect
from myapp import stock_api
from myapp.models import Stock
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout


# View for the home page - a list of 20 of the most active stocks
def index(request):
    # Query the stock table, filter for top ranked stocks and order by their rank.
    data = Stock.objects.filter(top_rank__isnull=False).order_by('top_rank')[:20]
    return render(request, 'index.html', {'page_title': 'Main', 'data': data})


# View for the single stock page
# symbol is the requested stock's symbol ('AAPL' for Apple)
def single_stock(request, symbol):
    data = stock_api.get_stock_info(symbol)
    return render(request, 'single_stock.html', {'page_title': 'Stock Page - %s' % symbol, 'data': data})


def register(request):
    # If post -> register the user and redirect to main page
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


def logout_view(request):
    logout(request)
    return redirect('index')


def search(request):
    if request.method == 'POST':
        filter_by, search_data = request.POST.get('filter-checkbox'), request.POST.get('stock_name')
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


# API for a stock's price over time
# symbol is the requested stock's symbol ('AAPL' for Apple)
# The response is JSON data of an array composed of "snapshot" objects (date + stock info + ...), usually one per day
def single_stock_historic(request, symbol):
    data = stock_api.get_stock_historic_prices(symbol, time_range='1m')
    return JsonResponse({'data': data})
