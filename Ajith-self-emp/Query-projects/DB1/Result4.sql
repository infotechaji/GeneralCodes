--File version : 4.0

declare @code nvarchar(30) = 'ABC'
declare @enddate date = '2021-09-30'

SELECT		unique_id,effectivedate,AVG(CAST(Price AS float))  avg_price
FROM		DB1
WHERE		code = @code AND  (enddate = @enddate)
AND			effectivedate in (SELECT DISTINCT top 3 effectivedate FROM DB1 WHERE code = @code AND  enddate = @enddate ORDER BY effectivedate DESC)
GROUP BY	unique_id,effectivedate
ORDER BY	effectivedate desc




