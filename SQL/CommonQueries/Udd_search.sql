select top 10 * from sys.types
where is_user_defined = 1
and name like  'udd%date'