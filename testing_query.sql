INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'url_status', 'Started',2
update A set access_restricted=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> A join (select distinct company_id from core_automation.company_attributes<table_suffix> where attribute_name='url_status' and (attribute_value='Forbidden' or attribute_value='Unauthorized'))B on A.company_id=B.company_id where A.access_restricted is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'url_status', 'Completed',2

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'accreditated_business', 'Started',3
update A set accreditated_business=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> A join core_automation.company_attributes<table_suffix> B on A.company_id=B.company_id where attribute_name='Other Domains' and attribute_value in ('ebit','bbb','findsmiley','soliditet','trustpilot','cnil','kununu','ekomi','certipedia','nic','sebi','soliditet','pts', 'sqs','ofsted','fca','cqc','rics','fsb','bbb','sipc','angieslist') and accreditated_business is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'accreditated_business', 'Completed',3

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'ajax_request', 'Started',4
update A set ajax_request=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> A join core_automation.company_attributes<table_suffix> B on A.company_id=B.company_id where B.attribute_name='Ajax Request' and ajax_request is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'ajax_request', 'Completed',4

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'b2b_b2c_flag', 'Started',5
update A set b2b_b2c_flag='B2B' from core_automation.product_generic_modelling_temp<mod_table_suffix> A join( select distinct company_id from core_automation.company_attributes<table_suffix> where attribute_name in ('description','og:description') and (attribute_value LIKE '%b2b%' OR attribute_value LIKE '%client%' OR attribute_value LIKE '%help business%' OR attribute_value LIKE '%helps business%' OR attribute_value LIKE '%help compan%' OR attribute_value LIKE '%helps compan%' OR attribute_value LIKE '%your business%' OR attribute_value LIKE '%your customer%' OR attribute_value LIKE '%your organization%' OR attribute_value LIKE '%your organisation%' OR attribute_value LIKE '%services to compan%' OR attribute_value LIKE '%service to compan%'  OR attribute_value LIKE '%services to business%' OR attribute_value LIKE '%service to business%' OR attribute_value LIKE '%manufacture %for industr%' OR attribute_value LIKE '%manufacture %for compan%' OR attribute_value LIKE '%deliver %to industr%' OR attribute_value LIKE '%deliver %to compan%' OR attribute_value LIKE '%wholesale%' OR attribute_value LIKE '%distribut%' OR attribute_value LIKE '%partner%' OR attribute_value LIKE '%help professional%' OR attribute_value LIKE '%serve professional%'))B on A.company_id=B.company_id where b2b_b2c_flag is null


update A set b2b_b2c_flag='B2B' from core_automation.product_generic_modelling_temp<mod_table_suffix> A join( SELECT distinct company_id FROM core_automation.company_info<table_suffix> WHERE summary IS NOT NULL AND ( summary LIKE '%b2b%' OR summary LIKE '%client%' OR summary LIKE '%help business%' OR summary LIKE '%helps business%' OR summary LIKE '%help compan%' OR summary LIKE '%helps compan%' OR summary LIKE '%your business%' OR summary LIKE '%your customer%' OR summary LIKE '%your organization%' OR summary LIKE '%your organisation%' OR summary LIKE '%services to compan%' OR summary LIKE '%service to compan%' OR summary LIKE '%services to business%' OR summary LIKE '%service to business%' OR summary LIKE '%manufacture %for industr%' OR summary LIKE '%manufacture %for compan%' OR summary LIKE '%deliver %to industr%' OR summary LIKE '%deliver %to compan%' OR summary LIKE '%wholesale%' OR summary LIKE '%distribut%' OR summary LIKE '%partner%' OR summary LIKE '%help professional%' OR summary LIKE '%serve professional%' ))B on A.company_id=B.company_id where b2b_b2c_flag is null

update A set b2b_b2c_flag='B2C' from core_automation.product_generic_modelling_temp<mod_table_suffix> A join( select distinct company_id from core_automation.company_attributes<table_suffix> where attribute_name in ('description','og:description') and (attribute_value LIKE '%b2c%' OR attribute_value LIKE '%customer%' OR attribute_value LIKE '%help people%' OR attribute_value LIKE '%helps people%' OR attribute_value LIKE '%sell%' OR attribute_value LIKE '%individual%' OR attribute_value LIKE '%famil%' OR attribute_value LIKE '%lives%') )B on A.company_id=B.company_id where b2b_b2c_flag is null 


