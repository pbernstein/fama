


select (IF(im.value -  (  select p.value from ins_map p where im.symbol = p.symbol and im.attribute = p.attribute and im.form = p.form and im.date_id > p.date_id order by date_id desc limit 1 ) > 0, 3, 2)) as direction
from ins_map im
where attribute in ('Cash') 
and
im.value <> 'NR' 
# There is a value for this attribute in the prior filing
and ( select p.value from ins_map p where im.symbol = p.symbol and im.attribute = p.attribute and im.form = p.form and im.date_id > p.date_id order by date_id desc limit 1    ) is not null
# No 8 - K filed
#and ( select eh_sk from extract_history where form = '8-K' and date_id = im.date_id and cik = im.cik  limit 1) is null
and im.eh_sk = template

