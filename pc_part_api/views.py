from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.db.models import Avg
from .models import PCPart
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F, ExpressionWrapper, fields
from django.db.models import Count
from django.db.models import FloatField
from django.views.decorators.http import require_http_methods

from rest_framework import status

@api_view(['GET', 'PUT'])
def PCParts_list(request, format=None):
    print(request.method)
    if request.method == 'GET':

        # We have to make sure that type is in uppercase
        part_type = request.GET.get('type', '').upper()
        part_type = part_type.upper()

        # If the type = ? is something else, then they are looking for an invalid type
        if part_type and part_type not in ['CPU', 'GPU']:
            return Response({"status": 1, "message": "Invalid 'type' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        # Apply the filters, which sorts
        pcparts = PCPart.objects.filter(type__iexact=part_type).order_by('-price')

        # Counts the number of items and the avg price
        total_parts = pcparts.count()
        avg_price = pcparts.aggregate(avg_price=Avg('price'))['avg_price']

        # We get the things we want to print out through serializer
        serializer = PCPartSerializerMany(pcparts, many=True)

        # Format of return 
        response_data = {
            "status": 0,
            "total": total_parts,
            "average_price": avg_price,
            "parts": serializer.data,
        }

        return Response(response_data)
    
    # When the user wants to 
    elif request.method == 'PUT':
        data = request.data
        part_type = data.get('type', '').upper()
        
        if part_type not in ['CPU', 'GPU']:
            return Response({"status": 1, "message": "Failed to add"}, status=status.HTTP_400_BAD_REQUEST)

        new_part = PCPart.objects.create(**data)

        response_data = {
            "status": 0,
            "message": "New part added",
            "id": str(new_part.id),
        }

        return Response(response_data, status=status.HTTP_200_OK)
    

# This is responsible for deleteing part, part modification, part detail update, get a individual part
# In views.py, update the PCPart_detail function
# @require_http_methods(["GET", "POST", "PATCH", "DELETE"])
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def PCPart_detail(request, id, format=None):
    try:
        pcpart = PCPart.objects.get(pk=id)
    except PCPart.DoesNotExist:
        return Response({"status": 1, "message": "Part not found"}, status=status.HTTP_404_NOT_FOUND)

    # When the user only wants to return one item
    if request.method == 'GET':
        serializer = PCPartSerializer(pcpart)
        response_data = {"status": 0, **serializer.data}
        return Response(response_data)

    # When the user wants to edit the entire thing at once
    elif request.method == 'POST':
        data = request.data
        if 'type' in data:
            data['type'] = data['type'].upper()

        serializer = PCPartSerializer(pcpart, data=data)
        if serializer.is_valid():
            new_part = serializer.save()
            return Response({"status": 0, "message": "New part added", "id": str(new_part.id)}, status=status.HTTP_201_CREATED)
        return Response({"status": 1, "message": "Something went wrong while updating"}, status=status.HTTP_400_BAD_REQUEST)

    # When the user wants to edit only one
    elif request.method == 'PATCH':
        data=request.data
        if 'type' in data:
            data['type'] = data['type'].upper()
        
        contains_unknown = is_data_valid(data)

        serializer = PCPartSerializer(pcpart, data=data, partial=True)
        if serializer.is_valid() and contains_unknown:
            serializer.save()
            return Response({"status": 0, "message": "Part modified"}, status=status.HTTP_200_OK)
        return Response({"status": 1, "message": "You have an invalid key(s)"}, status=status.HTTP_400_BAD_REQUEST)

    # When the user wants to delete
    elif request.method == 'DELETE':
        pcpart.delete()
        return Response({"status": 0, "message": "Part deleted"}, status=status.HTTP_200_OK)
    
    

def is_data_valid(data, fields = ['id', 'name', 'type', 'price', 'release_date', 'core_clock', 'boost_clock', 'clock_unit', 'TDP', 'part_no']):
    """
    This function will take two things. and see if the keys in data are in the fields, if not then the user is trying to put in
    something that is not valid.
    Parameter: data (dictionary), fields (list)
    return: contains_unknown_fields (Bool)
    """
    contains_unknown_fields = any(key not in fields for key in data.keys())
    return not contains_unknown_fields
