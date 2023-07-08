from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("clients/", views.clientListAll, name="clientListAll"),
    path("attendants/", views.attendantListAll, name="attendantListAll"),
    path('vouchers/',views.voucherListAll,name='voucherListAll'),
    path('transactions/',views.transactionsListAll,name='transactionsListAll'),
    path('users/',views.UserListAll,name='UserListAll'),
    path('stations/',views.StationListAll,name='StationListAll'),
    path('createClient/',views.createClient,name='createClient'),
    path('createTransaction/',views.createTransaction,name='createTransaction'),
    path('createAttendant/',views.createAttendant,name='createAttendant'),
    path('createVoucher/',views.createVoucher,name='createVoucher'),
    path('createUser/',views.createUser,name='createUser'),
    path('createStation/',views.createStation,name='createStation'),
    path('vouchers/<str:pk>/',views.voucher_details,name='voucher_details'),
    path('client/<str:pk>/',views.client_details,name='client_details'),
    path('attendant/<str:pk>/',views.attendant_details,name='attendant_details'),
    path('transaction/<str:pk>/',views.transaction_details,name='transaction_details'),
    path('user/<str:pk>/',views.user_details,name='user_details'),
    path('station/<str:pk>/',views.station_details,name='station_details'),
    path('chat/',views.ChatView,name='ChatView'),
    path('stationFields/',views.StationFields,name='StationFields'),
    path('clientFields/',views.ClientFields,name='ClientFields'),
    path('transactionFields/',views.TransactionFields,name='TransactionFields'),
    path('attendantFields/',views.AttendantFields,name='AttendantFields'),
    path('voucherFields/',views.VoucherFields,name='VoucherFields'),
    path('userFields/',views.UserFields,name='UserFields')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)