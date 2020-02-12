EXEC part_sale_order_inv_pop_sp
		@ctxt_language					=1,			
		@ctxt_ouinstance				=2,	
		@ctxt_role						='Ramcorole',	
		@ctxt_user						='dmuser',
		@contract_no_grid				=null,
		@customer_no_grid				=null,
		@date_from_grid					=null, 
		@date_to_grid					=null, 
		@gen_date_frm_grid				=null,
		@gen_date_to_grid				=null,
		@generated_by_grid				=null,
		@hguid_able						='3333',
		@report_name_grid				=null,
		@s_no_grid_grer					=null


-- exec part_sale_order_inv_copy_sp '12346'






--delete FROM pso_inv_hdr_dtl_tmp	WHERE guid = '12345'
--delete FROM pso_inv_tcd_dtl_tmp	WHERE guid = '12345'
--delete FROM pso_inv_part_dtl_tmp	WHERE guid = '12345'
--delete FROM pso_invoice_tmp		WHERE guid = '12345'