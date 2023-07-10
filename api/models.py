from django.db import models
from django.utils import timezone
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'attendant_{0}/{1}'.format(instance.atdt_id, filename)
# Create your models here.
class Station(models.Model):
    station_id      = models.AutoField(primary_key=True)
    location        = models.CharField(max_length=100,blank=True,null=True)
    station_name    = models.CharField(max_length=300,blank=False) 
    email           = models.EmailField(max_length=100,blank=False)
    phone           = models.CharField(max_length=100,blank=False)
    fuel_type       = models.CharField(max_length=100,blank=False)
    operated_hours  = models.CharField(max_length=100,blank=False)
    created_time    = models.DateTimeField(default=timezone.now,blank=True) 

class Attendant(models.Model):
    atdt_id         = models.AutoField(primary_key=True)
    first_name      = models.CharField(max_length=200,blank=False)
    last_name       = models.CharField(max_length=200,blank=False)
    date_of_birth   = models.DateField(null=True,blank=False)
    employee_id     = models.CharField(max_length=200,blank=False)
    location_id     = models.CharField(max_length=200,null=True,blank=True)
    password        = models.CharField(max_length=400,blank=False)
    vouchers        = models.IntegerField(default=0,blank=True)
    profile         = models.ImageField(upload_to=user_directory_path,null=True,blank=True)
    created_by      = models.CharField(max_length=100,null=True,blank=True)
    modified_by     = models.CharField(max_length=100,null=True,blank=True)
    department      = models.CharField(max_length=100,default="NA")
    station_id      = models.ForeignKey(Station,on_delete=models.DO_NOTHING,blank=True,null=True)
    created_time    = models.DateTimeField(default=timezone.now,blank=True) 

    def __str__(self) -> str:
        return str(self.atdt_id)

class ClientMaster(models.Model):
    client_id           = models.AutoField(primary_key=True)
    client_name         = models.CharField(max_length=200,blank=False) 
    address             = models.CharField(max_length=400,blank=False,default='c_addr') 
    contact_name        = models.CharField(max_length=400,blank=False,default='c_name')
    contact_no          = models.CharField(max_length=400,blank=False,default='c_no')
    active_vouchers     = models.IntegerField(default=0,null=True,blank=True)
    used_vouchers       = models.IntegerField(default=0,null=True,blank=True)
    last_order_date     = models.DateField(default=None,blank=True,null=True)
    last_order_amount   = models.IntegerField(default=0,blank=True)
    created_by          = models.CharField(max_length=100,null=True,blank=True)
    modified_by         = models.CharField(max_length=100,null=True,blank=True)
    created_time    = models.DateTimeField(default=timezone.now,blank=True) 

    def __str__(self) -> str:
        return str(self.client_id)

class Voucher(models.Model):
    voucher_id          = models.CharField(primary_key=True,max_length=100)
    initial_amount      = models.BigIntegerField(blank=False)
    balance             = models.BigIntegerField(blank=False)
    last_used           = models.DateField(blank=True,null=True,default=None)
    last_transaction_id = models.CharField(max_length=200,blank=True,null=True,default=None)
    start_date          = models.DateField(blank=False)
    end_date            = models.DateField(blank=False)
    client_id           = models.ForeignKey(ClientMaster,on_delete=models.CASCADE)
    status              = models.CharField(max_length=1,default='A')
    created_by          = models.CharField(max_length=100,null=True,blank=True)
    modified_by         = models.CharField(max_length=100,null=True,blank=True)
    created_time    = models.DateTimeField(default=timezone.now,blank=True) 

    def __str__(self) -> str:
        return str(self.voucher_id)

class Transactions(models.Model):
    txn_date        = models.DateTimeField(default=timezone.now,blank=True)
    txn_id          = models.AutoField(primary_key=True) 
    initial_amount  = models.BigIntegerField(blank=False)
    redeem_amount   = models.BigIntegerField(blank=False)
    left_balance    = models.BigIntegerField(null=True,blank=True)
    Voucher_id      = models.ForeignKey(Voucher,on_delete=models.CASCADE,blank=False)
    id              = models.ForeignKey(Attendant,on_delete=models.CASCADE,blank=False)

  

    def __str__(self) -> str:
        return str(self.txn_id)
    


class AccessLogModel(models.Model):
    sys_id = models.AutoField(primary_key=True,null=False,blank=True)
    session_key = models.CharField(max_length=1024,null=False,blank=True)
    path =  models.CharField(max_length=1024,null=False,blank=True)
    method = models.CharField(max_length=8,null=False,blank=True)
    data = models.TextField(null=True,blank=True)
    ip_address = models.CharField(max_length=45,null=False,blank=True)
    referrer = models.CharField(max_length=512,null=True,blank=True)
    timestamp = models.DateTimeField(null=False,blank=True)
    user = models.CharField(max_length=100,null=True,blank=True)


class chat(models.Model):
    chat_id     = models.AutoField(primary_key=True)
    message     = models.CharField(max_length=400,blank=False,null=False)
    employee_id = models.CharField(max_length=200,blank=False)
    status      = models.CharField(max_length=1,default='U')
    created_at  = models.DateTimeField(default=timezone.now)


class Users(models.Model):
    email       = models.EmailField(primary_key=True,blank=False)
    name        = models.CharField(max_length=300,null=True,blank=True)
    phone       = models.CharField(max_length=30,null=True,blank=True)
    department  = models.CharField(max_length=100,null=False,blank=False)
    role        = models.CharField(max_length=100,null=False,blank=False)
    password    = models.CharField(max_length=200,null=False,blank=False)
    created_time    = models.DateTimeField(default=timezone.now,blank=True) 




    

    