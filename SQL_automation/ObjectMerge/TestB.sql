/*$file_version=ms4.3.0.07$*/
/******************************************************************************/
/* procedure					: wma_gr_multi_su_sp_cmn_exe	 */
/* description					: 								 */
/******************************************************************************/
/* project						: 								 */
/* ecrno						: 								 */
/* version						: ms4.3.0.0						 */
/******************************************************************************/
/* referenced					: 								 */
/* tables						: 								 */
/******************************************************************************/
/* development history			: 								 */
/******************************************************************************/
/* author						: Ragunath C					 */
/* date							: 01 Apr 2019					 */
/* Defect ID					: MULTI_SU_01					 */
/******************************************************************************/
/* modification history			: 								 */
/******************************************************************************/
/* modified by					: 								 */
/* date							: 								 */
/* description					: 								 */
/* Ragunath C					12 Jul 2019			EPE-14453	 */
/* Ragunath C					17 Jul 2019			EPE-14999				  */
/* Ragunath C					24 Jul 2019			LRT-511					  */
/* Deepti G                     25 Jul 2019         LRT-574                   */
/* Nandhini V                   26 Jul 2019         LRT-656                   */
/* Ragunath C					26 Jul 2019			LRT-707					  */
/* Ragunath C					26 Jul 2019			LRT-593					  */
/* Deepti G                     29 Jul 2019         LRT-780                   */
/* Ragunath C					01 AUG 2019			LRT-802					  */
/* Ragunath C					07 Aug 2019			LRT-906					  */
/* Banuchander B				12 Aug 2019			LRT-1025				  */
/* Anupriya S					13 Aug 2019			LRT-1069				  */
/* Banuchander B				14 Aug 2019			LRT-1100				  */
/* Deepti G                     03 Sep 2019         LRT-1252                  */
/* Deepti G                     13 Sep 2019         LRT-1456                  */
/* Nandhini V                   18 Sep 2019         LRT-1387                  */
/* Ramya Sridhar                27 Sep 2019         LRT-1588                 */
/* Deepti G                     17 Oct 2019         LRT-1618                  */
/* Deepti G                     21 Oct 2019         LRT-1470                  */
/* Satheesh Kumar T             23 Oct 2019         LRT-1595                  */
/* Ramya Sridhar                25 Oct 2019         LRT-1586                 */
/* Ramya Sridhar                01 Nov 2019         LRT-2017                 */
/* Shanthipriya	M				01 Nov 2019			LRT-1971				  */
/* Deepti G                     02 Nov 2019         LRT-1612                  */
/* Shanthipriya	M				02 Nov 2019			LRT-2027				  */
/* kalamani v                   14 jan  2020        lrt-2933                  */
/* kalamani v                   14 jan  2020        lrt-3653                  */	
/* Subashree B					03 Feb 2020			LRT-2650				  */			
/* Ragunath C					05 Feb 2020			LRT-3719				  */
/* Nandhini V					20 Feb 2020			LRT-4101				  */
/* Nandhini V					20 Feb 2020			LRT-4100				  */
/* Nandhini V					21 Feb 2020			LRT-4111				  */
/* Satheesh Kumar T				12 May 2020			LRT-6837				  */
/* Satheesh Kumar T				29 May 2020			LRT-7787				  */
/* Satheesh Kumar T				01 Jun 2020			LRT-7826				  */
/* Satheesh Kumar T				02 Jun 2020			LRT-7726				  */
/* Hari Vignesh G				03 Jun 2020			LRT-7968				  */
/* Syed Tajudeen I				04 Jun 2020			LRT-7566				  */
/* Ragunath C					05 Jun 2020			LRT-8093				  */
/* Nandhini V					06 Jun 2020			LRT-8018				  */
/******************************************************************************/
create procedure wma_gr_multi_su_sp_cmn_exe
	@ctxt_ouinstance				udd_ctxt_ouinstance,   
	@ctxt_user						udd_ctxt_user,   
	@ctxt_language					udd_ctxt_language,   
	@ctxt_service					udd_ctxt_service,  
	@ctxt_role						udd_ctxt_role,   
	@accepted_qty					udd_quantity,   
	@builduid_gr					udd_desc40, 
	@consumables_gr					udd_desc40, 
	@exp_date						udd_date,   
	@guid							udd_guid,   
	@hdnhiddencontrol1				udd_desc255,   
	@hdnhiddencontrol2				udd_desc255,   
	@hiddencontrol1					udd_desc255,   
	@hiddencontrol2					udd_desc255,   
	@hiddencontrol3					udd_desc255,   
	@hiddencontrol4					udd_desc255,   
	@hiddencontrol5					udd_desc255,   
	@hidden_good1					udd_desc255,   
	@hidden_good10					udd_desc255,   
	@hidden_good11					udd_desc255,   
	@hidden_good12					udd_desc255,   
	@hidden_good13					udd_desc255,   
	@hidden_good14					udd_desc255,   
	@hidden_good15					udd_desc255,   
	@hidden_good2					udd_desc255,   
	@hidden_good3					udd_desc255,   
	@hidden_good4					udd_desc255,   
	@hidden_good5					udd_desc255,   
	@hidden_good6					udd_desc255,   
	@hidden_good7					udd_desc255,   
	@hidden_good8					udd_desc255,   
	@hidden_good9					udd_desc255,   
	@item_description_mgexe_dtl		udd_itmdesc,   
	@item_mgexe_dtl					udd_itemcode,   
	@lot_no							udd_desc28,   
	@manu_date						udd_date,   
	@masteruom_gr					udd_uomcode,   
	@master_uom_mgexe_dtl			udd_uomcode,   
	@modeflag						udd_modeflag,   
	@plan_no						udd_documentno,   
	@po_sl_no_mgexe_dtl				udd_desc28,   
	@qty_gr							udd_quantity,   
	@qty_mgexe_dtl					udd_quantity,   
	@rejected_qty					udd_quantity,   
	@re_employee					udd_employeecode,   
	@re_enddatetime					udd_datetime,   
	@re_po_date						udd_date,   
	@re_po_no						udd_documentno,   
	@re_startdatetime				udd_datetime,   
	@serial_no_mgexe_dtl			udd_desc28,   
	@status							udd_desc255,   
	@storage_unit					udd_uomcode,   
	@supplier_wh_batch_no			udd_desc28,   
	@su_qty							udd_quantity,   
	@uid_mgexe_dtl					udd_desc40,   
	@userdefined1					udd_desc255,   
	@userdefined2					udd_desc255,   
	@userdefined3					udd_desc255,   
	@wms_plan_exe_char1				udd_desc255,   
	@wms_plan_exe_char2				udd_desc255,   
	@wms_plan_exe_char3				udd_desc255,   
	@wms_plan_exe_char4				udd_desc255,   
	@wms_plan_exe_char5				udd_desc255,   
	@wms_plan_exe_int1				udd_lineno,   
	@wms_plan_exe_int2				udd_lineno, 
	@hdn_edit_exe_int_01			udd_int,
	@hdn_edit_exe_int_02			udd_int,
	@supplierbatchno_gr				udd_lotnumber,
	@thu_id_editexe					udd_desc40,
	@thu_serialno_editexe			udd_lotnumber,
	@whbatchno_gr					udd_lotnumber,
	@task							udd_desc255,  
	@fprowno						udd_rowno,   
	@customerserialno_man_ml    	udd_desc28,
	@refdocno1_man_ml           	udd_documentno,
	@remarks_man_ml             	udd_desc255,
	@reasoncode_man_ml          	udd_desc40, 
	@reasondescription_man_ml   	udd_desc40, 
	@bestbeforedate_man_ml      	udd_date, 
	@consignee_man_ml           	udd_documentno,
	@odono_man_ml               	documentno,  
	@odoqty_man_ml              	udd_quantity,
	@crossdock_gr_ml				udd_desc20, 
	@man_staging_man_ml         	udd_documentno,
	@stockstatus_gr_ml_rule     	udd_desc255,
	@gr_in_stage_ml             	udd_desc255,
	@gr_pln_coo_ml              	udd_desc50, 
	@gr_pln_inventorytype_ml    	udd_desc40, 
	@gr_pln_itemattribute1_ml   	udd_desc50, 
	@gr_pln_itemattribute2_ml   	udd_desc50, 
	@gr_pln_itemattribute3_ml   	udd_desc50, 
	@gr_pln_itemattribute4_ml   	udd_desc50, 
	@gr_pln_itemattribute5_ml   	udd_desc50, 
	@gr_pln_productstatus_ml    	udd_desc40, 
	@gr_thu_type_ml             	udd_desc40, 
	@gr_to_stage_ml             	udd_desc255,
	@gr_palletstatus            	udd_desc255, 
	@gr_pln_lottable10_ml       	udd_ouinstdesc,  
	@gr_pln_lottable1_ml        	udd_ouinstdesc,  
	@gr_pln_lottable2_ml        	udd_ouinstdesc,  
	@gr_pln_lottable3_ml        	udd_ouinstdesc,  
	@gr_pln_lottable4_ml        	udd_date,  
	@gr_pln_lottable5_ml        	udd_date,  
	@gr_pln_lottable6_ml        	udd_ouinstdesc,  
	@gr_pln_lottable8_ml        	udd_ouinstdesc,  
	@gr_pln_lottable9_ml        	udd_ouinstdesc,
	@gr_pln_callout_ml          	udd_desc255, 
	@gr_pln_calluot_char1_ml    	udd_desc255, 
	@gr_pln_calluot_char2_ml    	udd_desc255, 
	@gr_pln_calluot_date_ml     	udd_date, 
	@gr_pln_calluot_int1_ml     	udd_lineno, 
	@gr_pln_calluot_int2_ml 	udd_lineno, 
	@gr_pln_calluot_int3_ml     	udd_value, 
	@gr_exec_kit_item_line_no   	udd_lineno,
	@su_2_qty						udd_quantity,	
	@su_2_dtl						udd_uomcode,	
	@uid_2_srl_no					udd_lotnumber,
	@asn_ord_qty_dtl				udd_quantity,
	@order_uom_dtl					udd_uomcode,
	@asn_serialno__gr_pln_ml		udd_lineno,	
	@fn_prof_type					udd_metadata_code,
	--@m_errorid						udd_int output 
This is an extra line in B 