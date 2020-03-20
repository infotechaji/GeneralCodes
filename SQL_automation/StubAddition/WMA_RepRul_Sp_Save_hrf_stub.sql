/******************************************************************************/
/* Procedure					: WMA_RepRul_Sp_Save_hrf								 */
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
/* Author						: ModelExplorer								 */
/* Date							: Mar  9 2020  5:41PM								 */
/******************************************************************************/
/* Modification History			: 								 */
/******************************************************************************/
/* Modified By					: 								 */
/* Date							: 								 */
/* Description					: 								 */
/******************************************************************************/

Create Procedure WMA_RepRul_Sp_Save_hrf
	@ctxt_ouinstance        	ctxt_ouinstance, --Input 
	@ctxt_user              	ctxt_user, --Input 
	@ctxt_language          	ctxt_language, --Input 
	@ctxt_service           	ctxt_service, --Input 
	@alloc_rule             	desc255, --Input/Output
	@auto_short_close_order 	hrint, --Input/Output
	@critical_check         	hrint, --Input/Output
	@demand_replenish       	hrint, --Input/Output
	@enble_dmnd_based_rep   	hrint, --Input/Output -- 
	@hdnguid                	desc255, --Input/Output
	@hdnhiddencontrol1      	desc255, --Input/Output
	@hdnhiddencontrol2      	desc255, --Input/Output
	@hdntimestamp           	timestamp, --Input/Output
	@lines_per_plan         	lineno, --Input/Output
	@open_orders            	desc255, --Input/Output
	@order_date_combo       	desc255, --Input/Output
	@order_date_combo2      	desc255, --Input/Output
	@order_date_edit        	hrint, --Input/Output
	@order_date_range_1     	date, --Input/Output
	@order_date_range_2     	date, --Input/Output
	@order_time_base        	hrint, --Input/Output
	@replenish_plan         	desc255, --Input/Output
	@unlock_odo             	hrint, --Input/Output
	@wv_replenish_hdn1      	desc255, --Input/Output
	@wv_replenish_hdn10     	desc255, --Input/Output
	@wv_replenish_hdn2      	desc255, --Input/Output
	@wv_replenish_hdn3      	desc255, --Input/Output
	@wv_replenish_hdn4      	desc255, --Input/Output
	@wv_replenish_hdn5      	desc255, --Input/Output
	@wv_replenish_hdn6      	desc255, --Input/Output
	@wv_replenish_hdn7      	desc255, --Input/Output
	@wv_replenish_hdn8      	desc255, --Input/Output
	@wv_replenish_hdn9      	desc255, --Input/Output
	@zone_rule              	hrint, --Input/Output
	@ajith              		hrint, --Input/Output
	@vijay              		hrint, --Input/Output
	@m_errorid              	int output --To Return Execution Status
