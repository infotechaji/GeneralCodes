
/* 

Procedure                   : part_sale_order_invoce
Version                     : 1.0										  
Description                 : 
Pending cases               :
Open issues					:
																	  
****************************************************************************
Author                      : Ajithkumar M 							          
Date                        : 06 FEB 2020								  
ID                          : AHXI-179                                                      							 
*************************Modification History*******************************

V - 1.0 - Initial version  - 06/02/2020
																			  
****************************************************************************
*/


--sp_rename 'part_sale_order_inv_sp','part_sale_order_inv_pop_sp'
--CREATE
ALTER	PROCEDURE	part_sale_order_inv_pop_sp
		@ctxt_language					ctxt_language,			
		@ctxt_ouinstance				ctxt_ouinstance,	
		@ctxt_role						ctxt_role,	
		@ctxt_user						ctxt_user,
		@contract_no_grid				udd_documentno,
		@customer_no_grid				udd_documentno,
		@date_from_grid					fin_date, 
		@date_to_grid					fin_date, 
		@gen_date_frm_grid				fin_date,
		@gen_date_to_grid				fin_date,
		@generated_by_grid				udd_txt255,
		@hguid_able						udd_guid,
		@report_name_grid				udd_txt255,
		@s_no_grid_grer					UDD_SEQNO			

