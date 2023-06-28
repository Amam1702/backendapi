from django.shortcuts import render
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
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
        try:
            serializer = AttendantSerializer(data=request.data)
            new_user = User.objects.create_superuser(username=request.data['employee_id'],password=request.data['password'])
            if serializer.is_valid():
                serializer.save()
                token,created = Token.objects.get_or_create(user=new_user)
                return Response({'status':'Created Attendant'})
            else:
                 return Response({'status':serializer.errors})
        except Exception as e:
             return Response({'status':str(e)})

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
        """Authenticate user and create agent"""
        try:
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':'Created Client'})
            else:
                 return Response({'status':serializer.errors})
        except Exception as e:
              return Response({'status':str(e)})


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
                return Response({'status':'Created Transaction'})
            else:
                return Response(serializer.errors)
        except Exception as e:
             return Response({'status':str(e)})
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
def attendant_details(request,pk):
    try:
        atdt = Attendant.objects.get(attendant_id=pk)
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
         voucher.delete()
         return Response({'status':'Voucher Deleted'})
    

@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated, ))
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
    
""""""
@api_view(['POST'])
def employeeLogin(request):
        
        check = Attendant.objects.filter(employee_id=request.data['emp_id'],password=request.data['password'])
        serializer = AttendantSerializer(check)
        data = serializer.data
        print(data)
        if 'atdt_id' in data.keys():
            return Response({'status':'Verified'})
        else:
            return Response({'status':'Wrong Employee ID or password'})
    

     
     