as
Begin
	-- nocount should be switched on to prevent phantom rows
	Set nocount on
	-- @m_errorid should be 0 to Indicate Success
	Set @m_errorid = 0

	--declaration of temporary variables


	--temporary and formal parameters mapping

	Set @ctxt_user               = ltrim(rtrim(@ctxt_user))
	Set @ctxt_service            = ltrim(rtrim(@ctxt_service))
	Set @alloc_rule              = ltrim(rtrim(@alloc_rule))
	Set @hdnguid                 = ltrim(rtrim(@hdnguid))
	Set @hdnhiddencontrol1       = ltrim(rtrim(@hdnhiddencontrol1))
	Set @hdnhiddencontrol2       = ltrim(rtrim(@hdnhiddencontrol2))
	Set @open_orders             = ltrim(rtrim(@open_orders))
	Set @order_date_combo        = ltrim(rtrim(@order_date_combo))
	Set @order_date_combo2       = ltrim(rtrim(@order_date_combo2))
	Set @replenish_plan          = ltrim(rtrim(@replenish_plan))
	Set @wv_replenish_hdn1       = ltrim(rtrim(@wv_replenish_hdn1))
	Set @wv_replenish_hdn10      = ltrim(rtrim(@wv_replenish_hdn10))
	Set @wv_replenish_hdn2       = ltrim(rtrim(@wv_replenish_hdn2))
	Set @wv_replenish_hdn3       = ltrim(rtrim(@wv_replenish_hdn3))
	Set @wv_replenish_hdn4       = ltrim(rtrim(@wv_replenish_hdn4))
	Set @wv_replenish_hdn5       = ltrim(rtrim(@wv_replenish_hdn5))
	Set @wv_replenish_hdn6       = ltrim(rtrim(@wv_replenish_hdn6))
	Set @wv_replenish_hdn7       = ltrim(rtrim(@wv_replenish_hdn7))
	Set @wv_replenish_hdn8       = ltrim(rtrim(@wv_replenish_hdn8))
	Set @wv_replenish_hdn9       = ltrim(rtrim(@wv_replenish_hdn9))

	--null checking

	IF @ctxt_ouinstance = -915
		Select @ctxt_ouinstance = null  

	IF @ctxt_user = '~#~' 
		Select @ctxt_user = null  

	IF @ctxt_language = -915
		Select @ctxt_language = null  

	IF @ctxt_service = '~#~' 
		Select @ctxt_service = null  

	IF @alloc_rule = '~#~' 
		Select @alloc_rule = null  

	IF @auto_short_close_order = -915
		Select @auto_short_close_order = null  

	IF @critical_check = -915
		Select @critical_check = null  

	IF @demand_replenish = -915
		Select @demand_replenish = null  

	IF @enble_dmnd_based_rep = -915
		Select @enble_dmnd_based_rep = null

	IF @hdnguid = '~#~' 
		Select @hdnguid = null  

	IF @hdnhiddencontrol1 = '~#~' 
		Select @hdnhiddencontrol1 = null  

	IF @hdnhiddencontrol2 = '~#~' 
		Select @hdnhiddencontrol2 = null  

	IF @hdntimestamp = -915
		Select @hdntimestamp = null  

	IF @lines_per_plan = -915
		Select @lines_per_plan = null  

	IF @open_orders = '~#~' 
		Select @open_orders = null  

	IF @order_date_combo = '~#~' 
		Select @order_date_combo = null  

	IF @order_date_combo2 = '~#~' 
		Select @order_date_combo2 = null  

	IF @order_date_edit = -915
		Select @order_date_edit = null  

	IF @order_date_range_1 = '01/01/1900' 
		Select @order_date_range_1 = null  

	IF @order_date_range_2 = '01/01/1900' 
		Select @order_date_range_2 = null  

	IF @order_time_base = -915
		Select @order_time_base = null  

	IF @replenish_plan = '~#~' 
		Select @replenish_plan = null  

	IF @unlock_odo = -915
		Select @unlock_odo = null  

	IF @wv_replenish_hdn1 = '~#~' 
		Select @wv_replenish_hdn1 = null  

	IF @wv_replenish_hdn10 = '~#~' 
		Select @wv_replenish_hdn10 = null  

	IF @wv_replenish_hdn2 = '~#~' 
		Select @wv_replenish_hdn2 = null  

	IF @wv_replenish_hdn3 = '~#~' 
		Select @wv_replenish_hdn3 = null  

	IF @wv_replenish_hdn4 = '~#~' 
		Select @wv_replenish_hdn4 = null  

	IF @wv_replenish_hdn5 = '~#~' 
		Select @wv_replenish_hdn5 = null  

	IF @wv_replenish_hdn6 = '~#~' 
		Select @wv_replenish_hdn6 = null  

	IF @wv_replenish_hdn7 = '~#~' 
		Select @wv_replenish_hdn7 = null  

	IF @wv_replenish_hdn8 = '~#~' 
		Select @wv_replenish_hdn8 = null  

	IF @wv_replenish_hdn9 = '~#~' 
		Select @wv_replenish_hdn9 = null  

	IF @zone_rule = -915
		Select @zone_rule = null  

	/* 
	--OutputList
		Select
		null 'alloc_rule', 
		null 'auto_short_close_order', 
		null 'critical_check', 
		null 'demand_replenish', 
		null 'enble_dmnd_based_rep', 
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
	
Set nocount off

End


