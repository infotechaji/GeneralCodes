ALTER FUNCTION get_serial_lot
(
@serial_no VARCHAR(200),
@lot_no VARCHAR(200)
)
RETURNS VARCHAR(200)
AS
BEGIN

IF dbo.trm(@serial_no)is not null and dbo.trm(@serial_no) !='##' and len(dbo.trm(@serial_no))>2
	RETURN dbo.trm(@serial_no)
ELSE IF dbo.trm(@lot_no)is not null and dbo.trm(@lot_no) !='##' and len(dbo.trm(@lot_no))>2
	RETURN dbo.trm(@lot_no)
ELSE
	RETURN null
RETURN 1
END


select dbo.get_serial_lot('##','12345')
select dbo.get_serial_lot('12345','##')
select dbo.get_serial_lot('##','##')
select dbo.get_serial_lot('','')