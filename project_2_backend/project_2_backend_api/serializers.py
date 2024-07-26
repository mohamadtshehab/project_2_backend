from rest_framework import serializers
from .models import *


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = '__all__'
        
        
class TextureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Texture
        fields = '__all__'
     

class TDModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TDModel
        fields = '__all__'
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
           
class ObjectSerializer(serializers.ModelSerializer):
    td_model = TDModelSerializer()
    category = CategorySerializer()
    room = RoomSerializer()
    textures = TextureSerializer()
    
    class Meta:
        model = Object
        fields = ['td_model', 'category', 'room', 'url', 'textures', 'material',]

        
class ObjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectImage
        fields = '__all__'