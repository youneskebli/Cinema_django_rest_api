from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets

from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

#1 without REST and no model query FBV
def no_rest_no_model(request):
    guests = [
        {
            'id': 1,
            "Name": "Omar",
            "mobile": 789456,
        },
        {
            'id': 2,
            'name': "yassin",
            'mobile': 74123,
        }
    ]
    return JsonResponse(guests, safe=False)

#2 model data default djanog without rest
def no_rest_from_model(request):
    data= Movie.objects.all()
    response = {
        'guest': list(data.values('hall','movieName'))
    }
    return JsonResponse(response)
#3 Function based views 
#3.1 GET POST
@api_view(['GET','POST'])
def fbv_getAll_movies(request):
    if request.method == 'GET':
        movies= Movie.objects.all()
        serializer = MovieSerializer(movies,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = MovieSerializer(data=data)
        if not serializer.is_valid():
            return Response({'error':'data not valid'},status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
#3.1 GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def fbv_pk_(request,pk):
    try:
        movie = get_object_or_404(Movie,pk=pk)
    except Movie.DoesNotExists:
        return Response({'error':'this movie does not exists'},status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serialier = MovieSerializer(movie,many=False)
        return Response(serialier.data)
    elif request.method == 'PUT':
        data = request.data
        serializer = MovieSerializer(movie,data=data)
        if not serializer.is_valid():
            return Response({'error':'data not valid'},status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response({'details':'deleted with success'},status=status.HTTP_200_OK)

# CBV Class based views
#4.1 List and Create == GET and POST
class CBV_list_post(APIView):
    def get_all_movies(self,request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies,many=True)
        return Response(serializer.data)
    def create_one_movie(self,request):
        data = request.data
        serializer = MovieSerializer(data=data)
        if not serializer.is_valid():
            return Response({'error':'data not valid'},status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
#4.2 GET PUT DELETE cloass based views -- pk
class CBV_get_put_delete(APIView):
    def get_object(self,pk):
        try:
            movie = Movie.objects.get(pk=pk)
            return movie
        except Movie.DoesNotExists:
            raise Http404
    def get_pk(self,request,pk):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie,many=False)
        return Response(serializer.data)
    def put(self,request,pk):
        data = request.data
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie,data=data)
        if not serializer.is_valid():
            return Response({'errror':'data not valid'},status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)
    def delete(self,request,pk):
        movie = self.get_object(pk)
        movie.delete()
        return Response({'details':'movie delete with success'},status=status.HTTP_200_OK)
       
#5 Mixins 
#5.1 mixins list
class mixins_list_post(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
    def list(self,request):
        return self.list(request)
    def create(self, request):
        return self.create(request)
#5.2 mixins get put delete    
class mixins_get_put_delete(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
    def get_one(self,request,pk):
        return self.retrieve(request,pk)
    def put(self,request,pk):
        return self.update(request,pk)
    def delete(self,request,pk):
        return self.destroy(request,pk)
        
# 6 Generics 
#6.1 get and post
class generic_list_post(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
#6.2 get put and delete
class generics_get_put_delete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
        
#7 viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movieName']
class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
#8 filter movie
@api_view(['GET'])
def filter_view(request):
    movie = Movie.objects.filter(
        hall= request.data['hall']
    )
    serializer= MovieSerializer(movie,many=True)
    return Response(serializer.data)
@api_view(['POST'])
def create_reservation(request,pk):
    guest = get_object_or_404(Guest,pk)
    movie = Movie.objects.get(
        hall=request.data['hall'],
        movieName=request.data['movieName']
    )
    reservation = Reservation ()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    return Response(status.HTTP_201_CREATED)
    
    
    
        
        
    
