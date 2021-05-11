
SELECT	unique_id,AVG(CAST(Price AS float)) 
--select *
FROM	DB1
where code = 'ABC'
and (enddate = '2021-09-30')
and effectivedate in ('2020-03-18','2020-03-17','2020-02-02')

GROUP BY unique_id
ORDER BY Unique_id desc




--SELECT DISTINCT  TOP 3 effectivedate
--						FROM	DB1
--						WHERE	code  = 'ABC' 
--						AND		(enddate = '2021-09-30')
--						GROUP BY	effectivedate,code
--						ORDER BY	effectivedate 
--						DESC)