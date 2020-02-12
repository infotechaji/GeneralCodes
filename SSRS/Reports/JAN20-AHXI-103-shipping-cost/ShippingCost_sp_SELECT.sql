
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

--drop procedure shipping_cost_sp
ALTER	
--CREATE 
PROCEDURE	shipping_cost_chrg_back_to_customer_sp
		
		@hguid_able						udd_guid
		
AS 
BEGIN
	SELECT  
			customer_no							'customer_no',
			customer_name						'customer_name',
			order_type							'order_type',
			order_type_defn						'order_type_defn',
			order_no							'order_no',
			case when contract_no is not null
			then contract_no+'/'+revision_no						
			ELSE '' END as						'contract_no',
			revision_no							'revision_no',
			cast(order_date as date)			'order_date',
			reason_for_purchase					'reason_for_purchase',
			part_no								'part_no',
			part_description					'part_description',
			shipping_note_no					'shipping_note',
			advance_shipping_note_no			'advance_shipping_note_no',
			issue_ref_doc_type					'ref_doc_type',
			issue_ref_doc_no					'ref_doc_no',
			agency_no							'agency_no',
			freight_amount						'freight_amount',
			currency_adn						'currency',
			supplier_invoice_type				'supplier_invoice_type',
			supplier_invoice_no					'supplier_invoice_no',
			invoice_date						'invoice_date',
			invoice_category					'invoice_category',
			currency							'invoice_currency',
			supplier_provided_invoice_no		'supplier_provided_invoice_no',
			supplier_invoice_amount				'supplier_invoice_amount'
			
	FROM	shipping_cost_tmp
	WHERE	shipping_note_no is not null 
	AND		guid							=	@hguid_able
	
	
	DELETE 
	FROM	shipping_cost_tmp
	WHERE	guid							=	@hguid_able

END




--exec shipping_cost_chrg_back_to_customer_sp '12346'

--select * from shipping_cost_tmp

--truncate table shipping_cost_tmp
