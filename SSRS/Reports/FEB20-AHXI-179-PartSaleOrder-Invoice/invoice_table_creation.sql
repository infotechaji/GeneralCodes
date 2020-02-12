

CREATE SYNONYM pso_invoice_tmp FOR AVNAPPDB_TEMPDB..pso_invoice_tmp

CREATE TABLE  pso_invoice_tmp
(
hd_ou_name				udd_txt255,
hd_address_1			udd_txt255,
hd_address_others		udd_txt2000,
hd_attention			udd_txt255,
hd_receivable_mail		udd_txt255,
hd_website				udd_txt255,
hd_invoice_no			udd_refdocno,
hd_invoice_no_date		fin_date,
cus_no					udd_refdocno,
cus_name				udd_txt255,
cus_po_no_ref			udd_refdocno,
cus_part_sale_order_no	udd_refdocno,
cus_currency			udd_txt25,
cus_address_1_2			udd_txt255,
cus_address_3			udd_txt255,
cus_state_city_zip		udd_txt255,
cus_country				udd_txt25,
part_auto_num			udd_txt25,
part_no					udd_refdocno,
part_description		udd_txt255,
part_unit_price			udd_cost,
part_net_value			udd_cost,
part_sub_total			udd_cost,
tcd_auto_num			udd_txt25,
tcd_no					udd_refdocno,
tcd_description			udd_txt255,
tcd_type				udd_txt255,
tcd_variant_no			udd_refdocno,
tcd_rate				udd_cost,
tcd_amount				udd_cost,
tcd_subtotal			udd_cost,
inv_comments			udd_txt255,
ac_company_name			udd_txt255,
ac_bank_name			udd_txt255,
ac_inst_address			udd_txt255,
ac_account_no			udd_refdocno,
ac_currency				udd_txt25,
ac_swift_code			udd_refdocno,
apprd_user_name			udd_txt255,
apprd_total_amount		udd_cost,
apprd_currency			udd_txt25,
apprd_signature			udd_txt25,
ft_due_days				udd_txt25,
ft_penalty				udd_txt25,
ft_cur_date_time		udd_datetime,
ft_dtm_format_from_ou	udd_txt255,
ouid					udd_ctxt_ouinstance,
guid					udd_guid
)


ALTER TABLE pso_invoice_tmp ADD hd_invoice_status_code udd_txt25
ALTER TABLE pso_invoice_tmp ADD hd_invoice_tran_type udd_txt25
sp_rename 'pso_invoice_tmp.cus_no','cus_bill_no_and_cus_name'
ALTER TABLE pso_invoice_tmp alter column cus_bill_no_and_cus_name udd_txt255

ALTER TABLE pso_invoice_tmp ADD company_id udd_txt25
sp_rename 'pso_invoice_tmp.hd_invoice_no_date','hd_invoice_last_mdfd_date'

ALTER TABLE pso_invoice_tmp ADD pso_issue_no udd_refdocno
ALTER TABLE pso_invoice_tmp ADD pso_shipping_note_no udd_refdocno
ALTER TABLE pso_invoice_tmp ADD pso_ref_doc_type udd_txt255
bill_to_id


ALTER TABLE pso_invoice_tmp ALTER COLUMN cus_name udd_txt255
sp_rename 'pso_invoice_tmp.cus_bill_no_and_cus_name','cus_bill_to_customer'

ALTER TABLE pso_invoice_tmp ADD bill_to_id udd_refdocno 
ALTER TABLE pso_invoice_tmp ADD custno		udd_refdocno

ALTER TABLE pso_invoice_tmp ADD ac_bank_ref_no	udd_refdocno
ALTER TABLE pso_invoice_tmp ADD ac_company_code	udd_refdocno

ALTER TABLE pso_invoice_tmp ADD pay_term udd_refdocno

pay_term

cus_bill_to_customer,

cus_address_1
cus_address_2
cus_address_3
cus_state
cus_city
cus_zip
cus_country

sp_rename 'pso_invoice_tmp.cus_address_1_2','cus_address_1'
sp_rename 'pso_invoice_tmp.cus_state_city_zip','cus_address_2'
ALTER TABLE pso_invoice_tmp ADD cus_state	udd_txt255
ALTER TABLE pso_invoice_tmp ADD cus_city	udd_txt255
ALTER TABLE pso_invoice_tmp ADD cus_country	udd_txt255
ALTER TABLE pso_invoice_tmp ADD cus_zip		udd_txt255
			


-- for header company details 
CREATE TABLE pso_inv_hdr_dtl_tmp
(company_code		udd_refdocno,
hd_ou_name			udd_txt255, 
hd_address_1		udd_txt255,
hd_address_others	udd_txt2000,
hd_receivable_mail	udd_txt255,
hd_website			udd_txt255
) 