AS 
BEGIN
	SET NOCOUNT ON
	DECLARE @current_date fin_date
	
	SELECT @current_date	=	dbo.RAS_Getdate(@ctxt_ouinstance)
	--SELECT @hguid_able		=	newid()

	
	INSERT 	INTO	pso_invoice_tmp 
	(
			hd_invoice_no,					hd_invoice_status_code,		hd_invoice_tran_type,
			hd_invoice_last_mdfd_date,		cus_bill_to_customer,		company_id,
			cus_currency,					inv_comments,				bill_to_id,
			custno,							pay_term,					apprd_total_amount,
			cus_part_sale_order_no,			pso_ref_doc_type,			pso_shipping_note_no,
			apprd_user_name, 
			guid,							ouid
	) 
	SELECT	DISTINCT
			hdr.tran_no,					hdr.tran_status,					hdr.tran_type,
			hdr.modifieddate,				hdr.bill_to_cust,					hdr.fb_id,
			hdr.tran_currency,				hdr.comments,						hdr.bill_to_id,
			hdr.custno,						hdr.pay_term,						hdr.item_amount,
			dtl.packslip_no,				CASE WHEN refdoctype ='PSO' THEN 'Part Sale Order' ELSE refdoctype END,
			dtl.shpno,						hdr.modifiedby,
			@hguid_able,					@ctxt_ouinstance
	FROM 	cdi_invoice_hdr							hdr WITH(NOLOCK)
	JOIN	cdi_item_dtl							dtl WITH(NOLOCK)
	ON		dtl.tran_no							=	hdr.tran_no
	AND		dtl.tran_ou							=	hdr.tran_ou
	AND		dtl.refdoctype						=	'PSO'
	--AND		hdr.tran_status							in  ('AUT')
	AND		hdr.tran_type							in	('RM_CPIN','RM_RCPIN')
	AND		dtl.packslip_no							is not null 	
	AND		tran_date								BETWEEN isnull(@date_from_grid,tran_date)	AND isnull(@date_to_grid,tran_date)
	  	
	
	--po number 
	
	UPDATE	tmp
	SET		tmp.cus_po_no_ref					=	pso.pso_custpo
	FROM	pso_invoice_tmp							tmp 
	JOIN	pso_info_hdr							pso WITH(NOLOCK)
	ON		pso.pso_NO							=	tmp.cus_part_sale_order_no
	WHERE	guid								=	@hguid_able
	AND		ouid								=	@ctxt_ouinstance

	UPDATE	tmp
	SET		cus_name							=	custname
	FROM	pso_invoice_tmp							tmp
	JOIN	cdi_cu_ccy_acctgrp_vw					cus
	ON		custcode							=	tmp.cus_bill_to_customer
	AND		ou									=	tmp.ouid 
	WHERE	guid								=	@hguid_able
	AND		ouid								=	@ctxt_ouinstance
	
	-- bill to customer address 
	UPDATE	tmp
	SET		cus_address_1						=	CMH_Address1,
			cus_address_2						=	CMH_Address2,
			cus_address_3						=	CMH_Address3,
			cus_city							=	CMH_City,
			cus_state							=	CMH_State,
			cus_country							=	CMH_Country,
			cus_zip								=	CMH_ZipCode
	FROM	pso_invoice_tmp							tmp
	JOIN	Cu_CMH_Cust_Master_Hdr					cus
	ON		cus.CMH_Cust_Code					=	tmp.custno
	AND		cus.CMH_Created_Ouinstance			=	ouid
	WHERE	guid								=	@hguid_able
	AND		ouid								=	@ctxt_ouinstance

	
	-- OU details for header 
	INSERT INTO pso_inv_hdr_dtl_tmp 
	(
			company_code,						hd_ou_name,				hd_address_1,
			hd_address_2,						hd_address_3,			hd_city, 
			hd_state,							hd_country,				hd_attention,
			hd_receivable_mail,					hd_website,				
			guid,					ouid
	)
		
	SELECT DISTINCT 
			company_code,							company_name,										dbo.CapitalizeFirstLetter(address1),
			dbo.CapitalizeFirstLetter(address2),	dbo.CapitalizeFirstLetter(address3),				dbo.CapitalizeFirstLetter(city),
			dbo.CapitalizeFirstLetter([state]),		dbo.CapitalizeFirstLetter(country),					'Finance Department',	
			'account.receivable@haeco.com',		company_url,
			@hguid_able,			@ctxt_ouinstance 
	FROM	emod_company_mst			emo WITH(NOLOCK)
	JOIN	pso_invoice_tmp				tmp
	ON		tmp.company_id			=	emo.company_code
	

	INSERT INTO pso_inv_part_dtl_tmp 
	(
			part_sale_order_no,		part_line_num,		part_no,			part_description,
			part_qty,				uom,				part_serial_no,		part_lot_no,	
			part_unit_price,		part_net_value,		part_mrno,
			guid,					ouid
	) 
	SELECT	DISTINCT
			dtl.pso_no,				pso_lineno,			pso_partno,			pso_partdesc,
			pso_ordqty,				pso_prtuom,			null,				null,
			pso_act_uprice,			pso_exnetvalue,		pso_mrno,
			@hguid_able,			@ctxt_ouinstance
	FROM	pso_invoice_tmp							tmp
	JOIN	pso_prtinfo_dtl							dtl WITH(NOLOCK) 
	ON		pso_no								=	tmp.cus_part_sale_order_no
	AND		pso_ou								=	tmp.ouid 
	AND		tmp.guid							=	@hguid_able
	AND		tmp.ouid							=	@ctxt_ouinstance
	
	
	INSERT INTO pso_inv_tcd_dtl_tmp
	(
			part_sale_order_no,		tcd_no,				tcd_variant_no,
			tcd_rate,				tcd_amount,			tcd_type,
			tcd_auto_num,			guid,				ouid
	)
	
	SELECT DISTINCT 
			tcd.pso_no,				pso_tcdcode,		pso_tcdvar,
			pso_rate,				pso_tcd_amt,		r.parameter_text,
			pso_tcdlineno,			@hguid_able,		@ctxt_ouinstance
	FROM	pso_tcd_dtl								tcd WITH(NOLOCK)
	JOIN	pso_invoice_tmp							tmp
	ON		tcd.pso_no							=	tmp.cus_part_sale_order_no
	JOIN	fin_quick_code_met						r	WITH(NOLOCK)
	ON		r.parameter_code					=	 case when tcd.pso_tcd_type='C' then 'IC' 
														 when tcd.pso_tcd_type='T' then 'IT' 
														 when tcd.pso_tcd_type='D' then 'ID' else tcd.pso_tcd_type end
	WHERE	r.component_id						=   'CDI'
	AND		r.parameter_category				=	'ITEMTYPE'	
	AND		r.parameter_type					=	'COMBO'


	UPDATE	tmp
	SET		tcd_description						=	tcdcodevariantdesc
	FROM	pso_inv_tcd_dtl_tmp						tmp
	join	cdi_tcd_tmp_vw							b WITH (NOLOCK)
	on		b.tcdcode							=	tmp.tcd_no
	AND		b.tcdvariant  						=   tmp.tcd_variant_no
	WHERE	guid								=	@hguid_able
	AND		ouid								=	@ctxt_ouinstance
	
	
	-- bank details 
	UPDATE tmp
	SET		
			ac_bank_name						=	em.bank_name,
			ac_inst_address						=	dbo.CapitalizeFirstLetter(em.address1)+','+dbo.CapitalizeFirstLetter(address2)+','+dbo.CapitalizeFirstLetter(address3)+','+dbo.CapitalizeFirstLetter(city)+','+dbo.CapitalizeFirstLetter(state)+','+dbo.CapitalizeFirstLetter(country),--+','+zip_code,
			ac_swift_code						=	em.swift_no,
			ac_account_no						=	ac.bank_acc_no,
			ac_currency							=	ac.currency_code,
			ac_bank_ref_no						=	ac.bank_ref_no,
			ac_company_code						=	ac.company_code
	FROM	emod_bank_ref_mst						em WITH(NOLOCK)
	JOIN	bnkdef_acc_mst							ac WITH(NOLOCK)
	ON 		ac.bank_ref_no						=	em.bank_ref_no
	JOIN	pso_invoice_tmp							tmp 
	ON		ac.company_code						=	tmp.company_id


	--Signature 
	UPDATE	tmp
	SET		apprd_signature						=	CI_SubSegment
	FROM	pso_invoice_tmp							tmp 
	JOIN	Cu_CI_Commercial_Info					ci WITH(NOLOCK)
	ON		CI_Cust_Code						=	tmp.custno
	AND		CI_Created_OUInstance				=	tmp.ouid
	WHERE	guid								=	@hguid_able
	AND		ouid								=	@ctxt_ouinstance
	
	
	--Pay term details 
	UPDATE	tmp
	SET		part_serial_no						=	dtl.Smn_Serial_no,
			part_lot_no							=	dtl.Smn_Lot_no
	FROM	pso_inv_part_dtl_tmp					tmp 
	JOIN	SMN_SMN_SRL_LOT_PART_HISTORY			dtl WITH(NOLOCK)
	ON		dtl.Smn_Part_no						=	tmp.part_no
	AND		dtl.Smn_RefDoc_No					=	tmp.part_mrno
	AND		dtl.Smn_Transaction_OU				=	tmp.ouid
	WHERE	tmp.guid							=	@hguid_able
	AND		tmp.ouid							=	@ctxt_ouinstance

	--Pay term details 
	UPDATE	tmp
	SET		ft_due_days							=	dtl.PyTmDt_Due_Days,
			ft_penalty							=	dtl.PyTmDt_Penalty_Perc
	FROM	pso_invoice_tmp							tmp 
	JOIN	Pt_PyTmDt_Payment_Term_Dtl				dtl WITH(NOLOCK)
	ON		PYTMDT_PAY_TERM_CODE				=	tmp.pay_term
	AND		PYTMDT_CREATED_OUINSTANCE			=	tmp.ouid
	WHERE	guid								=	@hguid_able
	AND		ouid								=	@ctxt_ouinstance
	
	--select	dtl.PyTmDt_Due_Days ,dtl.PyTmDt_Penalty_Perc,
	--		dtl.PyTmDt_Due_Perc,hdr.PyTmHd_Pay_Term_Code
	--FROM	Pt_PyTmDt_Payment_Term_Dtl dtl	WITH(NOLOCK)
	--JOIN	Pt_PyTmHd_Payment_Term_Hdr hdr	WITH(NOLOCK)
	--ON		dtl.PYTMDT_CREATED_OUINSTANCE		=	hdr.PYTMHD_CREATED_OUINSTANCE
	--AND		dtl.PYTMDT_PAY_TERM_CODE			=	hdr.PYTMHD_PAY_TERM_CODE

	SELECT		DISTINCT
				
				dbo.trm(hdr.hd_address_1) + CONCAT (CHAR(13) , CHAR(10)) +
				dbo.trm(hdr.hd_address_2)+ ',' +dbo.trm(hdr.hd_address_3)+','+dbo.trm(hdr.hd_city)+ ',' +dbo.trm(hdr.hd_state)+ ',' + dbo.trm(hdr.hd_country) + CONCAT (CHAR(13) , CHAR(10)) + 
				'Attention: '+ dbo.trm(dbo.CapitalizeFirstLetter((hdr.hd_attention))) + CONCAT (CHAR(13) , CHAR(10)) + 
				'Email: ' + dbo.trm(lower(hdr.hd_receivable_mail)) + CONCAT (CHAR(13) , CHAR(10))+ 
				'Web site: '+dbo.trm(lower(hdr.hd_website))					'hd_add_single_data',
				hdr.hd_ou_name												'hd_ou_name',
				hdr.hd_address_1											'hd_address_1',
				hdr.hd_address_2+','+hd_address_3+','+
				hd_city+','+hd_state+','+
				hd_country													'hd_address_others',
				hdr.hd_attention											'hd_attention',
				hdr.hd_receivable_mail										'hd_receivable_mail',
				lower(hdr.hd_website)										'hd_website',
				tmp.hd_invoice_no											'hd_invoice_no',
				tmp.hd_invoice_last_mdfd_date								'hd_invoice_last_modified_date',
				cus_bill_to_customer										'cus_no',
				cus_name													'cus_name',
				cus_bill_to_customer+'/'+cus_name							'cus_no_and_cus_name',
				cus_po_no_ref												'cus_po_no_ref',
				cus_part_sale_order_no										'cus_part_sale_order_no',
				cus_currency												'cus_currency',
				cus_address_1+cus_address_2									'cus_address_1_and_2',
				cus_address_3												'cus_address_3',
				cus_state+','+cus_city+','+cus_zip							'cus_state_city_zip',
				cus_country													'cus_country',
				part.part_line_num											'part_auto_num',
				part.part_no												'part_no',
				part.part_description										'part_description',
				part.part_unit_price										'part_unit_price',
				part.part_net_value											'part_net_value',
				part.part_qty												'part_qty',
				upper(part.uom)												'part_uom',
				dbo.get_serial_lot(part.part_serial_no,part.part_lot_no) 	'part_serial_no_lot_no',
				tcd.tcd_auto_num											'tcd_auto_num',
				tcd.tcd_no													'tcd_no',
				tcd.tcd_description											'tcd_description',
				tcd.tcd_type												'tcd_type',
				tcd.tcd_variant_no											'tcd_variant_no',
				tcd.tcd_rate												'tcd_rate',
				tcd.tcd_amount												'tcd_amount',
				tcd.tcd_subtotal											'tcd_subtotal',
				inv_comments												'inv_comments',
				ac_company_name												'ac_company_name',
				ac_bank_name												'ac_bank_name',
				ac_inst_address												'ac_inst_address',
				ac_account_no												'ac_account_no',
				ac_currency													'ac_currency',
				ac_account_no+' '+ac_currency								'ac_account_no_and_currency',
				ac_swift_code												'ac_swift_code',
				apprd_user_name												'apprd_user_name',
				apprd_total_amount											'apprd_total_amount',
				apprd_currency												'apprd_currency',
				upper(apprd_signature)										'apprd_signature', 
				--'01-PS'														'apprd_signature',
				ft_due_days													'ft_due_days',
				ft_penalty													'ft_penalty',
				DBO.RAS_GETDATE(@ctxt_ouinstance)							'ft_cur_date_time',
				'YYYY-MM-DD hh:mm:ss'										'ft_dtm_format_from_ou'
	FROM		pso_invoice_tmp							tmp
	JOIN		pso_inv_hdr_dtl_tmp						hdr WITH(NOLOCK)
	ON			hdr.guid							=	tmp.guid
	AND			hdr.company_code					=	tmp.company_id
	JOIN		pso_inv_part_dtl_tmp					part WITH(NOLOCK)
	ON			part.guid							=	tmp.guid
	AND			part.part_sale_order_no				=	tmp.cus_part_sale_order_no
	LEFT JOIN	pso_inv_tcd_dtl_tmp						tcd WITH(NOLOCK)
	ON			tcd.guid							=	tmp.guid
	AND			tcd.part_sale_order_no				=	tmp.cus_part_sale_order_no
	WHERE		tmp.guid							=	@hguid_able
	AND			tmp.hd_invoice_no					=	'PSINV0000022017'
	-- PSINV0000022017
--PSINV0000032017
--PSINV0000042017
	DELETE FROM pso_inv_hdr_dtl_tmp		WHERE guid = @hguid_able
	DELETE FROM pso_inv_tcd_dtl_tmp		WHERE guid = @hguid_able
	DELETE FROM pso_inv_part_dtl_tmp	WHERE guid = @hguid_able
	DELETE FROM pso_invoice_tmp			WHERE guid = @hguid_able

END



