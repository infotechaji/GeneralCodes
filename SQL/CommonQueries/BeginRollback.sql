create
--alter	
PROCEDURE	begin_tran
		@input_query					nvarchar(max)	
AS 
BEGIN
	SET NOCOUNT ON

	DECLARE @sql nvarchar(max)
	set @sql='BEGIN TRAN '+ CHAR(13)
	print (@input_query)
	--set @sql+=replace(@input_query,'''', '''''')
	set @sql+=@input_query
	set @sql+=CHAR(13)+'ROLLBACK TRAN '
	print (@sql)
	exec sp_executesql @sql
	
END 

--exec begin_tran 'select top 10 * from cso_master_view'


--select replace(,'''', '''''')