--Cons_Rptlst_addtl_re_chge_elmnts_SP

/********************************************************************************/
/* procedure      Cons_Rptlst_addtl_re_chge_elmnts_SP                           */
/* description                                                                  */
/********************************************************************************/
/* project                                                                      */
/* version                                                                      */
/********************************************************************************/
/* referenced                                                                   */
/* tables                                                                       */
/********************************************************************************/
/* development history                                                          */
/********************************************************************************/
/* author          sindhu                                                       */
/* date           12/20/2019                                                   */
/********************************************************************************/
/* modification history                                                         */
/********************************************************************************/
/* modified by                                                                  */
/* date                                                                         */
/* description                                                                  */
/********************************************************************************/
--CREATE
ALTER PROC Cons_Rptlst_addtl_re_chge_elmnts_SP	
	@ctxt_language                	ctxt_language,
	@ctxt_ouinstance              	ctxt_ouinstance,
	@ctxt_role                    	ctxt_role,
	@ctxt_user                    	ctxt_user,
	@hguid_able                   	udd_guid,
	@contract_no_grid       		udd_documentno,
	@customer_no_grid              	udd_vendorcode,
	@date_from_grid              	udd_date,
	@date_to_grid                 	udd_date,
	@gen_date_frm_grid              udd_date,
	@gen_date_to_grid               udd_date,
	@generated_by_grid             	udd_txt255,
	@report_name_grid             	udd_txt255,
	@report_shrt_name_grid          udd_documentno,
	@s_no_grid_grer					udd_seqno
	

AS
BEGIN

	DECLARE @guid_able	udd_guid

	SET @guid_able = NEWID()

	SELECT @ctxt_language           = LTRIM(RTRIM(@ctxt_language))
	SELECT @ctxt_ouinstance         = LTRIM(RTRIM(@ctxt_ouinstance))
	SELECT @ctxt_role               = LTRIM(RTRIM(@ctxt_role))
	SELECT @ctxt_user           	= LTRIM(RTRIM(@ctxt_user))
	SELECT @hguid_able            	= LTRIM(RTRIM(@hguid_able))
	SELECT @contract_no_grid        = LTRIM(RTRIM(@contract_no_grid))
	SELECT @customer_no_grid        = LTRIM(RTRIM(@customer_no_grid))
	SELECT @date_from_grid			= LTRIM(RTRIM(@date_from_grid))
	SELECT @date_to_grid            = LTRIM(RTRIM(@date_to_grid))
	SELECT @gen_date_frm_grid       = LTRIM(RTRIM(@gen_date_frm_grid))
	SELECT @gen_date_to_grid        = LTRIM(RTRIM(@gen_date_to_grid))
	SELECT @generated_by_grid       = LTRIM(RTRIM(@generated_by_grid))
	SELECT @report_name_grid        = LTRIM(RTRIM(@report_name_grid))
	SELECT @report_shrt_name_grid   = LTRIM(RTRIM(@report_shrt_name_grid))
	SELECT @s_no_grid_grer          = LTRIM(RTRIM(@s_no_grid_grer))

	--null checking
	IF @ctxt_language = -915					SELECT @ctxt_language			= NULL
	IF @ctxt_ouinstance = -915					SELECT @ctxt_ouinstance			= NULL
	IF @ctxt_role  in ('', '~#~')				SELECT @ctxt_role				= NULL
	IF @ctxt_user  in ('', '~#~')				SELECT @ctxt_user				= NULL
	IF @hguid_able in ('', '~#~')				SELECT @hguid_able				= NULL
	IF @contract_no_grid in ('','~#~')			SELECT @contract_no_grid		= NULL
	IF @customer_no_grid in ('','~#~')			SELECT @customer_no_grid		= NULL
	IF @date_from_grid= '1900-01-01'			SELECT @date_from_grid			= NULL
	IF @date_to_grid= '1900-01-01'				SELECT @date_to_grid			= NULL
	IF @generated_by_grid in ('','~#~')			SELECT @generated_by_grid		= NULL
	IF @gen_date_frm_grid= '1900-01-01'			SELECT @gen_date_frm_grid		= NULL
	IF @gen_date_to_grid= '1900-01-01'			SELECT @gen_date_to_grid		= NULL
	IF @report_name_grid IN ('', '~#~')			SELECT @report_name_grid		= NULL
	IF @report_shrt_name_grid IN ('', '~#~')	SELECT @report_shrt_name_grid	= NULL
	IF @s_no_grid_grer=0						SELECT @s_no_grid_grer			= NULL



	IF @report_name_grid  = 'Loan Orders Charge back to Customers'
	BEGIN
	
		EXEC lo_loan_ord_chrgs_to_cust_POP_SP @ctxt_language,			@ctxt_ouinstance,			@ctxt_role,					@ctxt_user,   null,
											  @contract_no_grid,		@customer_no_grid,			@date_from_grid,			@date_to_grid,
											  @gen_date_frm_grid,		@gen_date_to_grid,			@generated_by_grid,			@hguid_able,
											  @report_name_grid,		@s_no_grid_grer
											
	END

	IF @report_name_grid  = 'Rental Orders Charge back to Customers'
	BEGIN


		EXEC rnt_rental_ord_chrgs_rpt_POP_SP  @ctxt_language,			@ctxt_ouinstance,			@ctxt_role,					@ctxt_user,
											  @contract_no_grid,		@customer_no_grid,			@date_from_grid,			@date_to_grid,
											  @gen_date_frm_grid,		@gen_date_to_grid,			@generated_by_grid,			@hguid_able,
											  @report_name_grid,		@s_no_grid_grer

											
	END



		IF @report_name_grid  = 'Unused Return Orders and cost elements'
		EXEC unused_rtn_ord_rpt_POP_SP		@ctxt_language,				@ctxt_ouinstance,			@ctxt_role,					@ctxt_user,
		@contract_no_grid,					@customer_no_grid,			@date_from_grid,			@date_to_grid,
		@gen_date_frm_grid,					@gen_date_to_grid,			@generated_by_grid,			@hguid_able,
		@report_name_grid,					@s_no_grid_grer
	

	IF @report_name_grid  = 'Shipping Cost'
		BEGIN
		
		EXEC shipping_cost_pop_sp			@ctxt_language,				@ctxt_ouinstance,			@ctxt_role,					@ctxt_user,
		@contract_no_grid,					@customer_no_grid,			@date_from_grid,			@date_to_grid,
		@gen_date_frm_grid,					@gen_date_to_grid,			@generated_by_grid,			@hguid_able,
		@report_name_grid,					@s_no_grid_grer

		END

	SELECT 

		@guid_able			'Guid'
	

END