from django.urls import path, re_path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('review', views.ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('zomato/search', views.Search.as_view()),
    path('zomato/categories', views.Categories.as_view()),
    path('zomato/type', views.Type.as_view()),
    path('zomato/cuisines', views.Cuisines.as_view()),
    path('zomato/restaurant', views.Restaurant.as_view()),
]

