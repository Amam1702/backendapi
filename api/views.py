from django.shortcuts import render
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from .models import *
from api.serializers import *

from django.utils import timezone
from datetime import datetime
# Create your views here.

class CustomAuthToken(ObtainAuthToken):
     def post(self,request,*args,**kwargs):
          serializer = self.serializer_class(data=request.data,context={'request':request})
          serializer.is_valid(raise_exception=True)
          new_user = serializer.validated_data['username']
          Token.objects.filter(user=new_user).delete()
          token, created = Token.objects.create(user=new_user)
          return Response({'status': token.key})


"""All Create API Functions"""
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def createAttendant(request):
        """Authenticate and Create client """
        result = []
        for row in request.data['data']:
            try:
                serializer = AttendantSerializer(data=row)
                new_user = User.objects.create_superuser(username=row['employee_id'],password=row['password'])
                if serializer.is_valid():
                    serializer.save()
                    token,created = Token.objects.get_or_create(user=new_user)
                    result.append({row['employee_id']:'Created Attendant'})
                else:
                   result.append({row['employee_id']:serializer.errors})
            except Exception as e:
                    result.append({row['employee_id']:str(e)})
        return Response(result)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def createVoucher(request):
        result = []
        """Authenticate user and create agent"""
        print(request.data)
        
        for row in request.data['data']:
            print(row)
            try:
                serializer = VoucherSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                    client = ClientMaster.objects.get(client_id=row['client_id'])
                    client.active_vouchers = client.active_vouchers+1
                    client.save(update_fields=['active_vouchers'])
                    result.append({row['voucher_id']:"created"})
                else:
                     result.append({row['voucher_id']:serializer.errors})
            except Exception as e:
                result.append({row['voucher_id']:str(e)})
        return Response(result)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def createClient(request):
        result = []
        """Authenticate user and create agent"""
        for row in request.data['data']:
            try:
                serializer = ClientSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                    result.append({serializer.data['client_id']:'Created Client'})
                else:
                    result.append({row['client_name']:serializer.errors})
            except Exception as e:
                result.append({serializer.data['client_id']:str(e)})
        return Response(result)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def createTransaction(request):
        """Authenticate user and create agent"""
        try:
            voucher = Voucher.objects.get(voucher_id = request.data['Voucher_id'])
            if voucher.balance == 0:
                 return Response({'status':"Balance Exhausted"})
            request.data['left_balance'] = request.data['initial_amount'] - request.data['redeem_amount']
            serializer = TransactionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                voucher.balance = voucher.balance - request.data['redeem_amount']
                voucher.last_transaction_id = serializer.data['txn_id']
                voucher.last_used = str(timezone.now())
                voucher.save(update_fields=['last_transaction_id','balance','last_used'])
                return Response({'status':'Created Transaction','data':serializer.data})
            else:
                return Response(serializer.errors)
        except Exception as e:
             return Response({'status':str(e)})


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def createUser(request):
        result = []
        """Authenticate user and create agent"""
        for row in request.data['data']:
            try:
                serializer = UserSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                    result.append({serializer.data['email']:'User Created'})
                else:
                    result.append({row['email']:serializer.errors})
            except Exception as e:
                result.append({serializer.data['email']:str(e)})
        return Response(result)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def createStation(request):
        result = []
        """Authenticate user and create agent"""
        for row in request.data['data']:
            try:
                serializer = StationSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                    result.append({serializer.data['station_id']:'Station Created'})
                else:
                    result.append({row['station_name']:serializer.errors})
            except Exception as e:
                result.append({serializer.data['station_name']:str(e)})
        return Response(result)
""""""

