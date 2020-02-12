
/* 

File Name                   : shipping cost 
Version                     : 1.0										  
Procedure                   : shpping_cost
Description                 : 
Pending cases               :
Open issues					:
																	  
****************************************************************************
Author                      : Ajithkumar M 							          
Date                        : 28 JAN 2020								  
ID                          : AHXI-103                                                      							 
*************************Modification History*******************************

V - 1.0 - Initial version  - 28/01/2020
																			  
****************************************************************************
*/

ALTER	PROCEDURE	shipping_cost_pop_sp
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
	SELECT @current_date = dbo.RAS_Getdate(@ctxt_ouinstance)
	
	
	INSERT 	INTO	shipping_cost_tmp	
	(
		order_no,				order_date,			order_type,				ouid,
		customer_no,			contract_no,		revision_no,			guid,
		part_no,				part_description
	) 
	
	
	SELECT	DISTINCT
			DTL.cso_od_ord_no,										MST.cso_od_ord_dt,		'CO',						@ctxt_ouinstance,	
			DTL.cso_od_cust_no,										DTL.cso_od_con_no,		DTL.cso_od_con_revno,		@hguid_able,
			DTL.CSO_OD_Part_No,										null
	FROM 	cso_od_object_dtl										DTL WITH(NOLOCK)
	JOIN	cso_cust_order_mst										MST	WITH(NOLOCK)
	ON		DTL.cso_od_ord_no									=	MST.cso_od_ord_no
	AND		DTL.cso_od_ou_id									=	MST.cso_od_ou_id
	AND		DTL.cso_od_cust_no									=	MST.cso_od_cust_no 
	WHERE	DTL.cso_od_cust_no									=	ISNULL(@customer_no_grid,DTL.cso_od_cust_no)
	AND		DTL.cso_od_ou_id									=	@ctxt_ouinstance
	AND		DTL.cso_od_con_no+'/'+DTL.cso_od_con_revno			=	ISNULL(@contract_no_grid,DTL.cso_od_con_no+'/'+DTL.cso_od_con_revno)
	AND     MST.cso_od_ord_dt										BETWEEN isnull(@date_from_grid,MST.cso_od_ord_dt)	AND isnull(@date_to_grid,MST.cso_od_ord_dt)      
	AND		MST.cso_od_ord_status									NOT	IN ('CNL')
	UNION
	--		Rental Order
	SELECT	DISTINCT
			RNTHDR_RNT_NO,											RNTHDR_RNT_DATE,		'RentOrd',		@ctxt_ouinstance,
			RNTHDR_CUST_CODE,										null,					null,						@hguid_able,
			RntHdr_Part_No,											null	
	FROM	Rnt_RntHdr_Rental_Order_Hdr								rnt WITH(NOLOCK)
	WHERE	RNTHDR_CUST_CODE									=	ISNULL(@customer_no_grid,RNTHDR_CUST_CODE)
	AND		RNTHDR_RNT_OUINSTANCE								=	@ctxt_ouinstance
	AND     RNTHDR_RNT_DATE											BETWEEN isnull(@date_from_grid,RNTHDR_RNT_DATE)	AND isnull(@date_to_grid,RNTHDR_RNT_DATE)      
	AND		RNTHDR_RNT_STATUS										IN ('AMD','CLS','PCL')
	UNION
	
	--		Purchase-order 
	SELECT	DISTINCT
			POITM_PO_NO,											POHDR_PO_DATE,			'PO',					@ctxt_ouinstance,
			POHDR_Pur_TradingPartner,								null,					 null,					@hguid_able,
			poitm_part_no,											null
	FROM	PO_POITM_PO_ITEM_DETAILS								po WITH(NOLOCK)
	JOIN	po_pohdr_po_header										pohdr WITH(NOLOCK)
	ON		po.POITM_PO_NO										=	pohdr.POHDR_PO_NO
	AND		po.POITM_OUINSTANCE									=	pohdr.POHDR_OUINSTANCE
	WHERE	POHDR_Purchase_For									=	'CUS'
	AND		POHDR_Pur_TradingPartner							=	ISNULL(@customer_no_grid,POHDR_Pur_TradingPartner)
	AND		pohdr.POHDR_OUINSTANCE								=	@ctxt_ouinstance
	AND     POHDR_PO_DATE											BETWEEN isnull(@date_from_grid,POHDR_PO_DATE)	AND isnull(@date_to_grid,POHDR_PO_DATE)      
	AND		POHDR_PO_STATUS											IN ('O','Cl','A')	
	UNION 
	--		Part sale order 
	SELECT	DISTINCT
			hdr.pso_no,												hdr.pso_orddt,				'PSO',					@ctxt_ouinstance,
			hdr.pso_custno,											null,						null,					@hguid_able,
			pso_partno,												pso_partdesc
	FROM	pso_info_hdr											hdr WITH(NOLOCK)
	JOIN	pso_prtinfo_dtl											dtl WITH(NOLOCK)
	ON		dtl.pso_no											=	hdr.pso_no
	AND		dtl.pso_ou											=	hdr.pso_ou
	AND		dtl.pso_revno										=	hdr.pso_revno
	WHERE	hdr.pso_custno										=	ISNULL(@customer_no_grid,hdr.pso_custno)
	AND		hdr.pso_ou											=	@ctxt_ouinstance
	AND     hdr.pso_orddt											BETWEEN isnull(@date_from_grid,hdr.pso_orddt)	AND isnull(@date_to_grid,hdr.pso_orddt)      
	AND		hdr.pso_docsts											IN ('APP','CF','CLS','RET')
	UNION
	--		loan order 
	SELECT	DISTINCT
			LOHDR_LO_NO,											LOHDR_LO_DATE,		LOHDR_NUM_TYPE_NUM,				@ctxt_ouinstance,
			LOHDR_TRADINGPARTNER,									null,				null,							@hguid_able,
			LOHdr_Part_No,											null
	FROM	LO_LOHDR_LOAN_ORDER_HDR									WITH(NOLOCK)
	WHERE	LOHDR_LOAN_FOR										=	'CUS'
	AND		LOHDR_TRADINGPARTNER								=	ISNULL(@customer_no_grid,LOHDR_TRADINGPARTNER)
	AND		LOHDR_LO_OUINSTANCE									=	@ctxt_ouinstance
	AND     LOHDR_LO_DATE											BETWEEN isnull(@date_from_grid,LOHDR_LO_DATE)	AND isnull(@date_to_grid,LOHDR_LO_DATE) 
	AND		LOHDR_LO_STATUS											IN ('CLS','AMD','AUT','RET')
	UNION
	--		repair order 
	SELECT	DISTINCT
			ROHD_RO_NO,												ROHd_Created_Date,		'REP',						@ctxt_ouinstance,
			ROHd_Customer_No,										null,					null,						@hguid_able,
			ROHd_RO_Part_No,										null
	FROM	Rep_ROHd_Repair_Order_Hdr								WITH(NOLOCK)
	WHERE	ROHd_Customer_No									=	ISNULL(@customer_no_grid,ROHd_Customer_No)
	AND		ROHD_RO_OUINSTANCE									=	@ctxt_ouinstance
	AND     ROHd_Created_Date										BETWEEN isnull(@date_from_grid,ROHd_Created_Date)	AND isnull(@date_to_grid,ROHd_Created_Date) 
	AND		ROHd_RO_Status											in ('AU','BC','CF','CL')

	UPDATE	tmp
	SET		customer_name										=	CMH_Cust_Name
	FROM	shipping_cost_tmp										tmp 
	JOIN	Cu_CMH_Cust_Master_Hdr									HDR WITH(NOLOCK)
	ON		customer_no											=	CMH_Cust_Code
	AND		ouid												=	CMH_Created_Ouinstance
	WHERE	guid												=	@hguid_able
	AND		ouid												=	@ctxt_ouinstance

	
	--UPDATE	tmp
	--SET		tmp.order_type_defn									=	ord.order_type_defn
	--FROM	shipping_cost_tmp										tmp 
	--JOIN	order_types_tbl_tmp											ord WITH(NOLOCK)
	--ON		ord.order_type										=	tmp.order_type
	--WHERE	guid												=	@hguid_able
	--AND		ouid												=	@ctxt_ouinstance
	
	--purchase order , Loan order and repair order defn 
	UPDATE	tmp
	SET		tmp.order_type_defn									=	parameter_text
	FROM	shipping_cost_tmp										tmp 
	JOIN	fin_quick_code_met										met WITH(NOLOCK)
	ON		met.parameter_code									=	tmp.order_type
	WHERE	component_id										=	'SIN' 
	AND		parameter_type										=	'COMBO'  
	AND		parameter_category									=	'INVCAT'  
	AND		language_id											=	@ctxt_language
	AND		guid												=	@hguid_able
	AND		ouid												=	@ctxt_ouinstance
	
	
	--customer order
	UPDATE	tmp
	SET		tmp.order_type_defn									=	parameter_text
	FROM	shipping_cost_tmp										tmp 
	JOIN	fin_quick_code_met										met WITH(NOLOCK)
	ON		met.parameter_code									=	tmp.order_type
	WHERE	component_id										=	'CDCN' 
	AND		parameter_type										=	'COMBO'  
	AND		parameter_category									=	'REFDOCTYP'
	AND		parameter_code										=	'CO'  
	AND		language_id											=	@ctxt_language
	AND		guid												=	@hguid_able
	AND		ouid												=	@ctxt_ouinstance

	--rental order 
	UPDATE	tmp
	SET		tmp.order_type_defn									=	parameter_text
	FROM	shipping_cost_tmp										tmp 
	JOIN	fin_quick_code_met										met WITH(NOLOCK)
	ON		met.parameter_code									=	tmp.order_type
	WHERE	component_id										=	'CDI' 
	AND		parameter_type										=	'REFDOC'  
	AND		parameter_category									=	'REFDOCTYPE'
	AND		parameter_code										=	'RentOrd'  
	AND		language_id											=	@ctxt_language
	AND		guid												=	@hguid_able
	AND		ouid												=	@ctxt_ouinstance
	
	--part sale order defn 
	UPDATE	tmp
	SET		tmp.order_type_defn									=	parameter_text
	FROM	shipping_cost_tmp										tmp 
	JOIN	fin_quick_code_met										met WITH(NOLOCK)
	ON		met.parameter_code									=	tmp.order_type
	WHERE	component_id										=	'CDI' 
	AND		parameter_type										=	'COMBO'  
	AND		parameter_category									=	'REFDOC'
	AND		language_id											=	@ctxt_language
	AND		guid												=	@hguid_able
	AND		ouid												=	@ctxt_ouinstance

	
	UPDATE	tmp
	SET		part_description									=	LTRIM(RTRIM(PrCrl_Part_Desc))
	FROM	shipping_cost_tmp										tmp 
	JOIN	Prt_PrCrl_CentralRefLISt_Info							part WITH(NOLOCK)   
	ON		part_no												=	PrCrl_Part_No     
	AND		ouid												=	PrCrl_Created_OuInstance
	WHERE	guid												=	@hguid_able
	AND		ouid												=	@ctxt_ouinstance    

	UPDATE	tmp
	SET		shipping_note_no									=	Isu_Rec_Ship_Dtl_NoteNo,
			agency_no											=	Isu_Rec_Ship_CarrierCode,
			freight_amount										=	Isu_Rec_Ship_Fright,
			currency_adn										=	Isu_Rec_Ship_FrightCur,
			issue_ref_doc_no									=	Isu_Rec_Ship_Dtl_IssNo,
			shipping_waybillno									=	Isu_Rec_Ship_WayBillNo,
			ship_to												=	dbo.bas_fetch_inv_param_desc ('BASISSUE' , 'COMBO' , 'SHIPTO' ,  Isu_Rec_Ship_ShipTo ,1), --@ctxt_language
			inco_terms											=	Isu_Rec_Ship_Incocode
	FROM	shipping_cost_tmp										tmp 
	JOIN	Isu_Rec_Ship_Note_Dtl									ship WITH(NOLOCK)
	ON		order_no											=	ship.Isu_Rec_Ship_Dtl_RefDocNo
	AND		ouid												=	ship.Isu_Rec_Ship_Dtl_OU
	JOIN	Isu_Rec_Ship_Note_Hdr									hdr	WITH(NOLOCK)
	ON		Isu_Rec_Ship_Dtl_NoteNo								=	Isu_Rec_Ship_Note_No
	AND		Isu_Rec_Ship_Note_OU								=	ship.Isu_Rec_Ship_Dtl_OU
	AND		Isu_Rec_Ship_Doc_Status									IN ('Confirmed')
	WHERE	guid												=	@hguid_able
	AND		ouid												=	@ctxt_ouinstance
	

	UPDATE	tmp
	SET		advance_shipping_note_no							=	ASNDET_ASN_NO,
			agency_no											=	asnhdr_carrier_agency,
			freight_amount										=	asnhdr_freight_amount,
			currency_adn										=	asnhdr_freight_currency
	FROM	shipping_cost_tmp										tmp 
	JOIN	asn_asndet_asn_detail									ship WITH(NOLOCK)
	ON		order_no											=	ship.ASNDET_REF_DOC_NO
	AND		ouid												=	ship.ASNDET_OUINSTANCE
	JOIN	asn_asnhdr_asn_header									hdr WITH(NOLOCK)
	ON		ship.ASNDET_ASN_NO									=	hdr.ASNHDR_ASN_NO
	AND		ship.ASNDET_OUINSTANCE								=	hdr.ASNHDR_OUINSTANCE
	WHERE	guid												=	@hguid_able
	AND		ouid												=	@ctxt_ouinstance
	
	
	UPDATE	tmp
	SET		issue_date											=	ISUIH_Transaction_Date,
			issue_ref_doc_no									=	ISUIH_TRANSACTION_NO,
			issue_type											=	ISUIH_issue_type,
			issue_type_defn										=	ISUIH_Ref_Doc_Type
	FROM	shipping_cost_tmp										tmp 
	JOIN	Isu_isuih_issue_tran_hdr								hdr WITH(NOLOCK)
	ON		ISUIH_Ref_Doc_No									=	order_no
	AND		ISUIH_ORG_UNIT										=	ouid
	AND		ISUIH_STATUS_CODE									=	'CO'
	AND		guid												=	@hguid_able
	AND		ouid												=	@ctxt_ouinstance
		
	UPDATE	tmp
	SET		issue_date											=	GIHD_RCPT_DATE,
			issue_ref_doc_no									=	GIHD_RCPT_NO,
			issue_type											=	GIHD_RCPT_TYPE,
			issue_type_defn										=	GIHD_REFDOC_TYPE
	FROM	shipping_cost_tmp										tmp 
	JOIN	GI_GIHD_RECEIPT_HDR										gh				
	ON		gh.GIHD_REFDOC_NO									=	tmp.order_no
	WHERE	gh.GIHD_RCPT_DOCSTATUS								=	'CMP'
	AND		gh.GIHD_CUSTNO										=	tmp.customer_no
	AND		gh.GIHD_RCPT_OU										=	ouid 
	AND		guid												=	@hguid_able
	AND		ouid												=	@ctxt_ouinstance


	UPDATE	tmp
	SET		issue_ref_doc_type									=	DBO.Bas_Fetch_Inv_Param_Desc('BASISSUE', 'COMBO', 'ISSTYPE',ISUIH_issue_type ,@ctxt_language)
	FROM	shipping_cost_tmp										tmp 
	JOIN	Isu_isuih_issue_tran_hdr								hdr WITH(NOLOCK)
	ON		issue_ref_doc_no									=	ISUIH_TRANSACTION_NO
	AND		ouid												=	ISUIH_ORG_UNIT
	--JOIN	Isu_issprm_parameter_details							dtl WITH(NOLOCK)
	--ON		IssPrm_ParamCode									=	CASE WHEN ISUIH_Ref_Doc_Type='TLG' THEN 'TL' ELSE  ISUIH_Ref_Doc_Type END 
	--WHERE	IssPrm_ParamCategory								=	'COMBO'       
	--AND		IssPrm_ParamType										IN ('REFDOCTYPE' ,'UPLISU' ) 
	--AND		IssPrm_Langid										=	@ctxt_language 
	AND		guid												=	@hguid_able
	AND		ouid												=	@ctxt_ouinstance
	
	UPDATE	tmp
	SET		issue_ref_doc_type									=	GIPRM_PARAMDESC
	FROM	shipping_cost_tmp										tmp 
	JOIN	GI_GIHD_RECEIPT_HDR										hdr WITH(NOLOCK)
	--ON		issue_ref_doc_no									=	GIHD_RCPT_NO
	ON		order_no												=	GIHD_REFDOC_NO
	AND		GIHD_RCPT_OU										=	ouid
	JOIN	GI_GIPRM_PARAM_DTL										prm		WITH(NOLOCK)
	ON		GIHD_RCPT_TYPE										=	GIPRM_PARAMCODE
	WHERE	GIPRM_COMPONENTNAME									=	'BASGI' 
	AND		GIPRM_PARAMCATEGORY									=	'COMBO' 
	AND		GIPRM_PARAMTYPE										=	'REFDOCTYPE'
	AND		guid												=	@hguid_able
	AND		ouid												=	@ctxt_ouinstance

	--invoice 
	UPDATE	tmp
	SET		supplier_invoice_type								=	hdr.tran_type,
			supplier_invoice_no									=	hdr.tran_no,
			invoice_date										=	hdr.supp_invoice_date,
			currency											=	hdr.tran_currency,
			supplier_provided_invoice_no 						=	hdr.supp_invoice_no,
			supplier_invoice_amount 							=	hdr.supp_invoice_amount
	FROM	shipping_cost_tmp										tmp 
	--JOIN	sin_delivery_charge_dtl									dtl WITH(NOLOCK) -- Can be enabled to filter delivery charge invoice only 
	JOIN	sin_item_dtl											dtl WITH(NOLOCK) 
	ON		issue_ref_doc_no									=	dtl.ref_doc_no
	AND		ouid												=	dtl.tran_ou
	AND		order_no											=	dtl.po_no -- can be enabled for order number matching 
	JOIN	sin_invoice_hdr											hdr WITH(NOLOCK)
	ON		dtl.tran_no											=	hdr.tran_no
	AND		dtl.tran_ou											=	hdr.tran_ou
	WHERE	guid												=	@hguid_able
	AND		ouid												=	@ctxt_ouinstance

	
	UPDATE	tmp
	SET		invoice_category									=	met.parameter_text
	FROM	shipping_cost_tmp										tmp 
	JOIN	sin_invoice_hdr											hdr WITH(NOLOCK)
	ON		supplier_invoice_no									=	tran_no						
	JOIN	fin_quick_code_met										met with(nolock)
	ON		hdr.dc_invoice_type									=	parameter_code
	WHERE  	component_id 										=	'SIN'

	--PURCHASE REASON  
	--NOTE  : COLUMN IS AVAILABLE IN ED5 SERVER ONLY 

	--UPDATE	tmp
	--SET		reason_for_purchase				=	POITM_PURCHASE_REASON 
	--FROM	shipping_cost_tmp					tmp 
	--JOIN	po_poitm_po_item_details			po WITH(NOLOCK)
	--ON		order_no						=	POITM_PO_NO
	--AND		ouid							=	POITM_OUINSTANCE
	--WHERE	guid							=	@hguid_able
	--AND		ouid							=	@ctxt_ouinstance


END

