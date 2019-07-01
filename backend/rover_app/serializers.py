
from rest_framework import serializers
from .models import Owner, Sitter, Stay, Pet

class SitterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sitter
        fields = ('id',
                  'sitter_name',
                  'sitter_image',
                  'sitter_score',
                  'avg_rating_score',
                  'overall_sitter_rank'
                  )

class SitterDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sitter
        fields = ('id',
                  'sitter_name',
                  'sitter_image',
                  'sitter_phone_number',
                  'sitter_email',
                  'sitter_score',
                  'avg_rating_score',
                  'overall_sitter_rank'
                  )

# class OwnerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Owner
#         fields = ('id',
#                   'owner_name',
#                   'owner_image',
#                   'owner_phone_number',
#                   'owner_email')

# class PetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pet
#         fields = ('id',
#                   'pet_name',
#                   'owner')
#
# class StaySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Stay
#         fields = ('id',
#                   'rating',
#                   'text',
#                   'start_date',
#                   'end_date',
#                   'owner',
#                   'sitter',
#                   'pets')
