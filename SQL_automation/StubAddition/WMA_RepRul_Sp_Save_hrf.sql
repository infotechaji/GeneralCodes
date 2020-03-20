-- added 
/*$File_version=ms4.3.0.01$*/
/******************************************************************************/
/* procedure					: wma_reprul_sp_save_hrf					  */
/* description					: 											  */
/******************************************************************************/
/* project						: 								 			  */
/* ecrno						: 								 			  */
/* version						: 								 			  */
/******************************************************************************/
/* referenced					: 								 			  */
/* tables						: 								 			  */
/******************************************************************************/
/* Development history			: EPE-14970							          */
/******************************************************************************/
/* Author						: Sangeetha M								  */
/* Date							: Jul 16 2019  10:17 PM						  */
/******************************************************************************/
/* modification history			: 											  */
/* Sangeetha M					13 Aug 2019					LRT-1094		  */
/* Anupriya S					25 Jan 2020					LRT-3129		  */
/* Ajithkumar M					10 Mar 2020					EPE-18934		  */
/******************************************************************************/

create procedure wma_reprul_sp_save_hrf
	@ctxt_ouinstance    	udd_ctxt_ouinstance,  
	@ctxt_user          	udd_ctxt_user,  
	@ctxt_language      	udd_ctxt_language,  
	@ctxt_service       	udd_ctxt_service,  
	@alloc_rule         	udd_desc255, 
	@critical_check     	udd_hrint, 
	@hdnguid            	udd_desc255, 
	@hdnhiddencontrol1  	udd_desc255, 
	@hdnhiddencontrol2  	udd_desc255, 
	@hdntimestamp       	udd_timestamp, 
	@lines_per_plan     	udd_lineno, 
	@open_orders        	udd_desc255, 
	@order_date_combo   	udd_desc255, 
	@order_date_combo2  	udd_desc255, 
	@order_date_edit    	udd_hrint, 
	@order_date_range_1 	udd_date, 
	@order_date_range_2 	udd_date, 
	@order_time_base    	udd_hrint, 
	@replenish_plan     	udd_desc255, 
	@unlock_odo         	udd_hrint, 
	@wv_replenish_hdn1  	udd_desc255, 
	@wv_replenish_hdn10 	udd_desc255, 
	@wv_replenish_hdn2  	udd_desc255, 
	@wv_replenish_hdn3  	udd_desc255, 
	@wv_replenish_hdn4  	udd_desc255, 
	@wv_replenish_hdn5  	udd_desc255, 
	@wv_replenish_hdn6  	udd_desc255, 
	@wv_replenish_hdn7  	udd_desc255, 
	@wv_replenish_hdn8  	udd_desc255, 
	@wv_replenish_hdn9  	udd_desc255, 
	@zone_rule          	udd_hrint,
	@auto_short_close_order udd_hrint,--Code added for LRT-3129
	@demand_replenish		udd_hrint,--Code added for LRT-312
	@enble_dmnd_based_rep	udd_hrint,--Code added for EPE-18934
	@m_errorid          	udd_int output --to return execution status