"""All Retrieve API Functions"""
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def clientListAll(request):
        """Display all the clients from database"""
        clients = ClientMaster.objects.all()
        serializer = ClientSerializer(clients,many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def attendantListAll(request):
        """Display all the clients from database"""
        attendants = Attendant.objects.all()
        serializer = AttendantSerializer(attendants,many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def voucherListAll(request):
        """Display all the clients from database"""
        vouchers = Voucher.objects.all()
        serializer = VoucherSerializer(vouchers,many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def transactionsListAll(request):
        """Display all the clients from database"""
        transactions = Transactions.objects.all()
        serializer = TransactionSerializer(transactions,many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def UserListAll(request):
        """Display all the clients from database"""
        users = Users.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def StationListAll(request):
        """Display all the clients from database"""
        stations = Station.objects.all()
        serializer = StationSerializer(stations,many=True)
        return Response(serializer.data)
""""""

"""GET by ID,Update By ID,Delete by ID"""
@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def client_details(request,pk):
    """display all Client Details"""
    try:
        client = ClientMaster.objects.get(client_id=pk)
    except Exception as e:
            return Response({'status':'Client ID not found'})

    if request.method=='GET':
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    elif request.method=='PUT':
        serializer = ClientSerializer(client,data=request.data,partial=True)
        if serializer.is_valid():
              serializer.save()
              return Response({'status':'Data Updated'})
        return Response({'status':serializer.errors})
    
    elif request.method=='DELETE':
         client.delete()
         return Response({'status':'Client Deleted'})


@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def attendant_details(request,pk):
    try:
        atdt = Attendant.objects.get(employee_id=pk)
    except Exception as e:
            return Response({'status':'Attendant ID not found'})

    if request.method=='GET':
        serializer = AttendantSerializer(atdt)
        return Response(serializer.data)

    elif request.method=='PUT':
        serializer = AttendantSerializer(atdt,data=request.data,partial=True)
        if serializer.is_valid():
              serializer.save()
              return Response({'status':'Data Updated'})
        return Response({'status':serializer.errors})
    elif request.method=='DELETE':
         atdt.delete()
         return Response({'status':'Attendant Deleted'})


@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def voucher_details(request,pk):
    try:
        voucher = Voucher.objects.get(voucher_id=pk)
    except Exception as e:
            return Response({'status':'Voucher ID not found'})

    if request.method=='GET':
        serializer = VoucherSerializer(voucher)
        return Response(serializer.data)

    elif request.method=='PUT':
        serializer = VoucherSerializer(voucher,data=request.data,partial=True)
        if serializer.is_valid():
              serializer.save()
              return Response({'status':'Data Updated'})
        return Response({'status':serializer.errors})
    
    elif request.method=='DELETE':
        serializer = VoucherSerializer(voucher)
        client = ClientMaster.objects.get(client_id=serializer.data['client_id'])
        client.active_vouchers = client.active_vouchers-1
        client.save(update_fields=['active_vouchers'])
        voucher.delete()
        return Response({'status':'Voucher Deleted'})
    

@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def transaction_details(request,pk):
    try:
        transaction = Transactions.objects.get(txn_id=pk)
    except Exception as e:
            return Response({'status':' Transaction ID not found'})

    if request.method=='GET':
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    elif request.method=='PUT':
        serializer = TransactionSerializer(transaction,data=request.data,partial=True)
        if serializer.is_valid():
              serializer.save()
              return Response({'status':'Data Updated'})
        return Response({'status':serializer.errors})
    
    elif request.method=='DELETE':
         transaction.delete()
         return Response({'status':'Transaction Deleted'})
    

@api_view(['GET','PUT','POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def ChatView(request):
     if request.method == 'GET':
          try:
            chats       = chat.objects.all()
            serializer  = ChatSerializer(chats,many=True)
            return Response(serializer.data)
          except Exception as e:
               return Response({'status':str(e)})
     elif request.method == 'PUT':
          chats = chat.objects.get(chat_id=request.data['chat_id'])
          serializer = ChatSerializer(chats,data=request.data,partial=True)
          if serializer.is_valid():
            serializer.save()
            return Response({'status':'Chat Marked as Read'})
          return Response({'status':serializer.errors})
     elif request.method=='POST':
          try:
            serializer = ChatSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':'chat created'})
            return Response({'status':serializer.errors})
          except Exception as e:
               return Response({'status':str(e)})
          

@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def user_details(request,pk):
    try:
        user = Users.objects.get(email=pk)
    except Exception as e:
            return Response({'status':' User not found'})

    if request.method=='GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method=='PUT':
        serializer = UserSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
              serializer.save()
              return Response({'status':'Data Updated'})
        return Response({'status':serializer.errors})
    
    elif request.method=='DELETE':
         user.delete()
         return Response({'status':'User Deleted'})
    

@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([JWTAuthentication,TokenAuthentication])
def station_details(request,pk):
    try:
        station = Station.objects.get(station_id=pk)
    except Exception as e:
            return Response({'status':' Station not found'})

    if request.method=='GET':
        serializer = StationSerializer(station)
        return Response(serializer.data)

    elif request.method=='PUT':
        serializer = StationSerializer(station,data=request.data,partial=True)
        if serializer.is_valid():
              serializer.save()
              return Response({'status':'Data Updated'})
        return Response({'status':serializer.errors})
    
    elif request.method=='DELETE':
         station.delete()
         return Response({'status':'User Deleted'})