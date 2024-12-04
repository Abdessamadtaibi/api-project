from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('category-admin/',views.CategoryViewAdmin.as_view()),#username = admin , password = admin
    path('menu-item-admin/',views.MenuItemViewAdmin.as_view()),
    path('group/manager/',views.manager,name='manager'),
    path('group/manager/users/',views.manager_users,name='manager_users'),
    path('manager/',views.MenuItemManagerView.as_view()),
    path('manager/delivery-crew/',views.DeliveryCrewManagerView.as_view()),
    path('delivery-crew/orders/',views.DeliveryCrewView.as_view()),
    path('register/',views.RegisterView.as_view()),
    path('category/',views.CategoryCustomerView.as_view()),
    path('menu-item/',views.MenuItemCustomerView.as_view()),
    path('card/',views.ItemsCardCustomerView.as_view()),
    path('orders/',views.OrdersCustomerView.as_view()),    
]