CREATE SYNONYM pso_inv_hdr_dtl_tmp FOR AVNAPPDB_TEMPDB..pso_inv_hdr_dtl_tmp

ALTER TABLE pso_inv_hdr_dtl_tmp ADD ouid ctxt_ouinstance
ALTER TABLE pso_inv_hdr_dtl_tmp ADD guid udd_guid
ALTER TABLE pso_inv_hdr_dtl_tmp ADD address2 udd_txt255
ALTER TABLE pso_inv_hdr_dtl_tmp ADD address3 udd_txt255
ALTER TABLE pso_inv_hdr_dtl_tmp ADD city udd_txt255
ALTER TABLE pso_inv_hdr_dtl_tmp ADD state udd_txt255
ALTER TABLE pso_inv_hdr_dtl_tmp ADD country udd_txt255
ALTER TABLE pso_inv_hdr_dtl_tmp ADD hd_attention udd_txt255
ALTER TABLE pso_inv_hdr_dtl_tmp ADD hd_invoice_no udd_refdocno
ALTER TABLE pso_inv_hdr_dtl_tmp ADD hd_invoice_last_mdfd_date fin_date



sp_rename 'pso_inv_hdr_dtl_tmp.address2','hd_address_2'
sp_rename 'pso_inv_hdr_dtl_tmp.address3','hd_address_3'
sp_rename 'pso_inv_hdr_dtl_tmp.city','hd_city'
sp_rename 'pso_inv_hdr_dtl_tmp.state','hd_state'
sp_rename 'pso_inv_hdr_dtl_tmp.country','hd_country'


CREATE SYNONYM pso_inv_part_dtl_tmp FOR AVNAPPDB_TEMPDB..pso_inv_part_dtl_tmp
--drop synonym pso_inv_part_dtl_tmp

CREATE TABLE pso_inv_part_dtl_tmp
(
part_sale_order_no	udd_refdocno,
part_line_num		int,
part_no				udd_txt255,
part_description	udd_txt255,
part_qty			fin_quantity,
uom					udd_txt255,
part_serial_no		udd_txt255,
part_lot_no			udd_txt255,
part_unit_price		fin_amount,
part_net_value		fin_amount,
ouid ctxt_ouinstance,
guid udd_guid
)


CREATE TABLE pso_inv_tcd_dtl_tmp
(
part_sale_order_no		udd_refdocno,
tcd_auto_num			udd_txt25,
tcd_no					udd_refdocno,
tcd_description			udd_txt255,
tcd_type				udd_txt255,
tcd_variant_no			udd_refdocno,
tcd_rate				udd_cost,
tcd_amount				udd_cost,
tcd_subtotal			udd_cost,
ouid					ctxt_ouinstance,
guid					udd_guid
)


CREATE Synonym pso_inv_tcd_dtl_tmp for AVNAPPDB_TEMPDB..pso_inv_tcd_dtl_tmp
	--DROP table pso_inv_tcd_dtl_tmp
	sp_rename 'pso_inv_tcd_dtl_tmp' ,'pso_inv_tcd_dtl_tmp_can_delete'

	sp_rename 'pso_inv_tcd_dtl_tmp.part_sale_order_no','tcd_invoice_no'

	alter table pso_inv_tcd_dtl_tmp add part_sale_order_no udd_refdocno
	sp_rename 'pso_inv_tcd_dtl_tmp.tcd_invoice_no','part_sale_order_no'



	select * FROM pso_inv_hdr_dtl_tmp	WHERE guid = '12345'
	select * FROM pso_inv_tcd_dtl_tmp	WHERE guid = '12345'
	select * FROM pso_inv_part_dtl_tmp	WHERE guid = '12345'
	select * FROM pso_invoice_tmp		WHERE guid = '12345'

	select * FROM pso_inv_hdr_dtl_tmp	
	select * FROM pso_inv_tcd_dtl_tmp	
	select * FROM pso_inv_part_dtl_tmp	
	select * FROM pso_invoice_tmp		

	truncate table pso_inv_hdr_dtl_tmp
	truncate table pso_inv_tcd_dtl_tmp
	truncate table pso_inv_part_dtl_tmp
	truncate table pso_invoice_tmp

	delete FROM pso_inv_hdr_dtl_tmp	WHERE guid = '12345'
	delete FROM pso_inv_tcd_dtl_tmp	WHERE guid = '12345'
	delete FROM pso_inv_part_dtl_tmp	WHERE guid = '12345'
	delete FROM pso_invoice_tmp		WHERE guid = '12345'