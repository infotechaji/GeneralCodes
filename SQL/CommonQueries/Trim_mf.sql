CREATE FUNCTION trm
(
--string need to format
@string VARCHAR(200)--increase the variable size depending on your needs.
)
RETURNS VARCHAR(200)
AS
BEGIN
RETURN ltrim(rtrim(@string))
END

--Declare Variables

len(dbo.trm('ajith'))
len(dbo.trm(' a j i t h '))
len(dbo.trm('ajith                '))
len(dbo.trm('              ajith'))