update A set b2b_b2c_flag='B2C' from core_automation.product_generic_modelling_temp<mod_table_suffix> A join( SELECT distinct company_id FROM core_automation.company_info<table_suffix> WHERE summary IS NOT NULL AND ( summary LIKE '%b2c%' OR summary LIKE '%customer%' OR summary LIKE '%help people%' OR summary LIKE '%helps people%' OR summary LIKE '%sell%' OR summary LIKE '%individual%' OR summary LIKE '%famil%' OR summary LIKE '%lives%' ))B on A.company_id=B.company_id where b2b_b2c_flag is null

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'b2b_b2c_flag', 'Completed',5

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'live_chat', 'Started',6
update A set live_chat = 1 from core_automation.product_generic_modelling_temp<mod_table_suffix> A join core_automation.company_attributes<table_suffix> B on A.company_id=B.company_id where attribute_name='Live Chat' and live_chat is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'live_chat', 'Completed',6


INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'meta_description', 'Started',8
update a set meta_description = 1 from core_automation.product_generic_modelling_temp<mod_table_suffix> a where exists(select 1 from core_automation.company_attributes<table_suffix> b where a.company_id=b.company_id and attribute_name in ('og:description', 'meta_description')) and meta_description is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'meta_description', 'Completed',8

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'meta_keywords', 'Started',9
update a  set meta_keywords = 1 from core_automation.product_generic_modelling_temp<mod_table_suffix> a where exists(select 1 from core_automation.company_attributes<table_suffix> b where a.company_id=b.company_id and attribute_name ='meta') and meta_keywords is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'meta_keywords', 'Completed',9

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'offers_flag', 'Started',10
update a set offers_flag = 1 from core_automation.product_generic_modelling_temp<mod_table_suffix> a where exists (select 1 from core_automation.company_attributes<table_suffix> b where (attribute_name in ('discounts','gift_cards') and attribute_value='Yes') and a.company_id=b.company_id) and offers_flag is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'offers_flag', 'Completed',10

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'other_email', 'Started',11
update A set other_email=B.score from core_automation.product_generic_modelling_temp<mod_table_suffix> A join(select company_id, count(*) as score from ( select distinct a.company_id, attribute_name,a.attribute_value, b.domain_name from core_automation.company_attributes<table_suffix> a join core_automation.product_generic_modelling_temp<mod_table_suffix> B on A.company_id=B.company_id)C where attribute_name='email' and len(attribute_value) = len(replace(attribute_value,domain_name,'')) group by company_id)B on A.company_id=B.company_id where other_email is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'other_email', 'Completed',11

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'product_and_services', 'Started',12
update A set product_presence=B.c from core_automation.product_generic_modelling_temp<mod_table_suffix> A join( select company_id, count(company_id) as c from core_automation.company_attributes<table_suffix> where attribute_name = 'product_and_services' group by company_id having count(company_id) < 31)B on A.company_id=B.company_id and product_presence is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'product_and_services', 'Completed',12

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'script_blocked', 'Started',13
update X set script_blocked= 1 from core_automation.product_generic_modelling_temp<mod_table_suffix> X  where exists (select distinct Y.company_id from  (select distinct a.company_id from core_automation.company_attributes<table_suffix> a join core_automation.company_attributes<table_suffix> b on a.company_id = b.company_id where (a.attribute_name =  'data_collected' and a.attribute_value = 'No') and (b.attribute_name = 'url_status' and b.attribute_value = 'Yes'))Y where X.company_id=Y.company_id ) and script_blocked is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'script_blocked', 'Completed',13

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'seo_description', 'Started',14
update a set seo_description=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> a join core_automation.company_attributes<table_suffix> b on (a.company_id=b.company_id) where attribute_name in ('og:description','meta_description') and seo_description is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'seo_description', 'Completed',14

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'seo_keywords', 'Started',15
update a set seo_keywords=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> a join core_automation.company_attributes<table_suffix> b on (a.company_id=b.company_id) where attribute_name='meta' and seo_keywords is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'seo_keywords', 'Completed',15

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'seo_optimization', 'Started',16
update  a set seo_optimization = 1 from core_automation.product_generic_modelling_temp<mod_table_suffix> a where exists(select 1 from core_automation.company_attributes<table_suffix> b where a.company_id=b.company_id and attribute_name in ('og:description', 'meta_description', 'meta')) and seo_optimization is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'seo_optimization', 'Completed',16

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'mobile_apps', 'Started',17
update a set store_apps=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> a where exists( select 1 from core_automation.company_attributes<table_suffix> b where attribute_name='mobile_apps' and a.company_id=b.company_id) and store_apps is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'mobile_apps', 'Completed',17

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'total_email', 'Started',18
update A set total_email=c from core_automation.product_generic_modelling_temp<mod_table_suffix> A join( select company_id, count(*) as c from core_automation.company_attributes<table_suffix> where attribute_name = 'email' group by company_id )B on A.company_id=B.company_id where total_email is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'total_email', 'Completed',18

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'website_development_outsource', 'Started',19
update A set website_development_outsource = 1 from core_automation.product_generic_modelling_temp<mod_table_suffix> A join core_automation.company_attributes<table_suffix> B on A.company_id=B.company_id where attribute_name='Website Outsource' and website_development_outsource is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'website_development_outsource', 'Completed',19

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'customer_support', 'Started',20
update A set customer_support=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> A join core_automation.company_attributes<table_suffix> B on A.company_id = B.company_id where B.attribute_name= 'customer_support' and B.attribute_value='Yes' and customer_support is null
update core_automation.product_generic_modelling_temp<mod_table_suffix> set customer_support=1 where live_chat = 1 and customer_support is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'customer_support', 'Completed',20

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'manufacturing_goods', 'Started',21
update A set manufacturing_goods=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> A where (product_presence > 0 and industry_type like '%manufacturing%') and manufacturing_goods is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'manufacturing_goods', 'Completed',21

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'international_presence', 'Started',22
update A set international_presence=cnt from core_automation.product_generic_modelling_temp<mod_table_suffix> A join( select company_id,count(distinct country) as cnt from core_automation.company_location_details<table_suffix> group by company_id having count(distinct country)>1 )B on A.company_id=B.company_id where international_presence is null   
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'international_presence', 'Completed',22

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'multiple_locations', 'Started',23
update A set multiple_locations=B.c from core_automation.product_generic_modelling_temp<mod_table_suffix> A join(select company_id, count(*) as c from core_automation.company_location_details<table_suffix> group by company_id)B on A.company_id=B.company_id where multiple_locations is null or multiple_locations=0
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'multiple_locations', 'Completed',23

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'data_backup', 'Started',25
update a set data_backup = 1 from core_automation.product_generic_modelling_temp<mod_table_suffix> a where exists (select 1 from core_automation.industry_sql_mapping b where data_backup = 1 and a.industry_type=b.industry) and data_backup is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'data_backup', 'Completed',25

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'enormous_transactions', 'Started',26
update a set enormous_transactions = 1  from  core_automation.product_generic_modelling_temp<mod_table_suffix> a where exists (select 1 from core_automation.industry_sql_mapping b where enormous_transactions = 1 and a.industry_type=b.industry ) and enormous_transactions is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'enormous_transactions', 'Completed',26

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'sensitive_data', 'Started',27
update a set sensitive_data = 1  from  core_automation.product_generic_modelling_temp<mod_table_suffix> a where exists (select 1 from core_automation.industry_sql_mapping b where sensitive_data = 1 and a.industry_type=b.industry ) and sensitive_data is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'sensitive_data', 'Completed',27

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'tracking_purpose', 'Started',28
update a set tracking_purpose = 1 from core_automation.product_generic_modelling_temp<mod_table_suffix> a where exists (select 1 from core_automation.industry_sql_mapping b where tracking_purpose = 1 and a.industry_type=b.industry ) and tracking_purpose is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'tracking_purpose', 'Completed',28

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'blog_flag', 'Started',29
update A set blog_flag=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> A join (select distinct company_id from core_automation.company_reference_links<table_suffix> where link_type='Blog')B on A.company_id=B.company_id where A.blog_flag is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'blog_flag', 'Completed',29

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'cust_support_flag', 'Started',30
update A set cust_support_flag=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> A join (select distinct company_id from core_automation.company_reference_links<table_suffix> where link_type='Call/Support' )B on A.company_id=B.company_id where A.cust_support_flag is null and cust_support_flag is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'cust_support_flag', 'Completed',30

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'presentation_flag', 'Started',31
update  a set presentation_flag=1 from  core_automation.product_generic_modelling_temp<mod_table_suffix> a where exists (select 1 from core_automation.company_reference_links<table_suffix>  b where link_type  IN ('Reports', 'Presentations') and a.company_id=b.company_id ) and presentation_flag is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'presentation_flag', 'Completed',31

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'omnichannel_presence', 'Started',32
update  a set omnichannel_presence = 1 from core_automation.product_generic_modelling_temp<mod_table_suffix> a  where exists (select X.company_id from ((select distinct company_id from core_automation.company_reference_links<table_suffix>  where link_type = 'Mobile App' union select distinct company_id from core_automation.company_attributes<table_suffix>  where attribute_name='store_locator_status' and attribute_value='Yes'  union select company_id from core_automation.product_generic_modelling_temp<mod_table_suffix>  where store_apps=1 union select distinct company_id from core_automation.company_info<table_suffix>   where (facebook_link is not null or twitter_link is not null or linkedin_link is not null or youtube_link is not null) ) )X where X.company_id = a.company_id ) and omnichannel_presence is null 
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'omnichannel_presence', 'Completed',32

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'employee_count', 'Started',74
update A set employee_count=B.attribute_value from core_automation.product_generic_modelling_temp<mod_table_suffix> A join( select company_id,attribute_value from core_automation.company_attributes<table_suffix> where attribute_name = 'employee_count' )B on A.company_id=B.company_id where employee_count is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'employee_count', 'Completed',74

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'founded_year', 'Started',75
update A set founded_year=B.attribute_value from core_automation.product_generic_modelling_temp<mod_table_suffix> A join( select company_id,attribute_value from core_automation.company_attributes<table_suffix> where attribute_name = 'founded_year' )B on A.company_id=B.company_id where founded_year is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'founded_year', 'Completed',75

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'active_blog_pr', 'Started',76
UPDATE a set active_blog_pr=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> a  where exists( select X.company_id from (  select distinct company_id from core_automation.post_feed_PR<table_suffix>  union  select distinct company_id from core_automation.company_reference_links<table_suffix> where link_type='Blog'  )X  where a.company_id=X.company_id) and active_blog_pr is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'active_blog_pr', 'Completed',76

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'social_links', 'Started',83
update A set facebook_link=B.facebook_link, twitter_link=B.twitter_link, linkedin_link=B.linkedin_link from core_automation.product_generic_modelling_temp<mod_table_suffix> A join core_automation.company_info<table_suffix> B on A.company_id=B.company_id
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'social_links', 'Completed',83

