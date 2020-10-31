from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('stock/<str:symbol>/', views.single_stock, name='single_stock'),
	path('stock/<str:symbol>/data/', views.single_stock_data, name='single_stock_data'),
	path('historic/<str:symbol>/', views.single_stock_historic, name='single_stock_historic'),
	path('financials/<str:symbol>/', views.single_stock_financials, name='single_stock_financials'),
	path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
	path('accounts/logout/', views.logout_view, name='logout'),
	path('accounts/register/', views.register, name='register'),
]