select contract_no,revision_no from shipping_cost_tmp
select contract_no_rev_no from shipping_cost_tmp

create synonym shipping_cost_tmp for AVNAPPDB_TEMPDB..shipping_cost_tmp

drop  synonym shipping_cost_tmp 

drop table shipping_cost_tmp

create table shipping_cost_tmp
		(
		customer_no						udd_customer_id,
		customer_name					udd_custname,
		order_type						udd_txt255,
		order_no						udd_refdocno,
		contract_no						udd_refdocno,
		revision_no						udd_refdocno,
		order_date						udd_date,
		reason_for_purchase				udd_txt255,
		advance_shipping_note			udd_txt255,
		shipping_note					udd_txt255,
		part_no							udd_refdocno,
		part_description				udd_txt255,
		ref_doc_type					udd_txt255,
		ref_doc_no						udd_refdocno,
		agency_no						udd_refdocno,
		freight_amount					udd_cost,
		currency_adn					udd_txt25,
		supplier_invoice_type			udd_txt255,
		supplier_invoice_no				udd_refdocno,
		invoice_date					udd_date,
		invoice_category				udd_txt255,
		currency						udd_txt25,
		supplier_provided_invoice_no	udd_refdocno,
		supplier_invoice_amount			udd_refdocno,
		guid							udd_guid,
		ouid							udd_ctxt_ouinstance
		)

--
use avnappdb

create synonym shipping_cost_tmp for avnappdb_tempdb..shipping_cost_tmp
drop synonym shipping_cost_tmp

sp_rename 'shipping_cost_tmp.shipping_note','shipping_note_no'
sp_rename 'shipping_cost_tmp.advance_shipping_note','advance_shipping_note_no'
sp_rename 'shipping_cost_tmp.ref_doc_type','issue_ref_doc_type'
sp_rename 'shipping_cost_tmp.ref_doc_no','issue_ref_doc_no'
sp_rename 'shipping_cost_tmp.issue_type','issue_type_defn'
sp_rename 'shipping_cost_tmp.issue_type','issue_type_defn'

alter table shipping_cost_tmp add supplier_code udd_refdocno
--altering date 
alter table shipping_cost_tmp alter column invoice_date	fin_date
alter table shipping_cost_tmp alter column order_date	fin_date
alter table shipping_cost_tmp add order_type_defn udd_txt25

alter table shipping_cost_tmp add issue_no udd_refdocno
alter table shipping_cost_tmp add issue_type udd_txt25
alter table shipping_cost_tmp add issue_date fin_date
alter table shipping_cost_tmp add issue_ref_doc_no_defn udd_txt25
alter table shipping_cost_tmp add shipping_waybillno udd_refdocno

alter table shipping_cost_tmp add ship_to udd_txt25
alter table shipping_cost_tmp add inco_terms udd_txt25





--alter table shipping_cost_tmp add contract_no	udd_refdocno
--alter table shipping_cost_tmp add revision_no	udd_txt25

--delete invoice_date from shipping_cost_tmp

--update shipping_cost_tmp
--set invoice_date =null
--where invoice_date is not null 

--update shipping_cost_tmp
--set order_date =null
--where order_date is not null 



--create synonym shipping_cost_delivery_tmp for AVNAPPDB_TEMPDB..shipping_cost_delivery_tmp

--drop table shipping_cost_delivery_tmp

--create table shipping_cost_deliv_details_tmp
--		(
--		ref_document_no				udd_refdocno,
--		ref_document_type			udd_txt25,
--		supp_no						udd_refdocno,
--		tran_currency				udd_txt25,
--		supp_provided_invoice_no	udd_refdocno,
--		supp_invoice_amount			udd_cost,
--		supp_invoice_date			fin_date,
--		freight_amount				udd_cost,
--		invoice_cat_code			udd_refdocno,
--		invoice_category			udd_txt255,
--		supp_invoice_type			udd_txt255,
--		supp_invoice_no				udd_refdocno,
--		guid						udd_guid,
--		ouid						udd_ctxt_ouinstance
--		)



--sp_rename 'shipping_cost_delivery_tmp','shipping_cost_deliv_details_tmp' 

--alter table add





--reate table shipping_cost_tmp
--		(
--		shipping_note_no				udd_refdocno,
--		part_no							udd_refdocno,
--		part_description				udd_txt255,
--		ref_doc_type					udd_txt255,
--		ref_doc_no						udd_refdocno,
--		ref_doc_date					fin_date,
--		parent_ref_doc_type				udd_txt255,
--		parent_ref_doc_no				udd_refdocno)

--		select distinct ref_doc_type
--		from sin_item_dtl

truncate table shipping_cost_tmp
