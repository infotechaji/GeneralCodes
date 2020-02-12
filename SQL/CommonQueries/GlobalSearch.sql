
SELECT      
	TABLE_NAME AS  'TableName',COLUMN_NAME AS 'ColumnName'
            
FROM        INFORMATION_SCHEMA.COLUMNS
WHERE       COLUMN_NAME LIKE '%ro%no'
ORDER BY    TableName
            ,ColumnName;