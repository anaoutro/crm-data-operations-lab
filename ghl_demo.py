import json
from pathlib import Path
p=Path(__file__).parent; events=json.loads((p/'ghl_events.json').read_text()); seen=set(); booked=set(); actions=[]
for event in events:
    if event['id'] in seen: continue
    seen.add(event['id']); email=event['email'].strip().lower()
    if event['type']=='booked':
        booked.add(email); actions=[a for a in actions if not(a['email']==email and a['action']=='nurture_email')]; actions.append({'email':email,'action':'appointment_reminder','due':'24h_before_appointment'}); continue
    if event['type']=='lead' and event.get('consent') and email not in booked:
        actions.append({'email':email,'action':'nurture_email','due':'next_business_day'})
    elif not event.get('consent'): actions.append({'email':email,'action':'manual_review_no_outbound'})
(p/'ghl_result.json').write_text(json.dumps({'actions':actions,'unique_events':len(seen)},indent=2),encoding='utf-8')
print(json.dumps({'actions':len(actions),'unique_events':len(seen)}))
