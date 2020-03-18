

select top 10 * from cdi_invoice_hdr
select top 10 * from emod_ou_mst_vw 
select top 10 * from emod_ou_addr_map_vw

select head.tran_ou H_OU,head.fb_id H_FB_ID,
ouinstname,ouinstdesc,bu_id,bu_name,company_code,company_name,map_status,op_code,stn_code,logo_name
from 
cdi_invoice_hdr head
join emod_ou_mst_vw  ouview on(head.tran_ou=ouview.ou_id)

select distinct address1,city,state,country,zip_code
from emod_ou_addr_map_vw


select distinct top 20  
ou_id=e1.ou_id,
company_name=e1.company_name,
			company_addressline1=e2.address_desc,
			company_addressline2=e2.address1,
			company_addressline3=e2.city +' '+e2.state+' '+e2.country,
			phone1   =e2.phone_no,
			pincode=e2.zip_code,
			org_no   =e2.address3 ,
			company_url=e2.url,
			company_code=e1.company_code
		--select e2.*
		from cdi_invoice_hdr  t 
		INNER JOIN emod_ou_mst_vw e1 with (nolock)
			ON     e1.map_status   = 'M'
			and e1.ou_id        = t.tran_ou
			INNER JOIN emod_ou_addr_map_vw e2 with (nolock)
		ON e1.company_code = e2.company_code


--select top 10 * from cdi_invoice_hdr

Cu_CMH_Cust_Master_Hdr

select  CMH_Cust_Code,CMH_Cust_Name,CMH_Url_Id,CMH_ValidTillDate,CMH_Mobile_No,CMH_Address1 +'\n'+ CMH_Address2 +'\n'+ CMH_Address3 Full_address,CMH_City,CMH_ZipCode,CMH_State,CMH_Country
from Cu_CMH_Cust_Master_Hdr where CMH_Cust_Name not like 'Customer%'
and CMH_Country is not null 

select count(*) from emod_ou_addr_map_vw

