create
alter  procedure calculate_age(@input_date as date )
as 
select DATEDIFF(year,cast(@input_date as date),cast(getdate() as date)) age 

exec calculate_age'1995-11-05'
select cast(getdate() as date)

select DATEDIFF(year,'1995-11-05',cast(getdate() as date))

DATEDIFF(month, '2017/08/25', '2011/08/25') AS DateDiff;