as
begin
	-- nocount should be switched on to prevent phantom rows
	set nocount on
	-- @m_errorid should be 0 to indicate success
	set @m_errorid = 0

	--declaration of temporary variables
	declare	@exists_flag				udd_flag,
			@sysdate					udd_date,
			@order_date_combo_tmp		udd_code,
			@order_date_combo2_tmp		udd_code,
			@replenish_plan_tmp			udd_code,
			@alloc_rule_tmp				udd_code

	--temporary and formal parameters mapping

	select @ctxt_user           = ltrim(rtrim(@ctxt_user))
	select @ctxt_service        = ltrim(rtrim(@ctxt_service))
	select @alloc_rule          = ltrim(rtrim(@alloc_rule))
	select @hdnguid             = ltrim(rtrim(@hdnguid))
	select @hdnhiddencontrol1   = ltrim(rtrim(@hdnhiddencontrol1))
	select @hdnhiddencontrol2   = ltrim(rtrim(@hdnhiddencontrol2))
	select @open_orders         = ltrim(rtrim(@open_orders))
	select @order_date_combo    = ltrim(rtrim(@order_date_combo))
	select @order_date_combo2   = ltrim(rtrim(@order_date_combo2))
	select @replenish_plan      = ltrim(rtrim(@replenish_plan))
	select @wv_replenish_hdn1   = ltrim(rtrim(@wv_replenish_hdn1))
	select @wv_replenish_hdn10  = ltrim(rtrim(@wv_replenish_hdn10))
	select @wv_replenish_hdn2   = ltrim(rtrim(@wv_replenish_hdn2))
	select @wv_replenish_hdn3   = ltrim(rtrim(@wv_replenish_hdn3))
	select @wv_replenish_hdn4   = ltrim(rtrim(@wv_replenish_hdn4))
	select @wv_replenish_hdn5   = ltrim(rtrim(@wv_replenish_hdn5))
	select @wv_replenish_hdn6   = ltrim(rtrim(@wv_replenish_hdn6))
	select @wv_replenish_hdn7   = ltrim(rtrim(@wv_replenish_hdn7))
	select @wv_replenish_hdn8   = ltrim(rtrim(@wv_replenish_hdn8))
	select @wv_replenish_hdn9   = ltrim(rtrim(@wv_replenish_hdn9))

	--null checking

	if @ctxt_ouinstance = -915
		select @ctxt_ouinstance = null  

	if @ctxt_user = '~#~' 
		select @ctxt_user = null  

	if @ctxt_language = -915
		select @ctxt_language = null  

	if @ctxt_service = '~#~' 
		select @ctxt_service = null  

	if @alloc_rule in ('~#~' ,'')
		select @alloc_rule = null  

	if @critical_check = -915
		select @critical_check = null  

	if @hdnguid = '~#~' 
		select @hdnguid = null  

	if @hdnhiddencontrol1 = '~#~' 
		select @hdnhiddencontrol1 = null  

	if @hdnhiddencontrol2 = '~#~' 
		select @hdnhiddencontrol2 = null  

	if @hdntimestamp = -915
		select @hdntimestamp = null  

	if @lines_per_plan = -915
		select @lines_per_plan = null  

	if @open_orders = '~#~' 
		select @open_orders = null  

	if @order_date_combo in ('~#~' ,'')
		select @order_date_combo = null  

	if @order_date_combo2 in ('~#~' ,'')
		select @order_date_combo2 = null  

	if @order_date_edit = -915
		select @order_date_edit = null  

	if @order_date_range_1 = '01/01/1900' 
		select @order_date_range_1 = null  

	if @order_date_range_2 = '01/01/1900' 
		select @order_date_range_2 = null  

	if @order_time_base = -915
		select @order_time_base = null  

	if @replenish_plan in ('~#~','')
		select @replenish_plan = null  

	if @unlock_odo = -915
		select @unlock_odo = null  

	if @wv_replenish_hdn1 = '~#~' 
		select @wv_replenish_hdn1 = null  

	if @wv_replenish_hdn10 = '~#~' 
		select @wv_replenish_hdn10 = null  

	if @wv_replenish_hdn2 = '~#~' 
		select @wv_replenish_hdn2 = null  

	if @wv_replenish_hdn3 = '~#~' 
		select @wv_replenish_hdn3 = null  

	if @wv_replenish_hdn4 = '~#~' 
		select @wv_replenish_hdn4 = null  

	if @wv_replenish_hdn5 = '~#~' 
		select @wv_replenish_hdn5 = null  

	if @wv_replenish_hdn6 = '~#~' 
		select @wv_replenish_hdn6 = null  

	if @wv_replenish_hdn7 = '~#~' 
		select @wv_replenish_hdn7 = null  

	if @wv_replenish_hdn8 = '~#~' 
		select @wv_replenish_hdn8 = null  

	if @wv_replenish_hdn9 = '~#~' 
		select @wv_replenish_hdn9 = null  

	if @zone_rule = -915
		select @zone_rule = null  

	if @auto_short_close_order = -915
		select @auto_short_close_order = null--code added for LRT-3129

	if @demand_replenish = -915
		select @demand_replenish = null--code added for LRT-3129
	
	IF @enble_dmnd_based_rep = -915
		SELECT @enble_dmnd_based_rep = null--code added for EPE-18934


	select	@sysdate	=	dbo.res_getdate(@ctxt_ouinstance)

	select	@exists_flag			=	'Y'
	from	wms_wave_replenish_rul_hdr (nolock)
	where	wms_wav_repl_ouid		=	@ctxt_ouinstance

	select @exists_flag = isnull(@exists_flag,'N')
	
	if	((@order_date_combo  is not null and @order_date_combo2 is null	or @order_date_edit is null) or
		(@order_date_combo2 is not null and @order_date_combo is null	or @order_date_edit is null) or
		(@order_date_edit	is not null and @order_date_combo is null	or @order_date_combo2 is null))
		and @order_time_base = 1 --LRT-1094
	begin
		--Provide all details for Order Date criteria.
		exec fin_german_raiserror_sp 'WMACTIVITY' ,@ctxt_language ,901
		return
	end	   

	select	@alloc_rule_tmp			=	wms_paramcode
	from	wms_component_met(nolock)
	where	wms_componentname		=	'WMACTIVITY'
	and		wms_paramcategory		=	'COMBO'
	and		wms_paramtype			=	'ALOCRUL'
	and		wms_paramdesc			=	@alloc_rule
	and		wms_langid				=   @ctxt_language

	select	@replenish_plan_tmp		=	wms_paramcode
	from	wms_component_met(nolock)
	where	wms_componentname		=	'WMACTIVITY'
	and		wms_paramcategory		=	'COMBO'
	and		wms_paramtype			=	'REPPLN'
	and		wms_paramdesc			=	@replenish_plan
	and		wms_langid				=   @ctxt_language

	select	@order_date_combo_tmp	=	wms_paramcode
	from	wms_component_met(nolock)
	where	wms_componentname		=	'WMACTIVITY'
	and		wms_paramcategory		=	'COMBO'
	and		wms_paramtype			=	'ORDDTOP'
	and		wms_paramdesc			=	@order_date_combo
	and		wms_langid				=   @ctxt_language

	select	@order_date_combo2_tmp	=	wms_paramcode
	from	wms_component_met(nolock)
	where	wms_componentname		=	'WMACTIVITY'
	and		wms_paramcategory		=	'COMBO'
	and		wms_paramtype			=	'ORDDTDY'
	and		wms_paramdesc			=	@order_date_combo2
	and		wms_langid				=   @ctxt_language

	if @exists_flag = 'Y'
	begin
		update	wms_wave_replenish_rul_hdr
		set		wms_wav_repl_zone				=	@zone_rule,	
				wms_wav_repl_criticalday		=	@critical_check,
				wms_wav_repl_lineperplan		=	@lines_per_plan,
				wms_wav_repl_allocrule			=	@alloc_rule_tmp,
				wms_wav_repl_planby				=	@replenish_plan_tmp,
				wms_wav_repl_unlock_odo			=	@unlock_odo,
				wms_wav_repl_time_based			=	@order_time_base,
				wms_wav_repl_open_order			=	@open_orders,
				wms_wav_repl_orddate_operator	=	@order_date_combo_tmp,
				wms_wav_repl_orddate_inno		=	@order_date_edit,
				wms_wav_repl_orddate_days		=	@order_date_combo2_tmp,
				wms_wav_repl_orddate_rangefrom	=	@order_date_range_1,
				wms_wav_repl_orddate_rangeto	=	@order_date_range_2,
				wms_wav_repl_timestamp			=	wms_wav_repl_timestamp + 1,
				wms_wav_repl_modified_date		=	@sysdate,
				wms_wav_repl_modified_by		=	@ctxt_user,
				wms_wav_repl_en_dmnd_rep		=	@enble_dmnd_based_rep --code added for EPE-18934 
		where	wms_wav_repl_ouid				=	@ctxt_ouinstance
	end
	else
	begin
		insert into wms_wave_replenish_rul_hdr
		(
			wms_wav_repl_ouid,					wms_wav_repl_zone,					wms_wav_repl_criticalday,			wms_wav_repl_lineperplan,
			wms_wav_repl_allocrule,				wms_wav_repl_planby,				wms_wav_repl_unlock_odo,			wms_wav_repl_time_based,
			wms_wav_repl_open_order,			wms_wav_repl_orddate_operator,		wms_wav_repl_orddate_inno,			wms_wav_repl_orddate_days,
			wms_wav_repl_orddate_rangefrom,		wms_wav_repl_orddate_rangeto,		wms_wav_repl_timestamp,				wms_wav_repl_created_date,
			wms_wav_repl_created_by,			
			wms_wav_repl_en_dmnd_rep  --code added for EPE-18934
		)
		select
			@ctxt_ouinstance,					@zone_rule,							@critical_check,					@lines_per_plan,
			@alloc_rule_tmp,					@replenish_plan_tmp,				@unlock_odo,						@order_time_base,
			@open_orders,						@order_date_combo_tmp,				@order_date_edit,					@order_date_combo2_tmp,
			@order_date_range_1,				@order_date_range_2,				1,									@sysdate,
			@ctxt_user,							
			@enble_dmnd_based_rep --code added for EPE-18934
	end

	exec	wma_reprul_sp_cmn_hrf
			@ctxt_ouinstance,
			@ctxt_user,
			@ctxt_language,
			@ctxt_service,
			@alloc_rule,
			@critical_check,
			@hdnguid,
			@hdnhiddencontrol1,
			@hdnhiddencontrol2,
			@hdntimestamp,
			@lines_per_plan,
			@open_orders,
			@order_date_combo,
			@order_date_combo2,
			@order_date_edit,
			@order_date_range_1,
			@order_date_range_2,
			@order_time_base,
			@replenish_plan,
			@unlock_odo,
			@wv_replenish_hdn1,
			@wv_replenish_hdn10,
			@wv_replenish_hdn2,
			@wv_replenish_hdn3,
			@wv_replenish_hdn4,
			@wv_replenish_hdn5,
			@wv_replenish_hdn6,
			@wv_replenish_hdn7,
			@wv_replenish_hdn8,
			@wv_replenish_hdn9,
			@zone_rule,
			'SAV',
			@exists_flag,
			@m_errorid output

	--Replenishment Rules saved successfully.
	select @m_errorid = 900034010


	/* 
	--outputlist
		select
		null 'alloc_rule', 
		null 'critical_check', 
		null 'hdnguid', 
		null 'hdnhiddencontrol1', 
		null 'hdnhiddencontrol2', 
		null 'hdntimestamp', 
		null 'lines_per_plan', 
		null 'open_orders', 
		null 'order_date_combo', 
		null 'order_date_combo2', 
		null 'order_date_edit', 
		null 'order_date_range_1', 
		null 'order_date_range_2', 
		null 'order_time_base', 
		null 'replenish_plan', 
		null 'unlock_odo', 
		null 'wv_replenish_hdn1', 
		null 'wv_replenish_hdn10', 
		null 'wv_replenish_hdn2', 
		null 'wv_replenish_hdn3', 
		null 'wv_replenish_hdn4', 
		null 'wv_replenish_hdn5', 
		null 'wv_replenish_hdn6', 
		null 'wv_replenish_hdn7', 
		null 'wv_replenish_hdn8', 
		null 'wv_replenish_hdn9', 
		null 'zone_rule', 
	*/
	
set nocount off

end