from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('stock/<str:symbol>/', views.single_stock, name='single_stock'),
    path('stock/<str:symbol>/data/',
         views.single_stock_data, name='single_stock_data'),
    path('stock/<str:symbol>/<str:time_range>/',
         views.single_stock, name='single_stock'),
    path('historic/<str:symbol>/<str:time_range>/',
         views.single_stock_historic, name='single_stock_historic'),

    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.my_profile, name='profile'),
    path('edit', views.edit_profile, name='edit_profile'),
    path('favorite/<str:symbol>/', views.favorite, name='favorite'),
    path('buy/<str:symbol>/', views.buy, name='buy'),
    path('portfolio/', views.my_portfolio, name='portfolio'),
    path('unfavorite/<str:symbol>/', views.unfavorite, name='favorite'),
    path('sell/<str:symbol>/', views.sell, name='toSell'),
    path('clear', views.history, name='history'),

    # path('add/<str:symbol>/', views.favorite, name='favorite'),
    # path('remove/<str:symbol>/', views.unfavorite, name='favorite'),
    path('chr/', views.chart, name='chart'),
    path('search/', views.search, name='search'),
    path('viewall', views.view_all, name='view_all'),

    path('notifications/', views.get_notifications, name='get_notifications'),
]


"""
for the price over time range line
1) i changed the url for single_stock and single_stock_historic
2)in the index page i set the time_range when routing to single_stock to 1m (default)
3)in the single_stock.html i took the timerange variable to the historic function 
to return the range from the api
4)in the design part, i turned the href into the index page url and set the time_rane according to
the button that was clicked
"""