update  a  set Youtube_link=1 from core_automation.product_generic_modelling a  where exists ( select 1 from core_automation.company_info b where Youtube_link is not null and a.company_id=b.company_id)

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'cross_channel_presence', 'Started',119
update a set cross_channel_presence=1 from core_automation.product_specific_modelling_temp<mod_table_suffix> a where exists (select 1 from core_automation.company_attributes<table_suffix> b where (attribute_name in ('match_crosschannel_found','match_payment_found') and attribute_value='True') and a.company_id=b.company_id) and cross_channel_presence is null --942
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'cross_channel_presence', 'Completed',119

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'ecommerce_presence', 'Started',127
update  a set ecommerce_presence=1 from core_automation.product_specific_modelling_temp<mod_table_suffix> a where exists ( select 1 from core_automation.company_attributes<table_suffix> b where (attribute_name in ('discounts','gift_cards','store_locator_status','match_payment_found') and attribute_value in ('Yes','True'))and a.company_id=b.company_id) and ecommerce_presence is null--747
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'ecommerce_presence', 'Completed',127

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'social_links', 'Started',128
update A set facebook_link=B.facebook_link, twitter_link=B.twitter_link, linkedin_link=B.linkedin_link ,youtube_link=B.youtube_link from core_automation.product_specific_modelling_temp<mod_table_suffix> A join core_automation.company_info<table_suffix> B on A.company_id=B.company_id
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'social_links', 'Completed',128

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'field_service', 'Started',129
update a set field_service=1  from core_automation.product_specific_modelling_temp<mod_table_suffix> a  where exists( select 1 from core_automation.company_attributes<table_suffix> b where attribute_name = 'phone' and a.company_id=b.company_id) and field_service is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'field_service', 'Completed',129

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'financials', 'Started',130
update a set financials=1 from core_automation.product_specific_modelling_temp<mod_table_suffix> a  where exists( select X.company_id from (select distinct company_id from core_automation.product_specific_modelling_temp<mod_table_suffix> where (industry_type like '%financial%' or industry_type like '%finance%') union select distinct company_id from core_automation.company_location_details<table_suffix> group by company_id having count(*) > 1 )X where a.company_id=X.company_id) and financials is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'financials', 'Completed',130

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'geo_redundant', 'Started',131
update  a set geo_redundant=1  from core_automation.product_specific_modelling_temp<mod_table_suffix> a where exists (select 1 from core_automation.industry_sql_mapping b where geo_redundant = 1 and a.industry_type=b.industry) and geo_redundant is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'geo_redundant', 'Completed',131

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'gift_cards', 'Started',132
update  a set gift_cards=1 from core_automation.product_specific_modelling_temp<mod_table_suffix> a where exists( select 1 from core_automation.company_attributes<table_suffix> b where (attribute_name in ('gift_cards','discounts') and attribute_value='Yes') and a.company_id=b.company_id) and gift_cards is null--150
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'gift_cards', 'Completed',132

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'in_memory_analytics', 'Started',135
update a set in_memory_analytics=1  from core_automation.product_specific_modelling_temp<mod_table_suffix> a  where (exists (select 1 from core_automation.industry_sql_mapping b where in_memory_analytics = 1 and  a.industry_type=b.industry) or industry_type in('Banking','Financial Services','Hardware & Software','Media')) and in_memory_analytics is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'in_memory_analytics', 'Completed',135

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'inventory', 'Started',137
update  a set inventory=1 from core_automation.product_specific_modelling_temp<mod_table_suffix> a where exists(select 1 from core_automation.product_specific_modelling_temp<mod_table_suffix> b where (industry_type in ('Machinery','Manufacturer','Manufacturing') or industry_type like '%manufactur%') and a.company_id=b.company_id) and inventory is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'inventory', 'Completed',137

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'loyalty_programs', 'Started',139
update a set loyalty_programs=1  from core_automation.product_specific_modelling_temp<mod_table_suffix> a where exists(select 1 from core_automation.company_attributes<table_suffix> b where (attribute_name='discounts' and attribute_value='Yes') and a.company_id=b.company_id) and loyalty_programs is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'loyalty_programs', 'Completed',139

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'mobile_responsiveness', 'Started',140
update  a set mobile_responsiveness=1  from core_automation.product_specific_modelling_temp<mod_table_suffix> a where exists (select 1 from core_automation.company_attributes<table_suffix> b where (attribute_name='mobile_responsiveness' and attribute_value='Yes') and a.company_id=b.company_id) and mobile_responsiveness is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'mobile_responsiveness', 'Completed',140

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'regulated_business', 'Started',148
update core_automation.product_specific_modelling_temp<mod_table_suffix> set regulated_business=1 where industry_type in ('Hospital & Health Care','Insurance','Financial Services','Health, Wellness and Fitness','Banking','Aerospace & Defence', 'Communication','Food & Beverages','Law Practice','Legal Services','Telecomm','Travel & Leisure') and regulated_business is null
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'regulated_business', 'Completed',148

INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'it_staff', 'Started',80
update tech set it_staff=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> tech join( SELECT distinct company_id FROM core_automation.company_attributes<table_suffix> attr where attr.attribute_name='url_status' AND attr.attribute_value IN ('Forbitten','ScriptPage','Forbidden','HasDataAndNoScript','HasDataAndScript','Not Acceptable','HasDataWithMoreScriptt','Unauthorized'))sig on tech.company_id=sig.company_id and it_staff is null--704
INSERT INTO core_automation.modelling_signals_stats(attribute_name, task_status, signal_id) select 'it_staff', 'Completed',80

update  a  set facebook_presence=1  from core_automation.product_generic_modelling_temp<mod_table_suffix> a  where exists ( select 1 from core_automation.post_feed_social_media<table_suffix> b where source='Facebook' and a.company_id=b.company_id)

update  a  set twitter_presence=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> a  where exists ( select 1 from core_automation.post_feed_social_media<table_suffix> b where source='Twitter' and a.company_id=b.company_id)

update  a  set linked_in_presence=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> a  where exists ( select 1 from core_automation.company_info<table_suffix> b where linkedin_link is not null and a.company_id=b.company_id)

update a set phone_number=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> a  where exists (select 1 from core_automation.company_attributes<table_suffix> b where attribute_name = 'phone' and attribute_value is not null and a.company_id = b.company_id)

update a set email=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> a  where exists (select 1 from core_automation.company_attributes<table_suffix> b where attribute_name = 'email' and attribute_value is not null and a.company_id = b.company_id);

update a set tollfree=1 from core_automation.product_generic_modelling_temp<mod_table_suffix> a  where exists (select * from (select distinct company_id, [dbo].[RemoveSpecialCharacters](attribute_value) as altred_number from core_automation.company_attributes<table_suffix> b where attribute_name = 'phone' and attribute_value is not null and a.company_id = b.company_id ) inn where a.Company_id = inn.company_id and  altred_number like '1800%' or altred_number like '1877%' or altred_number like '1866%' or altred_number like '1855%' or altred_number like '1844%' or altred_number like '1833%' or altred_number like '1822%' or altred_number like '1880%' or altred_number like '1887%' or altred_number like '1889%');