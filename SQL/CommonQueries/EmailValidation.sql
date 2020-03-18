/*$file_version=ms4.3.0.01$*/  
/**********************************************************************************************/
/* procedure					: cmn_sp_email_validation									  */
/* description					:															  */
/**********************************************************************************************/
/* project						:															  */
/* ecrno						: 															  */
/* version						: 															  */
/**********************************************************************************************/
/* referenced					: 															  */
/* tables						: 															  */
/**********************************************************************************************/
/* development history			: 															  */
/**********************************************************************************************/
/* author						: bharath a													  */
/* date							: june 7 2011  11:54am										  */
/* purpose						: 															  */
/**********************************************************************************************/
/* modification history			: 															  */
/**********************************************************************************************/
/*MANIK    30-11-2017           CAM-825     												  */

create procedure cmn_sp_email_validation
	@ctxt_ouinstance 	udd_ctxt_ouinstance,
	@ctxt_user       	udd_ctxt_user,
	@ctxt_language   	udd_ctxt_language,
	@ctxt_service    	udd_ctxt_service,
	--@emailid        	email,--code commented for CAM-825 
	@emailid        	udd_desc255, --code added for CAM-825	
	@m_errorid       	udd_int output --to return execution status
as
begin
-- nocount should be switched on to prevent phantom rows
	set nocount on
	-- @m_errorid should be 0 to indicate success
	select @m_errorid = 0

	--declaration of temporary variables


	--temporary and formal parameters mapping

	select @ctxt_user        = ltrim(rtrim(@ctxt_user))
	select @ctxt_service     = ltrim(rtrim(@ctxt_service))

	--null checking

	if @ctxt_ouinstance = -915
		select @ctxt_ouinstance = null  

	if @ctxt_user = '~#~' 
		select @ctxt_user = null  

	if @ctxt_language = -915
		select @ctxt_language = null  

	if @ctxt_service = '~#~' 
		select @ctxt_service = null  

	if @emailid = '~#~' 
		select @emailid = null  
	
	if @emailid is null
	begin
		return
	end
	
	 /*code commented for CAM-825 starts here*/ 
	/*
	if charindex('@',@emailid) = 0  or charindex('.',@emailid)  = 0 
	begin
		--'Enter Vaid Email at row no "%d".
		select @m_errorid = 107
		return
	end
	if   charindex(' ',ltrim(rtrim(@emailid))) <> 0 
	begin
		 --Embedded spaces can''t be allowed of an email at row no "%d".
		 select @m_errorid = 101
		 return
	end 
	if   left(ltrim(@emailid),1) = '@'  
	begin
		 --''@'' can''t be the first character of an email at row no "%d".
		 select @m_errorid = 102
		 return
	end
	if	 right(rtrim(@emailid),1) = '.' 
	begin
		 --''.'' can''t be the last character of an email at row no "%d".
		 select @m_errorid = 103
		 return
	end 
	if	 len(ltrim(rtrim(@emailid))) - len(replace(ltrim(rtrim(@emailid)),'@','')) <> 1 
	begin
		 --Only one ''@'' sign is allowed of an email at row no "%d".
		 select @m_errorid = 104
 		 return
	end	
	if	 (charindex('.@',@emailid) <> 0 or charindex('..',@emailid) <> 0 or charindex('@.',@emailid) <> 0) 
	begin
		 --Can''t have patterns like ''.@'' and ''.'' and ''@.'' of an email at row no "%d".
		 select @m_errorid = 106
		 return
	end
	if	 (charindex('.',reverse(ltrim(rtrim(@emailid)))) not between 3 and 4) 
	begin
		 --Domain name should end with at least 2 character extension of an email at row no "%d".
		 select @m_errorid = 105
 		 return
	end	 */	 
    /*code commented for CAM-825 ends here*/ 
	

	  /*code added for CAM-825 starts here*/	
	declare	@i				udd_int,
			@j				udd_int,
			@x				udd_int,
			@emailid_tmp	udd_desc255

	if	(len(@emailid)	-	len(replace(@emailid,';','')))	=	0
	begin
	/*02_09_2017_B	B_E*/

		if charindex('@',@emailid) = 0  or charindex('.',@emailid)  = 0 
		begin
			--'Enter Vaid Email at row no "%d".
			select @m_errorid = 107
			return
		end
		if   charindex(' ',ltrim(rtrim(@emailid))) <> 0 
		begin
			 --Embedded spaces can''t be allowed of an email at row no "%d".
			 select @m_errorid = 101
			 return
		end 
		if   left(ltrim(@emailid),1) = '@'  
		begin
			 --''@'' can''t be the first character of an email at row no "%d".
			 select @m_errorid = 102
			 return
		end
		if	 right(rtrim(@emailid),1) = '.' 
		begin
			 --''.'' can''t be the last character of an email at row no "%d".
			 select @m_errorid = 103
			 return
		end 
		if	 len(ltrim(rtrim(@emailid))) - len(replace(ltrim(rtrim(@emailid)),'@','')) <> 1 
		begin
			 --Only one ''@'' sign is allowed of an email at row no "%d".
			 select @m_errorid = 104
 			 return
		end	
		if	 (charindex('.@',@emailid) <> 0 or charindex('..',@emailid) <> 0 or charindex('@.',@emailid) <> 0) 
		begin
			 --Can''t have patterns like ''.@'' and ''.'' and ''@.'' of an email at row no "%d".
			 select @m_errorid = 106
			 return
		end
		if	 (charindex('.',reverse(ltrim(rtrim(@emailid)))) not between 3 and 4) 
		begin
			 --Domain name should end with at least 2 character extension of an email at row no "%d".
			 select @m_errorid = 105
 			 return
		end	 	
	/*02_09_2017_B	B_B*/
	end	--if	(len(@emailid)	-	len(replace(@emailid,';','')))	=	0
	else	
	begin
		 	
		select	@x	=	(len(@emailid)	-	len(replace(@emailid,';','')))+1
		select	@i	=	1

		while	@i	<=	@x
		begin
			 
			if	@i	=	1	
			begin

				select	@j	=	1	
				select	@j	=	charindex(';',@emailid)
				select	@emailid_tmp	=	substring(@emailid,@i,(@j-1))
				--select	@emailid_tmp '@emailid_tmp1'
			end	
			else	if	@i	<	@x
			begin
	
				select	@emailid_tmp	=	substring(@emailid,@j+1, charindex(';',@emailid,@j+1)-@j-1)
				select	@j	=	charindex(';',@emailid,@j+1)
				--select	@emailid_tmp '@emailid_tmp2'
				
			end	
			else	if	@i	=	@x
			begin
	
				select	@emailid_tmp	=	substring(@emailid,@j+1,len(@emailid))
				select	@j	=	charindex(';',@emailid,@j+1)
				--select	@emailid_tmp '@emailid_tmp3'
				
			end	
			
			if	isnull(@emailid_tmp,'')<>''
			begin

				if charindex('@',@emailid_tmp) = 0  or charindex('.',@emailid_tmp)  = 0 
				begin
					--'Enter Vaid Email at row no "%d".
					select @m_errorid = 107
					break;
				end
				if   charindex(' ',ltrim(rtrim(@emailid_tmp))) <> 0 
				begin
						--Embedded spaces can''t be allowed of an email at row no "%d".
						select @m_errorid = 101
						break;
				end 
				if   left(ltrim(@emailid_tmp),1) = '@'  
				begin
						--''@'' can''t be the first character of an email at row no "%d".
						select @m_errorid = 102
						break;
				end
				if	 right(rtrim(@emailid_tmp),1) = '.' 
				begin
						--''.'' can''t be the last character of an email at row no "%d".
						select @m_errorid = 103
						break;
				end 
				if	 len(ltrim(rtrim(@emailid_tmp))) - len(replace(ltrim(rtrim(@emailid_tmp)),'@','')) <> 1 
				begin
						--Only one ''@'' sign is allowed of an email at row no "%d".
						select @m_errorid = 104
						break;
				end	
				if	 (charindex('.@',@emailid_tmp) <> 0 or charindex('..',@emailid_tmp) <> 0 or charindex('@.',@emailid_tmp) <> 0) 
				begin
						--Can''t have patterns like ''.@'' and ''.'' and ''@.'' of an email at row no "%d".
						select @m_errorid = 106
						break;
				end
				if	 (charindex('.',reverse(ltrim(rtrim(@emailid_tmp)))) not between 3 and 4) 
				begin
						--Domain name should end with at least 2 character extension of an email at row no "%d".
						select @m_errorid = 105
						break;
				end	 	

			end	 	

			select	@i	=	@i	+	1	

		end	

 		if	@m_errorid	<>	0	
		begin

			return

		end	
	end	
	/*02_09_2017_B	B_E*/
	  /*code added for CAM-825 ends here*/
	
set nocount off

end