import csv, json, re
from pathlib import Path
p=Path(__file__).parent; leads={}; rejected=[]; audit=[]
for row in csv.DictReader((p/'hubspot_leads.csv').open(encoding='utf-8')):
    email=row['email'].strip().lower()
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+",email):
        rejected.append({'row':row,'reason':'invalid_email'}); continue
    score=(40 if row['requested_demo'].strip().lower()=='yes' else 0)+(25 if int(row['company_size'])>=20 else 0)+(10 if row['source']=='website' else 0)
    if email in leads:
        old=leads[email]; old['score']=max(old['score'],score); old['sources']=sorted(set(old['sources']+[row['source']])); audit.append({'email':email,'action':'merged_duplicate'})
    else: leads[email]={'name':row['name'].strip(),'email':email,'score':score,'sources':[row['source']]}
for lead in leads.values(): lead['owner']='sales_priority' if lead['score']>=40 else 'sales_general'
out={'contacts':list(leads.values()),'rejected':rejected,'audit':audit}
(p/'hubspot_result.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'contacts':len(leads),'rejected':len(rejected),'merged':len(audit)}))
