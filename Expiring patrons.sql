--query used to populate an expiring card notification e-mail to patrons whose card will expire in 30 days
--generated via Expiring patrons.py script
--Author: Jeremy Goldstein
--Contact Info: jgoldstein@minlib.net

SELECT
min(n.first_name),
min(n.last_name),
min(v.field_content) as email,
to_char(p.expiration_date_gmt,'Mon DD, YYYY'),
p.id
FROM
sierra_view.patron_view as p
JOIN		
sierra_view.varfield v		
ON		
p.id = v.record_id and v.varfield_type_code = 'z'
JOIN
sierra_view.patron_record_fullname n
ON
p.id = n.patron_record_id
WHERE
p.expiration_date_gmt::date = (localtimestamp::date + interval '30 days')
--Use for testing
--AND p.barcode in ('','')

--limit by ptype, gmail stops sending e-mails if too many go through at once
--so we run 4 iterations of this script with different ptype ranges
--and run them 15 minutes apart
AND p.ptype_code IN('1', '2', '3', '4', '5', '6', '8', '10', '11', '12', '110') 

group by 5, 4
