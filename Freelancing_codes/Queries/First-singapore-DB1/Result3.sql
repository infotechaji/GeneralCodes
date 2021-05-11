--File version : 5.0


--Test case : 01
--declare @code nvarchar(30) = 'ABC'
--declare @enddate date = '2021-09-30'

--Test case : 02
declare @code nvarchar(30) = 'CVB'
declare @enddate date = null


SELECT		unique_id,effectivedate,AVG(CAST(Price AS float))  avg_price
FROM		DB1
WHERE		code = isnull(@code,code) AND enddate = isnull(@enddate,enddate)
AND			effectivedate in (SELECT DISTINCT top 3 effectivedate FROM DB1 WHERE code = isnull(@code,code) AND  enddate = isnull(@enddate,enddate) ORDER BY effectivedate DESC)
GROUP BY	unique_id,effectivedate
ORDER BY	effectivedate desc
