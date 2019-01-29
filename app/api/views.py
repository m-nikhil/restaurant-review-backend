from django.shortcuts import render
from rest_framework import viewsets, views
from . import serializers
from . import models
from django.conf import settings
import requests
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ReviewGetSerializer
        elif self.request.method == 'POST':
            return serializers.ReviewPostSerializer
        else:
            return serializers.ReviewPutSerializer

#query
class Search(views.APIView):

    cuisines = openapi.Parameter('cuisines', openapi.IN_QUERY, description="cuisines", type=openapi.TYPE_STRING)
    establishment_type = openapi.Parameter('establishment_type', openapi.IN_QUERY, description="establishment_type", type=openapi.TYPE_STRING)
    category = openapi.Parameter('category', openapi.IN_QUERY, description="category", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[cuisines,establishment_type,category])
    def get(self, request):

        cuisines = self.request.query_params.get('cuisines')
        establishment_type = self.request.query_params.get('establishment_type')
        category = self.request.query_params.get('category')

        PARAMS = {'entity_type': 'city', 'entity_id' : settings.CITY_ID} 
        HEADERS = {'Accept': 'application/json', 'user-key': settings.ZOMATO_API_KEY}
        response = requests.get(url = settings.ZOMATO_API_URL  + 'search',params = PARAMS, headers = HEADERS)
        return Response(response.json())

class Categories(views.APIView):
    def get(self, request):
        HEADERS = {'Accept': 'application/json', 'user-key': settings.ZOMATO_API_KEY}
        response = requests.get(url = settings.ZOMATO_API_URL  + 'categories', headers = HEADERS)
        return Response(response.json())

class Type(views.APIView):
    def get(self, request):
        PARAMS = {'city_id': settings.CITY_ID} 
        HEADERS = {'Accept': 'application/json', 'user-key': settings.ZOMATO_API_KEY}
        response = requests.get(url = settings.ZOMATO_API_URL  + 'establishments',params = PARAMS, headers = HEADERS)
        return Response(response.json())

class Cuisines(views.APIView):
    def get(self, request):
        PARAMS = {'city_id': settings.CITY_ID} 
        HEADERS = {'Accept': 'application/json', 'user-key': settings.ZOMATO_API_KEY}
        response = requests.get(url = settings.ZOMATO_API_URL  + 'cuisines',params = PARAMS, headers = HEADERS)
        return Response(response.json())


class Restaurant(views.APIView):

    restaurant_id = openapi.Parameter('restaurant_id', openapi.IN_QUERY, description="restaurant_id", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[restaurant_id])
    def get(self, request):

        restaurant_id = self.request.query_params.get('restaurant_id')
        if not restaurant_id:
            return Response({'error':'Pass restaurant id query parameter.'}, status=500)

        PARAMS = {'res_id': restaurant_id} 
        HEADERS = {'Accept': 'application/json', 'user-key': settings.ZOMATO_API_KEY}
        response = requests.get(url = settings.ZOMATO_API_URL  + 'restaurant',params = PARAMS, headers = HEADERS)
        return Response(response.json())