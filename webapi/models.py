from django.db import models
class Plan(models.Model):
    name = models.CharField(max_length=60)
    max_request = models.IntegerField() 
    allow_ip = models.TextField()
    max_ip = models.IntegerField()
    harga = models.IntegerField()
    expired = models.IntegerField()
    def __str__(self) -> str:
        return self.name

class User(models.Model):
    nama = models.TextField()
    email = models.TextField(null=True)
    picture = models.TextField()
    email_verfied = models.BooleanField() #akun verification status [True, False]
    phone_number = models.CharField(max_length=20, null=True)
    verified_token = models.CharField(max_length=256)
    password = models.TextField(max_length=256)
    #kuki  = models.CharField(max_length=256)
    expired = models.DateTimeField()
    apikey = models.CharField(max_length=256)
    plan_name = models.TextField()
    max_request = models.IntegerField()
    allow_ip = models.TextField()
    max_ip = models.IntegerField()
    req_counter = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.nama

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ua   = models.CharField(max_length=256)
    ip    = models.CharField(max_length=50)
    cookie_value = models.CharField(max_length=256) #Encrypted
    AccessToken = models.CharField(max_length=256) #Encrypted
    Action = models.JSONField() #[] -> [[timestamp, actionNum, ..args]]-> [[ts, aT],[ts, aT],...]
    def __str__(self) -> str:
        return self.ip

class DokumentasiKategori(models.Model):
    icon = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    def __str__(self) -> str:
        return self.name

class Dokumentasi(models.Model):
    categori = models.ForeignKey(DokumentasiKategori, on_delete=models.CASCADE)
    icon = models.CharField(max_length=30)
    title= models.CharField(max_length=50)
    title_panel = models.CharField(max_length=100)
    url_dokumentasi = models.CharField(max_length=30)
    example_ajax = models.JSONField()
    path_api = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.title

class CodeDocumentation(models.Model):
    language = models.CharField(max_length=64)
    language_code = models.CharField(max_length=50)
    code = models.TextField()
    api_name = models.ForeignKey(Dokumentasi, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.language

