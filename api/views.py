from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import *
from api.serializers import *
from django.utils import timezone
from datetime import datetime
# Create your views here.



"""All Create API Functions"""
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def createAttendant(request):
        """Authenticate and Create client """
        try:
            serializer = AttendantSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                 return Response(serializer.errors)
        except Exception as e:
             return Response({'status':str(e)})

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def createVoucher(request):
        """Authenticate user and create agent"""
        try:
            serializer = VoucherSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                client = ClientMaster.objects.get(client_id=request.data['client_id'])
                client.active_vouchers = client.active_vouchers+1
                client.save(update_fields=['active_vouchers'])
                return Response(serializer.data)
            else:
                 return Response(serializer.errors)
        except Exception as e:
              return Response({'status':str(e)})

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def createClient(request):
        """Authenticate user and create agent"""
        try:
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                 return Response(serializer.errors)
        except Exception as e:
              return Response({'status':str(e)})


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
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
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except Exception as e:
             return Response({'status':str(e)})
""""""

"""All Retrieve API Functions"""
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def clientListAll(request):
        """Display all the clients from database"""
        clients = ClientMaster.objects.all()
        serializer = AttendantSerializer(clients,many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def attendantListAll(request):
        """Display all the clients from database"""
        attendants = Attendant.objects.all()
        serializer = AttendantSerializer(attendants,many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def voucherListAll(request):
        """Display all the clients from database"""
        vouchers = Voucher.objects.all()
        serializer = VoucherSerializer(vouchers,many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def transactionsListAll(request):
        """Display all the clients from database"""
        transactions = Transactions.objects.all()
        serializer = TransactionSerializer(transactions,many=True)
        return Response(serializer.data)
""""""

"""GET by ID,Update By ID,Delete by ID"""
@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated, ))
def client_details(request,pk):
    try:
        client = ClientMaster.objects.get(client_id=pk)
    except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    elif request.method=='PUT':
        serializer = ClientSerializer(client,data=request.data)
        if serializer.is_valid():
              serializer.save()
              return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='DELETE':
         client.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated, ))
def attendant_details(request,pk):
    try:
        atdt = Attendant.objects.get(attendant_id=pk)
    except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer = AttendantSerializer(atdt)
        return Response(serializer.data)

    elif request.method=='PUT':
        serializer = AttendantSerializer(atdt,data=request.data)
        if serializer.is_valid():
              serializer.save()
              return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
         atdt.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated, ))
def voucher_details(request,pk):
    try:
        voucher = Voucher.objects.get(voucher_id=pk)
    except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer = VoucherSerializer(voucher)
        return Response(serializer.data)

    elif request.method=='PUT':
        serializer = VoucherSerializer(voucher,data=request.data)
        if serializer.is_valid():
              serializer.save()
              return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='DELETE':
         voucher.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated, ))
def transaction_details(request,pk):
    try:
        transaction = Transactions.objects.get(txn_id=pk)
    except Exception as e:
            return Response({'status':'Incorrect transaction ID'},status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    elif request.method=='PUT':
        serializer = TransactionSerializer(transaction,data=request.data)
        if serializer.is_valid():
              serializer.save()
              return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='DELETE':
         transaction.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)
    
""""""