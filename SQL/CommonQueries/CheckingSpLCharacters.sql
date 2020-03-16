/*$File_version=MS4.3.0.00$*/
/******************************************************************************/
/* Procedure					: wms_cmn_splchar_chk			 */
/* Description					: 								 */
/******************************************************************************/
/* Project						: 								 */
/* EcrNo						: 								 */
/* Version						: 								 */
/******************************************************************************/
/* Referenced					: 								 */
/* Tables						: 								 */
/******************************************************************************/
/* Development history			: 								 */
/******************************************************************************/
/* Author						: Sejal N Khimani				 */
/* Date							: Apr 19 2016 11:58AM			 */
/* Defect ID					: 14H109_LgtAdmin_00001						  */
/******************************************************************************/
/* Modification History			: 								 */
/******************************************************************************/
/* Modified By					: 								 */
/* Date							: 								 */
/* Description					: 								 */
/******************************************************************************/
create procedure wms_cmn_splchar_chk
		@ctxt_ouinstance   	udd_ctxt_ouinstance,   
		@ctxt_user         	udd_ctxt_user,   
		@ctxt_language     	udd_ctxt_language,   
		@ctxt_service      	udd_ctxt_service,  
		@string_in			udd_nvarcharmax,
		@errorid			udd_int output
as
begin		
	set nocount on
	
	select	@errorid	=	0
	
	declare @position			udd_int,
			@asciival_tmp		udd_int

	select @position = 1

	while @position <= len(@string_in)
	begin
		select @asciival_tmp = ascii(substring(@string_in, @position, 1))
		
  		if @asciival_tmp not between 97 and 122
			and @asciival_tmp not between 65 and 90
			and @asciival_tmp <> 32
		begin
			select	@errorid	=	1
		end 	
	   
	   select @position = @position + 1
	end
		
	set nocount off
	
end