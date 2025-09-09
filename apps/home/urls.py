# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from apps.home.views import BookingCreateView

app_name = "home"

urlpatterns = [

    # The home page
    path('', views.index, name='index'),

    # Matches any html file
    path('booking/create/', BookingCreateView.as_view(), name='booking_create'),
    path('hotels/turkey/', views.turkey_hotel, name='turkey_hotel'),
    path('hotels/egypt/', views.egypt_hotel, name='egypt_hotel'),
    path('hotels/odessa/', views.odessa_hotel, name='odessa_hotel'),
    path('hotels/thailand/', views.thailand_hotel, name='thailand_hotel'),
    path('about_us/', views.about_us, name='about_us'),
    path("booking/<int:booking_id>/confirmation/", views.booking_confirmation, name="booking_confirmation"),
    re_path(r'^.*\.*', views.pages, name='pages'),
]
