from rest_framework import serializers
from .models import PCPart

class PCPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCPart
        fields = ['id', 
                  'name', 
                  'type', 
                  'price',
                  'release_date',
                  'core_clock',
                  'boost_clock',
                  'clock_unit',
                  'TDP',
                  'part_no']
        
   

class PCPartSerializerMany(serializers.ModelSerializer):
    """
    This class is for showing only few things, instead of the everything.
    """
    class Meta:
        model = PCPart
        fields = ('id', 'name', 'type', 'price')