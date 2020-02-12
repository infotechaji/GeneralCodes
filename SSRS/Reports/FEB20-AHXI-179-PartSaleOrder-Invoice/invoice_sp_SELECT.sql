/*
****************************************************************************
Author                      : Ajithkumar M 							          
Date                        : 06 FEB 2020								  
ID                          : AHXI-179                                                      							 
*************************Modification History*******************************

V - 1.0 - Initial version  - 06/02/2020
																			  
****************************************************************************
*/


ALTER	
--CREATE 
PROCEDURE	part_sale_order_inv_copy_sp
		
		@hguid_able						udd_guid
		
AS 
BEGIN
	SELECT
			hd_ou_name					'hd_ou_name',
			hd_address_1				'hd_address_1',
			hd_address_others			'hd_address_others',
			hd_attention				'hd_attention',
			hd_receivable_mail			'hd_receivable_mail',
			hd_website					'hd_website',
			hd_invoice_no				'hd_invoice_no',
			hd_invoice_no_date			'hd_invoice_no_date',
			cus_no						'cus_no',
			cus_name					'cus_name',
			cus_po_no_ref				'cus_po_no_ref',
			cus_part_sale_order_no		'cus_part_sale_order_no',
			cus_currency				'cus_currency',
			cus_address_1_2				'cus_address_1_2',
			cus_address_3				'cus_address_3',
			cus_state_city_zip			'cus_state_city_zip',
			cus_country					'cus_country',
			part_auto_num				'part_auto_num',
			part_no						'part_no',
			part_description			'part_description',
			part_unit_price				'part_unit_price',
			part_net_value				'part_net_value',
			part_sub_total				'part_sub_total',
			tcd_auto_num				'tcd_auto_num',
			tcd_no						'tcd_no',
			tcd_description				'tcd_description',
			tcd_type					'tcd_type',
			tcd_variant_no				'tcd_variant_no',
			tcd_rate					'tcd_rate',
			tcd_amount					'tcd_amount',
			tcd_subtotal				'tcd_subtotal',
			inv_comments				'inv_comments',
			ac_company_name				'ac_company_name',
			ac_bank_name				'ac_bank_name',
			ac_inst_address				'ac_inst_address',
			ac_account_no				'ac_account_no',
			ac_currency					'ac_currency',
			ac_swift_code				'ac_swift_code',
			apprd_user_name				'apprd_user_name',
			apprd_total_amount			'apprd_total_amount',
			apprd_currency				'apprd_currency',
			apprd_signature				'apprd_signature',
			ft_due_days					'ft_due_days',
			ft_penalty					'ft_penalty',
			ft_cur_date_time			'ft_cur_date_time',
			ft_dtm_format_from_ou		'ft_dtm_format_from_ou'
	FROM	pso_invoice_tmp
	WHERE	guid							=	@hguid_able
	
	
	DELETE 
	FROM	pso_invoice_tmp
	WHERE	guid							=	@hguid_able

END




--exec part_sale_order_inv_copy_sp '12346'

--select * from pso_invoice_tmp

--truncate table pso_invoice_tmp