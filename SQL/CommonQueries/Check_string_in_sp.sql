SELECT DISTINCT
       o.name AS Object_Name,
       o.type_desc
FROM sys.sql_modules m
       INNER JOIN
       sys.objects o
         ON m.object_id = o.object_id
		 and m.object_id =  OBJECT_ID('wms_bin_sp_multi_su_cmn_ed_asg_dtl')
 WHERE m.definition Like '%wms_out%';
 


--dbo.wms_bintobin_cmn_validation_sp
--dbo.wma_bin_cap_wt_cmn_sp
--dbo.wma_itord_sp_cmn_hsav
--dbo.wms_stock_uid_tracking_dtl_cmn_sp
--dbo.wma_inspm_sp_create_hchk
--dbo.wms_bin_item_alloc_sp





--wms_binpl_multi_su_cmn_hchk
--wms_Bintobin_cmn_validation_sp
--wma_inspm_sp_create_hchk
--wms_item_multiple_repln_cmn_sp
--wms_itm_repl_sp_cmn_dtl
--wms_bin_item_alloc_sp