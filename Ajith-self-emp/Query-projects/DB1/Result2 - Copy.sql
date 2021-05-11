
SELECT	DB1.unique_id,
		AVG(CAST(Price AS INT)) 
FROM	DB1
JOIN 
(SELECT  DISTINCT  TOP 3 effectivedate,DB1.unique_id
FROM	DB1
WHERE	code  = 'ABC' 
AND		(enddate = '2021-09-30')
GROUP BY	effectivedate,code,DB1.unique_id
ORDER BY	effectivedate 
DESC
)DB2
on	DB1.code = DB2.code
and DB1.effectivedate = DB2.effectivedate
GROUP BY Unique_id
ORDER BY DB1.unique_id desc