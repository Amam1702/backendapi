from rest_framework import serializers
from .models import Transactions,Attendant,ClientMaster,Voucher,chat,Users,Station

class TransactionSerializer(serializers.ModelSerializer):

  
   class Meta:
      model = Transactions
      fields = '__all__'

class AttendantSerializer(serializers.ModelSerializer):
   class Meta:
      model=  Attendant
      fields = '__all__'

class VoucherSerializer(serializers.ModelSerializer):
   class Meta:
      model = Voucher
      fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
   class Meta:
      model = ClientMaster
      fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
   class Meta:
      model = chat
      fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = Users
      fields = '__all__'
      extra_kwargs = {
            'password': {'write_only': True}
        }
      
class StationSerializer(serializers.ModelSerializer):
   class Meta:
      model = Station
      fields='__all__'