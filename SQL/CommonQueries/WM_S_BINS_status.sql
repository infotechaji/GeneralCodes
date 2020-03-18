wm_bin_sp_initstatus

/******************************************************************************/
/* procedure					: wm_bin_sp_initstatus						  */
/* description					: 											  */
/******************************************************************************/
/* project						: 								 			  */
/* ecrno						: 								 			  */
/* version						: 								 			  */
/******************************************************************************/
/* referenced					: 											  */
/* tables						: 											  */
/******************************************************************************/
/* development history			: 											  */
/******************************************************************************/
/* author						: Parameswari G								  */
/* date							: sep 21 2016  2:39pm						  */
/******************************************************************************/
/* modification history			: 											  */
/******************************************************************************/
/* modified by					: 								 			  */
/* date							: 								 			  */
/* description					: 								 			  */
/******************************************************************************/

CREATE PROCEDURE wm_bin_sp_initstatus
	@ctxt_ouinstance 	ctxt_ouinstance, 
	@ctxt_user       	ctxt_user, 
	@ctxt_language   	ctxt_language, 
	@ctxt_service    	ctxt_service, 
	@m_errorid       	udd_int output --to return execution status
AS
BEGIN
	-- nocount should be switched on to prevent phantom rows
	SET NOCOUNT ON
	-- @m_errorid should be 0 to indicate success
	SELECT @m_errorid		 = 0
	
	--temporary and formal parameters mapping

	SELECT @ctxt_user				=	LTRIM(RTRIM(@ctxt_user))
	SELECT @ctxt_service			=	LTRIM(RTRIM(@ctxt_service))

	--null checking

	IF @ctxt_ouinstance				=	-915		SELECT @ctxt_ouinstance		=	null  
	IF @ctxt_user					=	'~#~'		SELECT @ctxt_user			=	null  
	IF @ctxt_language				=	-915		SELECT @ctxt_language		=	null  
	IF @ctxt_service				=	'~#~'		SELECT @ctxt_service		=	null  

	SELECT		wms_paramdesc			'STATUS'
	FROM		wms_component_met		(nolock)
	WHERE		wms_componentname	=	'WMSETUP' 
	AND			wms_paramcategory	=	'COMBO' 
	AND			wms_paramtype		=	'BIN_STS'
	AND			wms_langid			=	1--@ctxt_language
	ORDER BY	wms_sequenceno			asc 
	
	SET NOCOUNT OFF

END

