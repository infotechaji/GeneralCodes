
cDB1

SELECT	Unique_id,	Price,	code,
		enddate,	effectivedate
from  DB1
where code = 'ABC'




SELECT	Unique_id,effectivedate,	avg(cast(Price as int))
from  DB1
where code = 'ABC' and ( enddate = '2021-09-30')
group by unique_id,effectivedate
order by effectivedate desc





select Unique_id,effectivedate,avg(cast(Price as int)) from DB1
group by Unique_id,effectivedate
order by effectivedate desc

select  Unique_id,code,effectivedate,enddate
from DB1





SELECT	DB1.unique_id,
		AVG(CAST(Price AS INT)) 
FROM	DB1
JOIN 
(SELECT  DISTINCT  TOP 3 effectivedate,code
FROM	DB1
WHERE	code  = 'ABC' 
AND		(enddate = '2021-09-30')
GROUP BY	effectivedate,code
ORDER BY	effectivedate 
DESC
)DB2
on	DB1.code = DB2.code
and DB1.effectivedate = DB2.effectivedate
GROUP BY Unique_id
ORDER BY DB1.unique_id desc







select distinct top 3 effectivedate,code
from DB1
where code  = 'ABC'
group by effectivedate,code,unique_id
order by effectivedate desc


