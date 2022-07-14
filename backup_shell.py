from sys import stderr
from webapi.models import User, Session, Plan, Dokumentasi, DokumentasiKategori, CodeDocumentation
execs ='''from webapi.models import User, Session, Plan, Dokumentasi, DokumentasiKategori,CodeDocumentation\n
from pytz import UTC
import datetime
class RelationShipBackup:
    def __init__(self, db,**kwargs) -> None:
        self.id = kwargs.pop('id')
        self.db = db(**kwargs)
        self.db.save()
'''
# User Backup
stderr.writelines('Backup User\n')
stderr.flush()
user =[]
for i in User.objects.all():
    i: User = i
    user.append({'id':i.id, 'nama':i.nama, 'email':i.email, 'picture':i.picture, 'email_verfied':i.email_verfied, 'phone_number':i.phone_number, 'verified_token':i.verified_token, 'password':i.password, 'expired':i.expired.timestamp(), 'apikey':i.apikey, 'plan_name':i.plan_name, 'max_request':i.max_request, 'allow_ip':i.allow_ip, 'max_ip':i.max_ip, 'req_counter':i.req_counter})

execs+=f'''
\nuser = []
print('RESTORE USER')
for i in {user}:
    i['expired'] = datetime.datetime.fromtimestamp(i['expired'], tz=UTC)
    user.append(RelationShipBackup(db=User,**i))

'''

stderr.writelines('Backup Session\n')
stderr.flush()
session = []
for ses in Session.objects.all():
    ses: Session = ses
    session.append({'id':ses.id,'user':ses.user.id, 'ua':ses.ua, 'ip':ses.ip, 'cookie_value':ses.cookie_value,'AccessToken':ses.AccessToken, 'Action':ses.Action})

execs+=f'''\n
print('RESTORE SESSION')
backup = []
for i in {session}:
    i['user'] = list(filter(lambda x: x.id == i['user'], user))[0].db
    backup.append(RelationShipBackup(db=Session,**i))
'''

stderr.writelines('Backup Plan\n')
stderr.flush()
plan = []
for pla in Plan.objects.all():
    pla:Plan=pla
    plan.append({'id':pla.id, 'name':pla.name, 'max_request':pla.max_request, 'allow_ip':pla.allow_ip, 'max_ip':pla.max_ip, 'harga':pla.harga, 'expired':pla.expired})

execs+=f'''
print('RESTORE PLAN')
plan = []
for i in {plan}:
    plan.append(RelationShipBackup(db=Plan, **i))


'''
stderr.writelines('Backup Dokumentasi Kategori\n')
stderr.flush()
dkategori = []
for kt in DokumentasiKategori.objects.all():
    dkategori.append({'id':kt.id,'icon':kt.icon, 'name':kt.name})

execs+=f'''
print('RESTORE DOKUMENTASI KATEGORI')
dkategori = []
for i in {dkategori}:
    dkategori.append(RelationShipBackup(db=DokumentasiKategori, **i))

'''
stderr.writelines('backup dokumntasi\n')
stderr.flush()
dokumentasi = []
for dkt in Dokumentasi.objects.all():
    dkt: Dokumentasi = dkt
    dokumentasi.append({'id':dkt.id, 'icon':dkt.icon, 'categori':dkt.categori.id, 'example_ajax':dkt.example_ajax, 'path_api':dkt.path_api, 'title':dkt.title, 'title_panel':dkt.title_panel, 'url_dokumentasi':dkt.url_dokumentasi})

execs+=f'''
print('RESTORE DOKUMENTASI')
dokumentasi = []
for i in {dokumentasi}:
    i['categori'] = list(filter(lambda x:i['categori'] == x.id, dkategori))[0].db
    dokumentasi.append(RelationShipBackup(db=Dokumentasi, **i))
'''

stderr.writelines('Backup CodeDocumentation\n')
stderr.flush()
cdokumentasi = []
for cd in CodeDocumentation.objects.all():
    cd: CodeDocumentation = cd
    cdokumentasi.append({'id':cd.id, 'api_name':cd.api_name.id, 'code':cd.code, 'language':cd.language, 'language_code':cd.language_code})

stderr.writelines('Backup Dokumentasi\n')
stderr.flush()
execs+=f'''
print('RESTORE CODE DOKUMENTASI')
cdokumentasi = []
for i in {cdokumentasi}:
    i['api_name'] = list(filter(lambda x:i['api_name'] == x.id, dokumentasi))[0].db
    cdokumentasi.append(RelationShipBackup(db=CodeDocumentation, **i))
    '''

print(execs)