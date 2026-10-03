import csv, re
from pathlib import Path
p=Path(__file__).parent; accepted={}; exceptions=[]
for row in csv.DictReader((p/'zoho_contacts.csv').open(encoding='utf-8')):
    email=row['email'].strip().lower(); digits=re.sub(r'\D','',row['phone'])
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+",email):
        exceptions.append({'source_id':row['source_id'],'reason':'missing_or_invalid_email'}); continue
    if email in accepted:
        exceptions.append({'source_id':row['source_id'],'reason':'merged_duplicate','canonical_id':accepted[email]['source_id']}); continue
    accepted[email]={'source_id':row['source_id'],'name':row['name'].strip(),'email':email,'phone_digits':digits,'owner':row['owner'].strip()}
for filename,fields,rows in [('clean_contacts.csv',['source_id','name','email','phone_digits','owner'],accepted.values()),('exceptions.csv',['source_id','reason','canonical_id'],exceptions)]:
    with (p/filename).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
print({'accepted':len(accepted),'exceptions':len(exceptions)})
