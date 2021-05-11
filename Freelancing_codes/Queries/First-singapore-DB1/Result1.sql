SELECT	DB1.unique_id,	DB1.effectivedate,
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
GROUP BY Unique_id,DB1.effectivedate
ORDER BY DB1.effectivedate desc