"""
    Content Type: Utilities
    Description: This python file has common variables used across the application
    Version    : v2.10
    History    :
                v1.0 - 01/01/2015 - Initial version
                v1.1 - 12/21/2015 - get_website_parent added
                v1.2 - 05/03/2016 - function to return the country name
                v1.3 - 07/12/2016 - function to class conversion. get_domain_details is moved from DomainSupport.py(to be removed) to WebsiteCodesSupport
                v1.4 - 07/13/2016 - added additional function around website to see country code/language code in url.
                v1.5 - 07/16/2016 - Called the class in the function. Ultimately the functions from this modules need to removed and only Class to be used.
                v2.0 - 07/20/2016 - Combined version check-in to common repository.
                v2.1 - 07/25/2016 - Added function process_ticker_info to fetch ticker details from url.
                v2.2 - 08/16/2016 - Country name is normalized ex - Netherlands (Holandsko) vs Netherlands
                v2.3 - 09/01/2016 - try and except for ticker part. Added new suffixes
                v2.4 - 09/01/2016 - Added function normalize_website_url to normalize website url before processing.
                v2.5 - 10/14/2016 - Changes to handle ? properly - having links in ?
                v2.6 - 11/25/2016 - return the website domain in lower case Fb.com vs fb.com
                v2.7 - 02/10/2017 - Use url in lowercase for all calculation. changed in set_url() function.
                v2.8 - 04/10/2017 - Fixes for special symbols in domain and incorrect domain classification (http://N/a)
                v2.9 - 05/10/2017 - Port number logic is handled in process_domain_name
                v2.10 - 05/12/2017 - ignore_errors is set to True. ignore_errors = False to halt the process on incorrect url which has high likeliwood when we run in batch
    Procedure to use: Import this config file into all python scripts where country code for url is required
    Open Issues: None.
    Pending :    For country specific websites parsing
                   - http://www.nielsen.com/au/en/contact-us.html-completed
                   reduce the number of variables;group them
                   http://www.adobe.com/ - uses en_us vs en-us(language_country_code_map)
                   https://eservices.steveco.fi:8090/kct/ShowLogin ,'http://shop.lululemon.com:80'
                   Valid double :// scenario normalize_website_url:	The url does not have proper place for ://. will not process the url further. Url Passed:http://fusion.google.com/add?feedurl=http://blog.ignify.com/feed/
                   Handling IP address: http://185.15.169.148/web_asi/
                    http://www.suny.edu/howmuch/netpricecalculator.xhtml?embed=n&headerUrl=http://www.oldwestbury.edu/images/index/header_logo.jpg&bgColor=006000&id=13
"""
from Utilities import *
website_suffix_code_list=['com','net','org','edu','biz','gov','mil','info','name','me','tv','mobi'
    ,'ad','ae','af','ag','ai','al','am','an','ao','aq','ar','arpa','as','at','au','aw','az'
    ,'ba','bb','bd','be','bf','bg','bh','bi','bj','bm','bn','bo','br','bs','bt','bv','bw','by','bz'
    ,'ca','cc','cf','cg','ch','ci','ck','cl','cm','cn','co','cr','cs','cu','cv','cx','cy','cz'
    ,'de','dj','dk','dm','do','dz','ec','ee','eg','eh','er','es','et','fi','fj','fk','fm','fo','fr','fx'
    ,'ga','gb','gd','ge','gf','gh','gi','gl','gm','gn','gp','gq','gr','gs','gt','gu','gw','gy','hk','hm','hn','hr','ht','hu'
    ,'id','ie','il','in','int','io','iq','ir','is','it','jm','jo','jp','ke','kg','kh','ki','km','kn','kp','kr','kw','ky','kz'
    ,'la','lb','lc','li','lk','lr','ls','lt','lu','lv','ly'
    ,'ma','mc','md','mg','mh','mk','ml','mm','mn','mo','mp','mq','mr','ms','mt','mu','mv','mw','mx','my','mz'
    ,'na','nato','nc','ne','nf','ng','ni','nl','no','np','nr','nt','nu','nz','om','pa','pe','pf','pg','ph','pk','pl','pm','pn','pr','pt','pw','py'
    ,'qa','re','ro','ru','rw','sa','sb','sc','sd','se','sg','sh','si','sj','sk','sl','sm','sn','so','sr','st','su','sv','sy','sz'
    ,'tc','td','tf','tg','th','tj','tk','tm','tn','to','tp','tr','tt','tw','tz','ua','ug','uk','um','us','uy','uz'
    ,'va','vc','ve','vg','vi','vn','vu','wf','ws','ye','yt','yu','za','zm','zr','zw']
website_suffix_code_map={
'xxx':'Pornographic sites'
,'porn':'Pornographic sites'
,'aero':'Members of the air-transport industry'
,'cat':'Catalan linguistic and cultural community'
,'coop':'Cooperative associations'
,'jobs':'Human resource managers'
,'museum':'Museums'
,'post':'Postal services'
,'tel':'For businesses and individuals to publish contact data'
,'travel':'Travel agents, airlines, hoteliers, tourism bureaus, etc.'
,'com':'Commercial'
,'net':'Network'
,'org':'Organization'
,'edu':'Educational'
,'biz':'Business'
,'gov':'Government'
,'mil':'Military'
,'info':'Information Source'
,'name':'Personal Name'
,'me':'Personal Websites'
,'tv':'Television Station'
,'mobi':'Designed for Mobile Phones'
#The following are country codes
,'ad':'Andorra'
,'ae':'United Arab Emirates'
,'af':'Afghanistan'
,'ag':'Antigua and Barbuda'
,'ai':'Anguilla'
,'al':'Albania'
,'am':'Armenia'
,'an':'Netherlands Antilles'
,'ao':'Angola'
,'aq':'Antarctica'
,'ar':'Argentina'
,'arpa':'Old style Arpanet'
,'as':'American Samoa'
,'at':'Austria (Rakousko)'
,'au':'Australia'
,'aw':'Aruba'
,'az':'Azerbaijan'
,'ba':'Bosnia and Herzegovina'
,'bb':'Barbados'
,'bd':'Bangladesh'
,'be':'Belgium'
,'bf':'Burkina Faso'
,'bg':'Bulgaria (Bulharsko)'
,'bh':'Bahrain'
,'bi':'Burundi'
,'bj':'Benin'
,'bm':'Bermuda'
,'bn':'Brunei Darussalam'
,'bo':'Bolivia'
,'br':'Brazil'
,'bs':'Bahamas'
,'bt':'Bhutan'
,'bv':'Bouvet Island'
,'bw':'Botswana'
,'by':'Belarus'
,'bz':'Belize'
,'ca':'Canada'
,'cb':'Caribbean'#added after initial round
,'cc':'Cocos (Keeling) Islands'
,'cf':'Central African Republic'
,'cg':'Congo'
,'ch':'Switzerland'
,'ci':'Cote D\'Ivoire (Ivory Coast)'
,'ck':'Cook Islands'
,'cl':'Chile'
,'cm':'Cameroon'
,'cn':'China'
,'co':'Colombia'
,'cr':'Costa Rica'
,'cs':'Czechoslovakia (former)'
,'cu':'Cuba'
,'cv':'Cape Verde'
,'cx':'Christmas Island'
,'cy':'Cyprus'
,'cz':'Czech Republic'
,'de':'Germany'
,'dj':'Djibouti'
,'dk':'Denmark'
,'dm':'Dominica'
,'do':'Dominican Republic'
,'dz':'Algeria'
,'ec':'Ecuador'
,'ee':'Estonia'
,'eg':'Egypt'
,'eh':'Western Sahara'
,'er':'Eritrea'
,'es':'Spain'
,'et':'Ethiopia'
,'fi':'Finland'
,'fj':'Fiji'
,'fk':'Falkland Islands (Malvinas)'
,'fm':'Micronesia'
,'fo':'Faroe Islands'
,'fr':'France (Francie)'
,'fx':'France, Metropolitan'
,'ga':'Gabon'
,'gb':'Great Britain (UK)'
,'gd':'Grenada'
,'ge':'Georgia (Gruzie)'
,'gf':'French Guiana'
,'gh':'Ghana'
,'gi':'Gibraltar'
,'gl':'Greenland (Island)'
,'gm':'Gambia'
,'gn':'Guinea'
,'gp':'Guadeloupe'
,'gq':'Equatorial Guinea'
,'gr':'Greece'
,'gs':'S. Georgia and S. Sandwich Isls.'
,'gt':'Guatemala'
,'gu':'Guam'
,'gw':'Guinea-Bissau'
,'gy':'Guyana'
,'hk':'Hong Kong'
,'hm':'Heard and McDonald Islands'
,'hn':'Honduras'
,'hr':'Croatia (Hrvatska) (Chorvatsko)'
,'ht':'Haiti'
,'hu':'Hungary'
,'id':'Indonesia'
,'ie':'Ireland (Irsko)'
,'il':'Israel'
,'in':'India'
,'int':'International'
,'io':'British Indian Ocean Territory'
,'iq':'Iraq'
,'ir':'Iran'
,'is':'Iceland (Island)'
,'it':'Italy'
,'jm':'Jamaica'
,'jo':'Jordan'
,'jp':'Japan'
,'ke':'Kenya'
,'kg':'Kyrgyzstan'
,'kh':'Cambodia'
,'ki':'Kiribati'
,'km':'Comoros'
,'kn':'Saint Kitts and Nevis'
,'kp':'Korea (North)'
,'kr':'Korea (South)'
,'kw':'Kuwait'
,'ky':'Cayman Islands'
,'kz':'Kazakhstan'
,'la':'Laos'
,'lb':'Lebanon'
,'lc':'Saint Lucia'
,'li':'Liechtenstein'
,'lk':'Sri Lanka'
,'lr':'Liberia'
,'ls':'Lesotho'
,'lt':'Lithuania'
,'lu':'Luxembourg'
,'lv':'Latvia(Litva)'
,'ly':'Libya'
,'ma':'Morocco'
,'mc':'Monaco'
,'md':'Moldova'
,'mg':'Madagascar'
,'mh':'Marshall Islands'
,'mk':'Macedonia'
,'ml':'Mali'
,'mm':'Myanmar'
,'mn':'Mongolia'
,'mo':'Macau'
,'mp':'Northern Mariana Islands'
,'mq':'Martinique'
,'mr':'Mauritania'
,'ms':'Montserrat'
,'mt':'Malta'
,'mu':'Mauritius'
,'mv':'Maldives'
,'mw':'Malawi'
,'mx':'Mexico'
,'my':'Malaysia'
,'mz':'Mozambique'
,'na':'Namibia'
,'nato':'Nato field'
,'nc':'New Caledonia'
,'ne':'Niger'
,'nf':'Norfolk Island'
,'ng':'Nigeria'
,'ni':'Nicaragua'
,'nl':'Netherlands'
,'no':'Norway'
,'np':'Nepal'
,'nr':'Nauru'
,'nt':'Neutral Zone'
,'nu':'Niue'
,'nz':'New Zealand (Aotearoa)'
,'om':'Oman'
,'pa':'Panama'
,'pe':'Peru'
,'pf':'French Polynesia'
,'pg':'Papua New Guinea'
,'ph':'Philippines'
,'pk':'Pakistan'
,'pl':'Poland (Polsko)'
,'pm':'St. Pierre and Miquelon'
,'pn':'Pitcairn'
,'pr':'Puerto Rico'
,'pt':'Portugal'
,'pw':'Palau'
,'py':'Paraguay'
,'qa':'Qatar'
,'re':'Reunion'
,'ro':'Romania (Rumunsko)'
,'ru':'Russian Federation (Rusko)'
,'rw':'Rwanda'
,'sa':'Saudi Arabia'
,'sb':'Solomon Islands'
,'sc':'Seychelles'
,'sd':'Sudan'
,'se':'Sweden'
,'sg':'Singapore'
,'sh':'St. Helena'
,'si':'Slovenia (Slovinsko)'
,'sj':'Svalbard and Jan Mayen Islands'
,'sk':'Slovak Republic (Slovensko)'
,'sl':'Sierra Leone'
,'sm':'San Marino'
,'sn':'Senegal'
,'so':'Somalia'
,'sp':'Serbia and Montenegro'
,'sr':'Suriname'
,'st':'Sao Tome and Principe'
,'su':'USSR (former) (SSSR)'
,'sv':'El Salvador'
,'sy':'Syria'
,'sz':'Swaziland'
,'tc':'Turks and Caicos Islands'
,'td':'Chad'
,'tf':'French Southern Territories'
,'tg':'Togo'
,'th':'Thailand'
,'tj':'Tajikistan'
,'tk':'Tokelau'
,'tm':'Turkmenistan'
,'tn':'Tunisia'
,'to':'Tonga'
,'tp':'East Timor'
,'tr':'Turkey (Turecko)'
,'tt':'Trinidad and Tobago'
#,'tv':'Tuvalu'
,'tw':'Taiwan'
,'tz':'Tanzania'
,'ua':'Ukraine'
,'ug':'Uganda'
,'uk':'United Kingdom'
,'um':'US Minor Outlying Islands'
,'us':'United States'
,'uy':'Uruguay'
,'uz':'Uzbekistan'
,'va':'Vatican City State (Holy See)'
,'vc':'Saint Vincent and the Grenadines'
,'ve':'Venezuela'
,'vg':'Virgin Islands (British)'
,'vi':'Virgin Islands (U.S.)'
,'vn':'Viet Nam'
,'vu':'Vanuatu'
,'wf':'Wallis and Futuna Islands'
,'ws':'Samoa'
,'ye':'Yemen'
,'yt':'Mayotte'
,'yu':'Yugoslavia'
,'za':'South Africa'
,'zm':'Zambia'
,'zr':'Zaire'
,'zw':'Zimbabwe'
}
language_country_code_map={
'af-za':{'language':'Afrikaans','country':'South Africa'}
,'ar-ae':{'language':'Arabic','country':'U.A.E.'}
,'ar-bh':{'language':'Arabic','country':'Bahrain'}
,'ar-dz':{'language':'Arabic','country':'Algeria'}
,'ar-eg':{'language':'Arabic','country':'Egypt'}
,'ar-iq':{'language':'Arabic','country':'Iraq'}
,'ar-jo':{'language':'Arabic','country':'Jordan'}
,'ar-kw':{'language':'Arabic','country':'Kuwait'}
,'ar-lb':{'language':'Arabic','country':'Lebanon'}
,'ar-ly':{'language':'Arabic','country':'Libya'}
,'ar-ma':{'language':'Arabic','country':'Morocco'}
,'ar-om':{'language':'Arabic','country':'Oman'}
,'ar-qa':{'language':'Arabic','country':'Qatar'}
,'ar-sa':{'language':'Arabic','country':'Saudi Arabia'}
,'ar-sy':{'language':'Arabic','country':'Syria'}
,'ar-tn':{'language':'Arabic','country':'Tunisia'}
,'ar-ye':{'language':'Arabic','country':'Yemen'}
,'az-az':{'language':'Azeri','country':'Azerbaijan'}
,'be-by':{'language':'Belarusian','country':'Belarus'}
,'bg-bg':{'language':'Bulgarian','country':'Bulgaria'}
,'bs-ba':{'language':'Bosnian','country':'Bosnia and Herzegovina'}
,'ca-es':{'language':'Catalan','country':'Spain'}
,'cs-cz':{'language':'Czech','country':'Czech Republic'}
,'cy-gb':{'language':'Welsh','country':'United Kingdom'}
,'da-dk':{'language':'Danish','country':'Denmark'}
,'de-at':{'language':'German','country':'Austria'}
,'de-ch':{'language':'German','country':'Switzerland'}
,'de-de':{'language':'German','country':'Germany'}
,'de-li':{'language':'German','country':'Liechtenstein'}
,'de-lu':{'language':'German','country':'Luxembourg'}
,'dv-mv':{'language':'Divehi','country':'Maldives'}
,'el-gr':{'language':'Greek','country':'Greece'}
,'en-au':{'language':'English','country':'Australia'}
,'en-bz':{'language':'English','country':'Belize'}
,'en-ca':{'language':'English','country':'Canada'}
,'en-cb':{'language':'English','country':'Caribbean'}
,'en-gb':{'language':'English','country':'United Kingdom'}
,'en-ie':{'language':'English','country':'Ireland'}
,'en-jm':{'language':'English','country':'Jamaica'}
,'en-nz':{'language':'English','country':'New Zealand'}
,'en-ph':{'language':'English','country':'Republic of the Philippines'}
,'en-tt':{'language':'English','country':'Trinidad and Tobago'}
,'en-us':{'language':'English','country':'United States'}
,'en-za':{'language':'English','country':'South Africa'}
,'en-zw':{'language':'English','country':'Zimbabwe'}
,'es-ar':{'language':'Spanish','country':'Argentina'}
,'es-bo':{'language':'Spanish','country':'Bolivia'}
,'es-cl':{'language':'Spanish','country':'Chile'}
,'es-co':{'language':'Spanish','country':'Colombia'}
,'es-cr':{'language':'Spanish','country':'Costa Rica'}
,'es-do':{'language':'Spanish','country':'Dominican Republic'}
,'es-ec':{'language':'Spanish','country':'Ecuador'}
,'es-es':{'language':'Spanish','country':'Spain'}
,'es-gt':{'language':'Spanish','country':'Guatemala'}
,'es-hn':{'language':'Spanish','country':'Honduras'}
,'es-mx':{'language':'Spanish','country':'Mexico'}
,'es-ni':{'language':'Spanish','country':'Nicaragua'}
,'es-pa':{'language':'Spanish','country':'Panama'}
,'es-pe':{'language':'Spanish','country':'Peru'}
,'es-pr':{'language':'Spanish','country':'Puerto Rico'}
,'es-py':{'language':'Spanish','country':'Paraguay'}
,'es-sv':{'language':'Spanish','country':'El Salvador'}
,'es-uy':{'language':'Spanish','country':'Uruguay'}
,'es-ve':{'language':'Spanish','country':'Venezuela'}
,'et-ee':{'language':'Estonian','country':'Estonia'}
,'eu-es':{'language':'Basque','country':'Spain'}
,'fa-ir':{'language':'Farsi','country':'Iran'}
,'fi-fi':{'language':'Finnish','country':'Finland'}
,'fo-fo':{'language':'Faroese','country':'Faroe Islands'}
,'fr-be':{'language':'French','country':'Belgium'}
,'fr-ca':{'language':'French','country':'Canada'}
,'fr-ch':{'language':'French','country':'Switzerland'}
,'fr-fr':{'language':'French','country':'France'}
,'fr-lu':{'language':'French','country':'Luxembourg'}
,'fr-mc':{'language':'French','country':'Principality of Monaco'}
,'gl-es':{'language':'Galician','country':'Spain'}
,'gu-in':{'language':'Gujarati','country':'India'}
,'he-il':{'language':'Hebrew','country':'Israel'}
,'hi-in':{'language':'Hindi','country':'India'}
,'hr-ba':{'language':'Croatian','country':'Bosnia and Herzegovina'}
,'hr-hr':{'language':'Croatian','country':'Croatia'}
,'hu-hu':{'language':'Hungarian','country':'Hungary'}
,'hy-am':{'language':'Armenian','country':'Armenia'}
,'id-id':{'language':'Indonesian','country':'Indonesia'}
,'is-is':{'language':'Icelandic','country':'Iceland'}
,'it-ch':{'language':'Italian','country':'Switzerland'}
,'it-it':{'language':'Italian','country':'Italy'}
,'ja-jp':{'language':'Japanese','country':'Japan'}
,'ka-ge':{'language':'Georgian','country':'Georgia'}
,'kk-kz':{'language':'Kazakh','country':'Kazakhstan'}
,'kn-in':{'language':'Kannada','country':'India'}
,'ko-kr':{'language':'Korean','country':'Korea'}
,'kok-in':{'language':'Konkani','country':'India'}
,'ky-kg':{'language':'Kyrgyz','country':'Kyrgyzstan'}
,'lt-lt':{'language':'Lithuanian','country':'Lithuania'}
,'lv-lv':{'language':'Latvian','country':'Latvia'}
,'mi-nz':{'language':'Maori','country':'New Zealand'}
,'mk-mk':{'language':'FYRO','country':'Macedonian'}
,'mn-mn':{'language':'Mongolian','country':'Mongolia'}
,'mr-in':{'language':'Marathi','country':'India'}
,'ms-bn':{'language':'Malay','country':'Brunei Darussalam'}
,'ms-my':{'language':'Malay','country':'Malaysia'}
,'mt-mt':{'language':'Maltese','country':'Malta'}
,'nb-no':{'language':'Norwegian','country':'Norway'}
,'nl-be':{'language':'Dutch','country':'Belgium'}
,'nl-nl':{'language':'Dutch','country':'Netherlands'}
,'nn-no':{'language':'Norwegian','country':'Norway'}
,'ns-za':{'language':'Northern','country':'South Africa'}
,'pa-in':{'language':'Punjabi','country':'India'}
,'pl-pl':{'language':'Polish','country':'Poland'}
,'ps-ar':{'language':'Pashto','country':'Afghanistan'}
,'pt-br':{'language':'Portuguese','country':'Brazil'}
,'pt-pt':{'language':'Portuguese','country':'Portugal'}
,'qu-bo':{'language':'Quechua','country':'Bolivia'}
,'qu-ec':{'language':'Quechua','country':'Ecuador'}
,'qu-pe':{'language':'Quechua','country':'Peru'}
,'ro-ro':{'language':'Romanian','country':'Romania'}
,'ru-ru':{'language':'Russian','country':'Russia'}
,'sa-in':{'language':'Sanskrit','country':'India'}
,'se-fi':{'language':'Sami','country':'Finland'}
,'se-no':{'language':'Sami','country':'Norway'}
,'se-se':{'language':'Sami','country':'Sweden'}
,'sk-sk':{'language':'Slovak','country':'Slovakia'}
,'sl-si':{'language':'Slovenian','country':'Slovenia'}
,'sq-al':{'language':'Albanian','country':'Albania'}
,'sr-ba':{'language':'Serbian','country':'Bosnia and Herzegovina'}
,'sr-sp':{'language':'Serbian','country':'Serbia and Montenegro'}
,'sv-fi':{'language':'Swedish','country':'Finland'}
,'sv-se':{'language':'Swedish','country':'Sweden'}
,'sw-ke':{'language':'Swahili','country':'Kenya'}
,'syr-sy':{'language':'Syriac','country':'Syria'}
,'ta-in':{'language':'Tamil','country':'India'}
,'te-in':{'language':'Telugu','country':'India'}
,'th-th':{'language':'Thai','country':'Thailand'}
,'tl-ph':{'language':'Tagalog','country':'Philippines'}
,'tn-za':{'language':'Tswana','country':'South Africa'}
,'tr-tr':{'language':'Turkish','country':'Turkey'}
,'tt-ru':{'language':'Tatar','country':'Russia'}
,'uk-ua':{'language':'Ukrainian','country':'Ukraine'}
,'ur-pk':{'language':'Urdu','country':'Pakistan'}
,'uz-uz':{'language':'Uzbek','country':'Uzbekistan'}
,'vi-vn':{'language':'Vietnamese','country':'Vietnam'}
,'xh-za':{'language':'Xhosa','country':'South Africa'}
,'zh-cn':{'language':'Chinese','country':'China'}
,'zh-hk':{'language':'Chinese','country':'Hong Kong'}
,'zh-mo':{'language':'Chinese','country':'Macau'}
,'zh-sg':{'language':'Chinese','country':'Singapore'}
,'zh-tw':{'language':'Chinese','country':'Taiwan'}
,'zu-za':{'language':'Zulu','country':'South Africa'}
}

language_code_for_website={
'af':{'language':'Afrikaans','country':'South Africa'}
,'ar':{'language':'Arabic','country':'Saudi Arabia'}
,'az':{'language':'Azeri','country':'Latin'}
,'be':{'language':'Belarusian','country':'Belarus'}
,'bg':{'language':'Bulgarian','country':'Bulgaria'}
,'bs':{'language':'Bosnian','country':'Bosnia and Herzegovina'}
,'ca':{'language':'Catalan','country':'Spain'}
,'cs':{'language':'Czech','country':'Czech Republic'}
,'cy':{'language':'Welsh','country':'Wales'}
,'da':{'language':'Danish','country':'Denmark'}
,'de':{'language':'German','country':'Germany'}
,'dv':{'language':'Divehi','country':'Maldives'}
,'el':{'language':'Greek','country':'Greece'}
,'en':{'language':'English','country':'United Kingdom'}
,'eo':{'language':'Esperanto','country':'No Country'}
,'es':{'language':'Spanish','country':'Spain'}
,'et':{'language':'Estonian','country':'Estonia'}
,'eu':{'language':'Basque','country':'Spain'}
,'fa':{'language':'Farsi','country':'Iran'}
,'fi':{'language':'Finnish','country':'Finland'}
,'fo':{'language':'Faroese','country':'Faroe Islands'}
,'fr':{'language':'French','country':'France'}
,'gl':{'language':'Galician','country':'Spain'}
,'gu':{'language':'Gujarati','country':'India'}
,'he':{'language':'Hebrew','country':'Israel'}
,'hi':{'language':'Hindi','country':'India'}
,'hr':{'language':'Croatian','country':'Croatia'}
,'hu':{'language':'Hungarian','country':'Hungary'}
,'hy':{'language':'Armenian','country':'Armenia'}
,'id':{'language':'Indonesian','country':'Indonesia'}
,'is':{'language':'Icelandic','country':'Iceland'}
,'it':{'language':'Italian','country':'Italy'}
,'ja':{'language':'Japanese','country':'Japan'}
,'ka':{'language':'Georgian','country':'Georgia'}
,'kk':{'language':'Kazakh','country':'Kazakhstan'}
,'kn':{'language':'Kannada','country':'India'}
,'ko':{'language':'Korean','country':'Korea'}
,'kok':{'language':'Konkani','country':'India'}#has 3 char
,'ky':{'language':'Kyrgyz','country':'Kyrgyzstan'}
,'lt':{'language':'Lithuanian','country':'Lithuania'}
,'lv':{'language':'Latvian','country':'Latvia'}
,'mi':{'language':'Maori','country':'New Zealand'}
,'mk':{'language':'FYRO','country':'Macedonian'}
,'mn':{'language':'Mongolian','country':'Mongolia'}
,'mr':{'language':'Marathi','country':'India'}
,'ms':{'language':'Malay','country':'Malaysia'}
,'mt':{'language':'Maltese','country':'Malta'}
,'nb':{'language':'Norwegian','country':'Norway'}
,'nn':{'language':'Norwegian','country':'Norway'}
,'nl':{'language':'Dutch','country':'Netherlands'}
,'ns':{'language':'Northern','country':'South Africa'}
,'pa':{'language':'Punjabi','country':'India'}
,'pl':{'language':'Polish','country':'Poland'}
,'ps':{'language':'Pashto','country':'Afghanistan'}
,'pt':{'language':'Portuguese','country':'Portugal'}
,'qu':{'language':'Quechua','country':'Bolivia'}
,'ro':{'language':'Romanian','country':'Romania'}
,'ru':{'language':'Russian','country':'Russia'}
,'sa':{'language':'Sanskrit','country':'India'}
,'se':{'language':'Sami','country':'Finland'}
,'sk':{'language':'Slovak','country':'Slovakia'}
,'sl':{'language':'Slovenian','country':'Slovenia'}
,'sq':{'language':'Albanian','country':'Albania'}
,'sr':{'language':'Serbian','country':'Serbia and Montenegro'}
,'sv':{'language':'Swedish','country':'Sweden'}
,'sw':{'language':'Swahili','country':'Kenya'}
,'syr':{'language':'Syriac','country':'Syria'} #has 3 char
,'ta':{'language':'Tamil','country':'India'}
,'te':{'language':'Telugu','country':'India'}
,'th':{'language':'Thai','country':'Thailand'}
,'tl':{'language':'Tagalog','country':'Philippines'}
,'tn':{'language':'Tswana','country':'South Africa'}
,'tr':{'language':'Turkish','country':'Turkey'}
,'tt':{'language':'Tatar','country':'Russia'}
,'ts':{'language':'Tsonga','country':'South Africa'}
,'uk':{'language':'Ukrainian','country':'Ukraine'}
,'ur':{'language':'Urdu','country':'Pakistan'}
,'uz':{'language':'Uzbek','country':'Uzbekistan'}
,'vi':{'language':'Vietnamese','country':'Vietnam'}
,'xh':{'language':'Xhosa','country':'South Africa'}
,'zh':{'language':'Chinese','country':'China'}
,'zu':{'language':'Zulu','country':'South Africa'}
}
country_region_code_map={
'south-america':{'country':'South America','key_country':0}
,'north-america':{'country':'North America','key_country':0}
,'southamerica':{'country':'South America','key_country':0}
,'northamerica':{'country':'North America','key_country':0}
,'europe':{'country':'Europe','key_country':0}
,'africa':{'country':'Africa','key_country':0}
,'asia':{'country':'Asia','key_country':0}

}
country_common_code_map={
'worldwide':{'country':'Worldwide','key_country':0}
,'country':{'country':'Country','key_country':0}
}

country_short_code_map={
'afghanistan':{'country':'Afghanistan','key_country':0}
,'albania':{'country':'Albania','key_country':0}
,'algeria':{'country':'Algeria','key_country':0}
,'americansamoa':{'country':'American Samoa','key_country':0}
,'andorra':{'country':'Andorra','key_country':0}
,'angola':{'country':'Angola','key_country':0}
,'anguilla':{'country':'Anguilla','key_country':0}
,'antarctica':{'country':'Antarctica','key_country':0}
,'antigua':{'country':'Antigua and Barbuda','key_country':0}
,'argentina':{'country':'Argentina','key_country':1}
,'armenia':{'country':'Armenia','key_country':0}
,'aruba':{'country':'Aruba','key_country':0}
,'australia':{'country':'Australia','key_country':1}
,'austria':{'country':'Austria (Rakousko)','key_country':1}
,'azerbaijan':{'country':'Azerbaijan','key_country':0}
,'bahamas':{'country':'Bahamas','key_country':0}
,'bahrain':{'country':'Bahrain','key_country':0}
,'bangladesh':{'country':'Bangladesh','key_country':0}
,'barbados':{'country':'Barbados','key_country':0}
,'belarus':{'country':'Belarus','key_country':0}
,'belgium':{'country':'Belgium','key_country':1}
,'belize':{'country':'Belize','key_country':0}
,'benin':{'country':'Benin','key_country':0}
,'bermuda':{'country':'Bermuda','key_country':0}
,'bhutan':{'country':'Bhutan','key_country':0}
,'bolivia':{'country':'Bolivia','key_country':0}
,'bosnia':{'country':'Bosnia and Herzegovina','key_country':0}
,'botswana':{'country':'Botswana','key_country':0}
,'bouvetisland':{'country':'Bouvet Island','key_country':0}
,'brazil':{'country':'Brazil','key_country':1}
,'britishindianoceanterritory':{'country':'British Indian Ocean Territory','key_country':0}
,'bruneidarussalam':{'country':'Brunei Darussalam','key_country':0}
,'bulgaria':{'country':'Bulgaria (Bulharsko)','key_country':1}
,'burkinafaso':{'country':'Burkina Faso','key_country':0}
,'burundi':{'country':'Burundi','key_country':0}
,'cambodia':{'country':'Cambodia','key_country':1}
,'cameroon':{'country':'Cameroon','key_country':1}
,'canada':{'country':'Canada','key_country':1}
,'capeverde':{'country':'Cape Verde','key_country':0}
,'caymanislands':{'country':'Cayman Islands','key_country':0}
,'centralafricanrepublic':{'country':'Central African Republic','key_country':0}
,'chad':{'country':'Chad','key_country':0}
,'chile':{'country':'Chile','key_country':1}
,'china':{'country':'China','key_country':1}
,'christmasisland':{'country':'Christmas Island','key_country':0}
,'cocosisland':{'country':'Cocos (Keeling) Islands','key_country':0}
,'colombia':{'country':'Colombia','key_country':1}
,'comoros':{'country':'Comoros','key_country':0}
,'congo':{'country':'Congo','key_country':0}
,'cookisland':{'country':'Cook Islands','key_country':0}
,'costarica':{'country':'Costa Rica','key_country':0}
,'ivorycoast':{'country':'Cote D\'Ivoire (Ivory Coast)','key_country':0}
,'croatia':{'country':'Croatia (Hrvatska) (Chorvatsko)','key_country':0}
,'cuba':{'country':'Cuba','key_country':1}
,'cyprus':{'country':'Cyprus','key_country':0}
,'czechrepublic':{'country':'Czech Republic','key_country':0}
,'czechoslovakia':{'country':'Czechoslovakia (former)','key_country':0}
,'denmark':{'country':'Denmark','key_country':1}
,'djibouti':{'country':'Djibouti','key_country':0}
,'dominica':{'country':'Dominica','key_country':0}
,'dominicanrepublic':{'country':'Dominican Republic','key_country':0}
,'easttimor':{'country':'East Timor','key_country':0}
,'ecuador':{'country':'Ecuador','key_country':0}
,'egypt':{'country':'Egypt','key_country':1}
,'elsalvador':{'country':'El Salvador','key_country':0}
,'equatorialguinea':{'country':'Equatorial Guinea','key_country':0}
,'eritrea':{'country':'Eritrea','key_country':0}
,'estonia':{'country':'Estonia','key_country':0}
,'ethiopia':{'country':'Ethiopia','key_country':1}
,'falklandislands':{'country':'Falkland Islands (Malvinas)','key_country':0}
,'faroeislands':{'country':'Faroe Islands','key_country':0}
,'fiji':{'country':'Fiji','key_country':1}
,'finland':{'country':'Finland','key_country':0}
,'france':{'country':'France','key_country':1}
,'frenchguiana':{'country':'French Guiana','key_country':0}
,'frenchpolynesia':{'country':'French Polynesia','key_country':0}
,'frenchsouthernterritories':{'country':'French Southern Territories','key_country':0}
,'gabon':{'country':'Gabon','key_country':0}
,'gambia':{'country':'Gambia','key_country':0}
,'georgia':{'country':'Georgia (Gruzie)','key_country':0}
,'germany':{'country':'Germany','key_country':1}
,'ghana':{'country':'Ghana','key_country':0}
,'gibraltar':{'country':'Gibraltar','key_country':0}
,'uk':{'country':'Great Britain (UK)','key_country':0}
,'greece':{'country':'Greece','key_country':1}
,'greenland':{'country':'Greenland (Island)','key_country':0}
,'grenada':{'country':'Grenada','key_country':0}
,'guadeloupe':{'country':'Guadeloupe','key_country':0}
,'guam':{'country':'Guam','key_country':0}
,'guatemala':{'country':'Guatemala','key_country':0}
,'guinea':{'country':'Guinea','key_country':0}
,'guinea-bissau':{'country':'Guinea-Bissau','key_country':0}
,'guyana':{'country':'Guyana','key_country':0}
,'haiti':{'country':'Haiti','key_country':0}
,'heardisland':{'country':'Heard and McDonald Islands','key_country':0}
,'honduras':{'country':'Honduras','key_country':0}
,'hongkong':{'country':'Hong Kong','key_country':1}
,'hungary':{'country':'Hungary','key_country':0}
,'iceland':{'country':'Iceland (Island)','key_country':0}
,'india':{'country':'India','key_country':1}
,'indonesia':{'country':'Indonesia','key_country':1}
,'international':{'country':'International','key_country':0}
,'iran':{'country':'Iran','key_country':1}
,'iraq':{'country':'Iraq','key_country':1}
,'ireland':{'country':'Ireland','key_country':1}
,'israel':{'country':'Israel','key_country':1}
,'italy':{'country':'Italy','key_country':1}
,'jamaica':{'country':'Jamaica','key_country':1}
,'japan':{'country':'Japan','key_country':1}
,'jordan':{'country':'Jordan','key_country':1}
,'kazakhstan':{'country':'Kazakhstan','key_country':0}
,'kenya':{'country':'Kenya','key_country':0}
,'kiribati':{'country':'Kiribati','key_country':0}
,'northkorea':{'country':'Korea (North)','key_country':1}
,'southkorea':{'country':'Korea (South)','key_country':1}
,'kuwait':{'country':'Kuwait','key_country':1}
,'kyrgyzstan':{'country':'Kyrgyzstan','key_country':0}
,'laos':{'country':'Laos','key_country':0}
,'latvia(litva)':{'country':'Latvia(Litva)','key_country':0}
,'lebanon':{'country':'Lebanon','key_country':0}
,'lesotho':{'country':'Lesotho','key_country':0}
,'liberia':{'country':'Liberia','key_country':0}
,'libya':{'country':'Libya','key_country':0}
,'liechtenstein':{'country':'Liechtenstein','key_country':0}
,'lithuania':{'country':'Lithuania','key_country':0}
,'luxembourg':{'country':'Luxembourg','key_country':0}
,'macau':{'country':'Macau','key_country':0}
,'macedonia':{'country':'Macedonia','key_country':0}
,'madagascar':{'country':'Madagascar','key_country':0}
,'malawi':{'country':'Malawi','key_country':0}
,'malaysia':{'country':'Malaysia','key_country':1}
,'maldives':{'country':'Maldives','key_country':0}
,'mali':{'country':'Mali','key_country':0}
,'malta':{'country':'Malta','key_country':0}
,'marshallislands':{'country':'Marshall Islands','key_country':0}
,'martinique':{'country':'Martinique','key_country':0}
,'mauritania':{'country':'Mauritania','key_country':0}
,'mauritius':{'country':'Mauritius','key_country':0}
,'mayotte':{'country':'Mayotte','key_country':0}
,'mexico':{'country':'Mexico','key_country':1}
,'micronesia':{'country':'Micronesia','key_country':0}
,'moldova':{'country':'Moldova','key_country':0}
,'monaco':{'country':'Monaco','key_country':0}
,'mongolia':{'country':'Mongolia','key_country':0}
,'montserrat':{'country':'Montserrat','key_country':0}
,'morocco':{'country':'Morocco','key_country':0}
,'mozambique':{'country':'Mozambique','key_country':0}
,'myanmar':{'country':'Myanmar','key_country':0}
,'namibia':{'country':'Namibia','key_country':0}
,'natofield':{'country':'Nato field','key_country':0}
,'nauru':{'country':'Nauru','key_country':0}
,'nepal':{'country':'Nepal','key_country':0}
,'netherlands':{'country':'Netherlands','key_country':1}
,'netherlandsantilles':{'country':'Netherlands Antilles','key_country':0}
,'neutralzone':{'country':'Neutral Zone','key_country':0}
,'newcaledonia':{'country':'New Caledonia','key_country':0}
,'newzealand':{'country':'New Zealand (Aotearoa)','key_country':1}
,'nicaragua':{'country':'Nicaragua','key_country':0}
,'niger':{'country':'Niger','key_country':0}
,'nigeria':{'country':'Nigeria','key_country':0}
,'niue':{'country':'Niue','key_country':0}
,'norfolkisland':{'country':'Norfolk Island','key_country':0}
,'northernmarianaislands':{'country':'Northern Mariana Islands','key_country':0}
,'norway':{'country':'Norway','key_country':1}
,'oldstylearpanet':{'country':'Old style Arpanet','key_country':0}
,'oman':{'country':'Oman','key_country':0}
,'pakistan':{'country':'Pakistan','key_country':0}
,'palau':{'country':'Palau','key_country':0}
,'panama':{'country':'Panama','key_country':0}
,'papuanewguinea':{'country':'Papua New Guinea','key_country':0}
,'paraguay':{'country':'Paraguay','key_country':0}
,'peru':{'country':'Peru','key_country':0}
,'philippines':{'country':'Philippines','key_country':0}
,'pitcairn':{'country':'Pitcairn','key_country':0}
,'poland':{'country':'Poland (Polsko)','key_country':0}
,'portugal':{'country':'Portugal','key_country':1}
,'puertorico':{'country':'Puerto Rico','key_country':1}
,'qatar':{'country':'Qatar','key_country':1}
,'reunion':{'country':'Reunion','key_country':0}
,'romania':{'country':'Romania (Rumunsko)','key_country':0}
,'russia':{'country':'Russian Federation (Rusko)','key_country':1}
,'rwanda':{'country':'Rwanda','key_country':0}
,'georgiaisland':{'country':'S. Georgia and S. Sandwich Isls.','key_country':0}
,'saintkittsandnevis':{'country':'Saint Kitts and Nevis','key_country':0}
,'saintlucia':{'country':'Saint Lucia','key_country':0}
,'saintvincentandthegrenadines':{'country':'Saint Vincent and the Grenadines','key_country':0}
,'samoa':{'country':'Samoa','key_country':0}
,'sanmarino':{'country':'San Marino','key_country':0}
,'saotomeandprincipe':{'country':'Sao Tome and Principe','key_country':0}
,'saudiarabia':{'country':'Saudi Arabia','key_country':1}
,'senegal':{'country':'Senegal','key_country':0}
,'seychelles':{'country':'Seychelles','key_country':0}
,'sierraleone':{'country':'Sierra Leone','key_country':0}
,'singapore':{'country':'Singapore','key_country':1}
,'slovakrepublic':{'country':'Slovak Republic (Slovensko)','key_country':0}
,'slovenia':{'country':'Slovenia (Slovinsko)','key_country':0}
,'solomonislands':{'country':'Solomon Islands','key_country':0}
,'somalia':{'country':'Somalia','key_country':0}
,'southafrica':{'country':'South Africa','key_country':1}
,'spain':{'country':'Spain','key_country':1}
,'srilanka':{'country':'Sri Lanka','key_country':0}
,'sthelena':{'country':'St. Helena','key_country':0}
,'stpierreandmiquelon':{'country':'St. Pierre and Miquelon','key_country':0}
,'sudan':{'country':'Sudan','key_country':0}
,'suriname':{'country':'Suriname','key_country':0}
,'svalbardandjanmayenislands':{'country':'Svalbard and Jan Mayen Islands','key_country':0}
,'swaziland':{'country':'Swaziland','key_country':0}
,'sweden':{'country':'Sweden','key_country':1}
,'switzerland':{'country':'Switzerland','key_country':1}
,'syria':{'country':'Syria','key_country':0}
,'taiwan':{'country':'Taiwan','key_country':1}
,'tajikistan':{'country':'Tajikistan','key_country':0}
,'tanzania':{'country':'Tanzania','key_country':0}
,'thailand':{'country':'Thailand','key_country':0}
,'togo':{'country':'Togo','key_country':0}
,'tokelau':{'country':'Tokelau','key_country':0}
,'tonga':{'country':'Tonga','key_country':0}
,'trinidadandtobago':{'country':'Trinidad and Tobago','key_country':0}
,'tunisia':{'country':'Tunisia','key_country':0}
,'turkey':{'country':'Turkey (Turecko)','key_country':0}
,'turkmenistan':{'country':'Turkmenistan','key_country':0}
,'turksandcaicosislands':{'country':'Turks and Caicos Islands','key_country':0}
,'tuvalu':{'country':'Tuvalu','key_country':0}
,'uganda':{'country':'Uganda','key_country':0}
,'ukraine':{'country':'Ukraine','key_country':0}
,'uae':{'country':'United Arab Emirates','key_country':1}
,'unitedkingdom':{'country':'United Kingdom','key_country':1}
,'usa':{'country':'United States','key_country':1}
,'uruguay':{'country':'Uruguay','key_country':0}
,'usminoroutlyingislands':{'country':'US Minor Outlying Islands','key_country':0}
,'sovietunion':{'country':'USSR (former) (SSSR)','key_country':0}
,'uzbekistan':{'country':'Uzbekistan','key_country':0}
,'vanuatu':{'country':'Vanuatu','key_country':0}
,'vatican':{'country':'Vatican City State (Holy See)','key_country':0}
,'venezuela':{'country':'Venezuela','key_country':0}
,'vietnam':{'country':'Viet Nam','key_country':0}
,'virginislandsbritish':{'country':'Virgin Islands (British)','key_country':0}
,'virginislandsus':{'country':'Virgin Islands (U.S.)','key_country':0}
,'wallisandfutunaislands':{'country':'Wallis and Futuna Islands','key_country':0}
,'westernsahara':{'country':'Western Sahara','key_country':0}
,'yemen':{'country':'Yemen','key_country':0}
,'yugoslavia':{'country':'Yugoslavia','key_country':0}
,'zaire':{'country':'Zaire','key_country':0}
,'zambia':{'country':'Zambia','key_country':0}
,'zimbabwe':{'country':'Zimbabwe','key_country':0}
}
selected_countries_how_to_use={
'ae':'United Arab Emirates'
,'ar':'Argentina'
,'at':'Austria (Rakousko)'
,'au':'Australia'
,'be':'Belgium'
,'bh':'Bahrain'
,'br':'Brazil'
,'ca':'Canada'
,'ch':'Switzerland'
,'cn':'China'
,'de':'Germany'
,'dk':'Denmark'
#,'es':'Spain' #This will confuse with language code es
,'hk':'Hong Kong'
,'il':'Israel'
,'in':'India'
,'jp':'Japan'
,'kp':'Korea (North)'
,'kr':'Korea (South)'
,'kw':'Kuwait'
,'mx':'Mexico'
,'my':'Malaysia'
,'nl':'Netherlands'
,'no':'Norway'
,'nz':'New Zealand (Aotearoa)'
,'qa':'Qatar'
,'ru':'Russian Federation (Rusko)'
,'sa':'Saudi Arabia'
,'se':'Sweden'
,'sg':'Singapore'
,'su':'USSR (former) (SSSR)'
,'tw':'Taiwan'
,'uk':'United Kingdom'
,'us':'United States'
,'vn':'Viet Nam'
,'za':'South Africa'
}

reuters_ticker_country = {'NYSE':'US','NASDAQ':'US','AU':'Australia', 'DH':'Bangladesh', 'HK':'China', 'SH':'China', 'SZ':'China', 'IN':'India', 'BY':'India', 'JK':'Indonesia', 'FU':'Japan', 'HQ':'Japan', 'JA':'Japan', 'NY':'Japan', 'OK':'Japan', 'SO':'Japan', 'TO':'Japan', 'SE':'Korea', 'KQ':'Korea', 'KU':'Malaysia', 'NZ':'New Zealand', 'KA':'Pakistan', 'Lah':'Pakistan', 'PH':'Philippines', 'SG':'Singapore', 'SL':'Sri Lanka', 'OT':'Taiwan', 'TW':'Taiwan', 'TH':'Thailand'}
google_finance_ticker_country = {'NYSE':'US', 'NASDAQ':'US','ASX':'Australia', 'HKG':'China', 'SHE':'China', 'SHA':'China', 'NSE':'India', 'BSE':'India', 'JAK':'Indonesia', 'FUK':'Japan', 'NJM':'Japan', 'JSD':'Japan', 'NAG':'Japan', 'OSA':'Japan', 'TYO':'Japan', 'SEO':'Korea', 'KDQ':'Korea', 'KUL':'Malaysia', 'NZE':'New Zealand', 'KAR':'Pakistan', 'Lah':'Pakistan', 'PSE':'Philippines', 'SIN':'Singapore', 'COL':'Sri Lanka', 'TPE':'Taiwan', 'BAK':'Thailand'}

class WebURLParse():
    def __init__(self,website_url,developer_mode=False,print_instance=None,ignore_errors=True,log_process_status=True):
        self.developer_mode=developer_mode
        self.log_process_status=log_process_status
        self.ignore_errors=ignore_errors
        self.initiate_print_instance(print_instance=print_instance)
        self.set_url(website_url)
    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True,message_priority=''):
        module_name='WebURLParse'
        input_string=input_string_in
        if isinstance(input_string,str):
            input_string = get_html_to_unicode_string(input_string)
        if self.print_instance:
            self.print_instance.customPrint(input_string,skip_timestamp=skip_timestamp,add_leading_space=add_leading_space,module_name=module_name,message_priority=message_priority)
        else:
            print_string=u'' + module_name + '\t' + message_priority + '\t' + input_string
            if not skip_timestamp:
                print_string = log_time_stamp() + print_string
            print get_printable_string(print_string)
    def initiate_print_instance(self,print_instance=None):
        self.print_instance=None
        if print_instance:
            try:
                if print_instance.check():
                    self.print_instance=print_instance
                    return True
            except:            
                return False        
        return False  
    def set_url(self,website_url,description=None,title=None):
        self.website_url=website_url.lower() #lower() is to avoid error while replacing domain suffix from the url
        self.website_url_passed=website_url
        self.description=description
        self.title=title
        self.valid_website=True
        self.website_www_type=''
        self.website_schema=''
        self.website_sub_domain_name=''
        self.website_path=''
        self.port=''
        self.website_param=''
        self.website_domain_name=''
        
        self.website_parent=''
        self.website_suffix=''
        
        self.normalize_website_url()
        #self.website_domain_name=self.process_domain_name()
        #self.website_suffix=self.process_website_suffix()
        #self.website_country_name=self.process_country_name()
        #self.website_parent=self.process_website_parent()
        #self.website_domain_details=self.process_domain_details()
        self.process_domain_name()
        #self.display()
        self.process_website_suffix()
        #self.display()
        self.process_country_name()
        #self.display()
        self.process_website_parent()
        self.process_links_country_code()
        self.process_domain_details()
        self.process_ticker_info()
    def normalize_website_url(self):
        print_prefix='normalize_website_url:\t'
        self.website_param=''
        if self.website_url:
            first_part_of_website=''
            last_part_of_website=''
            if '?' in self.website_url:
                temp_split=self.website_url.split('?')
                if len(temp_split) <= 2:
                    self.website_url=temp_split[0]
                    if len(temp_split) == 2:
                        self.website_param=temp_split[1]
                elif len(temp_split)>2:
                    self.website_url=temp_split[0]
                    self.website_param='?'.join(temp_split[1:])
                else:
                    self.website_param=''
            else:
                self.website_param=''
            http_cnt=self.website_url.count('http:') + self.website_url.count('https:')
            if http_cnt > 1:
                self.valid_website=False
                if self.log_process_status:
                    self._print_(print_prefix + 'FATAL: more than two occurence for http(s) in the url:' + repr(self.website_url))
                if self.ignore_errors:
                    pass
                else:
                    exit()
            if '://' in self.website_url:
                temp_split=self.website_url.split('://')
                if len(temp_split) == 1:
                    first_part_of_website=temp_split[0]
                    last_part_of_website=''
                    if self.log_process_status:
                        self._print_(print_prefix + 'The url does not have proper place for ://. will not process the url further. Url Passed:' + self.website_url)
                    self.valid_website=False
                elif len(temp_split) == 2:
                    first_part_of_website=temp_split[0]
                    last_part_of_website=temp_split[1]
                else:
                    if self.log_process_status:
                        self._print_(print_prefix + 'The url does not have proper place for ://. will not process the url further. Url Passed:' + self.website_url)
                    self.valid_website=False
                    
            else:
                first_part_of_website=''
                last_part_of_website=self.website_url
            if len(first_part_of_website)>1:
                self.website_url = first_part_of_website + '://' + last_part_of_website.replace('//','/')
            else:
                self.website_url = last_part_of_website.replace('//','/')
        return True
    def process_links_country_code(self):
        if not self.valid_website:
            self.website_has_int_presence_elements=False
            self.website_int_presence_elements_details={'status':False,'data_found':'','country':''}
            return False
        if '://' in self.website_url:
            website_path_split=self.website_url.split('://')[1]
        else:
            website_path_split=self.website_url
        if '/' not in website_path_split:
            pass
        else:
            website_path_split=website_path_split.lower().split('/')
            for i_iter in range(len(website_path_split)):
                each_data=website_path_split[i_iter]
                if each_data in language_country_code_map:
                    self.website_has_int_presence_elements=True
                    self.website_int_presence_elements_details={'status':True,'data_found':each_data,'country':language_country_code_map[each_data]['country']}
                    return True
                elif each_data in country_short_code_map:
                    self.website_has_int_presence_elements=True
                    self.website_int_presence_elements_details={'status':True,'data_found':each_data,'country':country_short_code_map[each_data]['country']}
                    return True
                elif each_data in country_region_code_map:
                    self.website_has_int_presence_elements=True
                    self.website_int_presence_elements_details={'status':True,'data_found':each_data,'country':country_region_code_map[each_data]['country']}
                    return True
                elif each_data in country_common_code_map:
                    self.website_has_int_presence_elements=True
                    self.website_int_presence_elements_details={'status':True,'data_found':each_data,'country':country_common_code_map[each_data]['country']}
                    return True
                elif each_data in website_suffix_code_map:
                    if len(each_data) == 2 and (i_iter+1) < len(website_path_split):
                        if website_path_split[i_iter+1] in language_code_for_website:
                            self.website_has_int_presence_elements=True
                            self.website_int_presence_elements_details={'status':True,'data_found':each_data + '/' + website_path_split[i_iter+1],'country':website_suffix_code_map[each_data]}
                            return True
        self.website_has_int_presence_elements=False
        self.website_int_presence_elements_details={'status':False,'data_found':'','country':''}
        return False
    def process_domain_details(self):
        print_prefix='process_domain_details:\t'
        self.website_www_type=''
        self.website_schema=''
        self.website_sub_domain_name=''
        self.website_path=''
        #self.website_param=''
        if not self.valid_website:
            return {}
        path_param=''
        no_path=False
        no_param=False
        domain_name=self.website_domain_name
        domain_name_alone=self.website_parent
        domain_suffix=self.website_suffix
        if '://' in self.website_url:
            self.website_schema=self.website_url.split('://')[0]
            www_type_temp=self.website_url.split('://')[1]
        else:
            www_type_temp=self.website_url
        if '/' in www_type_temp:
            temp_string=www_type_temp
            www_type_temp=www_type_temp.split('/')[0]
            path_param=temp_string.replace(www_type_temp+'/','')
            if '?' in path_param:
                self.website_path=path_param.split('?')[0]
                #self.website_param=path_param.split('?')[1]
            else:
                self.website_path=path_param
                #self.website_param=''
        else:
            www_type_temp=www_type_temp
        if len(self.port) > 0:
            www_type_temp=www_type_temp.replace(':' + self.port,'')
        if '.' + self.website_parent + '.' + domain_suffix in domain_name:
            self.website_sub_domain_name=domain_name.replace('.' + self.website_parent + '.' + domain_suffix,'')
        if self.developer_mode:
            self._print_(print_prefix + 'website_parent:' + self.website_parent + '\t' + 'Suffix:' + domain_suffix)
        if len(www_type_temp) > len('.' + domain_name):
            self.website_www_type=www_type_temp.replace('.' + domain_name,'')
        if self.developer_mode:
            self._print_(print_prefix + 'Identified www type:' + self.website_www_type)
        if '.' in self.website_www_type:
            if self.log_process_status:
                self._print_(print_prefix + 'www identification failed. will not process the url further. www identified:' + self.website_www_type)
            self.valid_website=False
            if self.ignore_errors:
                pass
            else:
                #http://www.agoracom.comwww.agoracom.com/ir/POETTechnologies/forums/discussion/topics/653621-bae-systems-nashua-n-h-a-navy-11-million-contract-for-fssr-idf/messages/2051254
                self._print_(print_prefix + 'FATAL: get_domain_details: www_type logic:' + self.website_www_type + ' for url:' + self.website_url)
                exit()
        return {'schema':self.website_schema,'input':self.website_url,'www_type':self.website_www_type,'sub_domain':self.website_sub_domain_name,'domain_name':self.website_domain_name,'domain_alone':self.website_parent,'path':self.website_path,'param':self.website_param}
    def process_website_parent(self):
        print_prefix='get_website_parent:\t'
        if not self.valid_website:
            self.website_parent=''
            return self.website_parent
        domain_name=self.website_domain_name
        domain_suffix=self.website_suffix
        if self.developer_mode: 
            self._print_(print_prefix + 'domain_name=' + str(domain_name) + '\t domain_suffix=' + str(domain_suffix))
        domain_name_without_suffix_length=len(domain_name) - len('.' + domain_suffix)
        if self.developer_mode: 
            self._print_(print_prefix + 'domain_name_without_suffix_length=' + str(domain_name_without_suffix_length))
        domain_name_without_suffix=domain_name[0:domain_name_without_suffix_length]
        domain_name_without_suffix_split=domain_name_without_suffix.split('.')
        if len(domain_name_without_suffix_split)>1:
            parent_domain=domain_name_without_suffix_split[-1]
        else:
            parent_domain=domain_name_without_suffix
        self.website_parent=parent_domain.lower()
        return self.website_parent
    def process_country_name(self,output_none=False): 
        if not self.valid_website:
            self.website_country_name=''
            return self.website_country_name
        if output_none:
            output_name=None
        else:
            output_name=''
        input_website=self.website_suffix
        if len(input_website) > 1:
            if '.' in input_website:
                lookup_suffix=input_website.split('.')[-1]
            else:
                lookup_suffix=input_website
            if lookup_suffix in website_suffix_code_map:
                if len(lookup_suffix) == 2:
                    output_name=website_suffix_code_map[lookup_suffix]
                elif len(lookup_suffix) == 3 and lookup_suffix == 'int':
                    pass #Not sure whether we encounter this scenario
                elif len(lookup_suffix) == 4 and lookup_suffix == 'arpa':
                    output_name=website_suffix_code_map[lookup_suffix]
                else:
                    pass
            else:
                pass
        else:
            pass
        self.website_country_name=output_name
    def process_website_suffix(self):
        print_prefix='process_website_suffix:\t'
        if not self.valid_website:
            self.website_suffix=''
            return self.website_suffix
        website_url_formatted=self.website_domain_name
        website_url_formatted_split=website_url_formatted.split('.')
        website_url_formatted_split_length=len(website_url_formatted_split)
        current_index=-1
        suffix_found=False
        suffix_text=''
        if website_url_formatted_split_length <= 1: 
            self.website_suffix=''
            return ''
        for i in range(website_url_formatted_split_length):
            current_suffix=website_url_formatted_split[current_index]
            if self.developer_mode: 
                self._print_(print_prefix + 'Wesbite :' + str(self.website_url) + '\tcurrent suffix - ' + str(current_suffix) + ': Suffix found=' + str(suffix_found))
            if suffix_found:
                if current_suffix in website_suffix_code_list and website_url_formatted_split_length>2:
                    if self.developer_mode: 
                        self._print_(print_prefix + 'Website:' + str(self.website_url) + '\tInside 2nd suffix - ' + str(current_suffix))
                    suffix_text=current_suffix + '.' + suffix_text
                break
            else:
                try:
                    suffix_text=str(current_suffix)
                    suffix_found=True
                except Exception as e:
                    self.valid_website=False
                    suffix_text=''
                    suffix_found=False
                    if self.ignore_errors:
                        return ''
                    else:
                        #http://www.agoracom.comwww.agoracom.com/ir/POETTechnologies/forums/discussion/topics/653621-bae-systems-nashua-n-h-a-navy-11-million-contract-for-fssr-idf/messages/2051254
                        self._print_(print_prefix + 'FATAL: get_domain_details: suffix logic: for url:' + repr(self.website_url) + '\t Error:' + str(e))
                        exit()
            current_index -= 1
        self.website_suffix=suffix_text
        return self.website_suffix
    def process_domain_name(self):
        print_prefix='process_domain_name:\t'
        if not self.valid_website:
            self.website_domain_name=''
            return self.website_domain_name
        if '//' in self.website_url:
            website_url_formatted=self.website_url[self.website_url.find('//')+2:]
        else:
            website_url_formatted=self.website_url
        if '/' in website_url_formatted:
            website_url_formatted=website_url_formatted[0:website_url_formatted.find('/')]
        if '.' not in website_url_formatted:
            self.valid_website=False
            self.website_domain_name=''
            if self.developer_mode:
                self._print_(print_prefix + 'FATAL: : No dot present in domain name:' + repr(self.website_url))
            if self.ignore_errors:
                pass
            else:
                exit()
            return self.website_domain_name
        if ':' in website_url_formatted:
            port_split=website_url_formatted.split(':')
            if len(port_split) != 2:
                if self.developer_mode:
                    self._print_(print_prefix + 'FATAL: Colon(:) is used more than once in the domain name:' + repr(website_url_formatted) + ' in website:' + repr(self.website_url))
                self.valid_website=True
                if self.ignore_errors:
                    pass
                else:
                    exit()
            if len(port_split[1])>0 and is_number(input_text=port_split[1],check_for_integer=True):
                self.port=port_split[1]
                website_url_formatted=port_split[0]
            else:
                if self.developer_mode:
                    self._print_(print_prefix +  'FATAL: Port number specified in the domain is not integer:' + repr(port_split[1]) + ' in website:' + repr(self.website_url))
                self.valid_website=True
                if self.ignore_errors:
                    pass
                else:
                    exit()
        spec_characters=re.sub(r'[a-z0-9\.-]','',website_url_formatted)
        if len(spec_characters) > 0:
            self.valid_website=False
            if self.developer_mode:
                self._print_(print_prefix + 'FATAL: the following characters are not allowed in domain name:' + repr(spec_characters) + ' in website:' + repr(self.website_url))
            if self.ignore_errors:
                pass
            else:
                exit()
        website_url_formatted_split=website_url_formatted.split('.')
        if len(website_url_formatted)>1 and len(website_url_formatted_split)>2:
            first_split=website_url_formatted_split[0]
            if len(first_split)> 0 and len(first_split) < 6: ##wwwen.#earlier 7 now 6.
                if first_split.lower().startswith('ww'):#ww
                    #website_url_formatted=website_url_formatted.replace(first_split + '.','')
                    website_url_formatted='.'.join(website_url_formatted_split[1:])
        self.website_domain_name=website_url_formatted.lower()
        return self.website_domain_name
    def process_ticker_info(self):
        print_prefix='process_ticker_info\t'
        ticker_url=self.website_url
        ticker_url_title=self.title
        ticker_url_description=self.description
        self.ticker_available=False
        self.ticker_source=''
        self.ticker_exchange=''
        self.ticker=''
        self.ticker_country=''
        if not self.valid_website:
            return False
        try:#To be handled properly
            if 'reuters.com/finance/stocks/overview?symbol=' in ticker_url:
                result_dict = {}
                temp_string_split=ticker_url.split('reuters.com/finance/stocks/overview?symbol=')
                if len(temp_string_split)>1:
                    temp_string=temp_string_split[1]
                else:
                    temp_string=''
                if '.' in temp_string:
                    self.ticker_source = 'Reuters'
                    self.ticker = temp_string.split('.')[0]
                    self.ticker_country = ''
                    self.ticker_exchange = temp_string.split('.')[1]
                    if self.ticker_exchange in reuters_ticker_country.keys(): 
                        self.ticker_country = reuters_ticker_country[self.ticker_exchange]
            elif 'bloomberg.com/quote/' in ticker_url:
                result_dict = {}
                temp_string_split=ticker_url.split('bloomberg.com/quote/')
                if len(temp_string_split)>1:
                    temp_string=temp_string_split[1]
                else:
                    temp_string=''
                if ':' in temp_string:
                    self.ticker_source = 'Bloomberg'
                    temp_string=temp_string.split(':')
                    self.ticker = temp_string[0]
                    self.ticker_country = temp_string[1]
                    self.ticker_exchange = ''
                    if ticker_url_description and 'Stock analysis for ' in ticker_url_description and ':' in ticker_url_description and '(' in ticker_url_description:
                        tick = ticker_url_description.split('(')[1]
                        if ')' in tick:
                            tick=tick.split(')')[0]
                            if ':' in tick:
                                if tick.split(':')[0] == self.ticker:
                                    self.ticker_exchange = tick.split(':')[1]
            elif 'www.marketwatch.com/investing/Stock/' in ticker_url and '?countryCode=' in ticker_url:
                result_dict = {}
                self.ticker_source = 'Marketwatch'
                self.ticker = ticker_url.split('/Stock/')[1].split('?countryCode=')[0]
                self.ticker_country = ticker_url.split('?countryCode=')[1]
                self.ticker_exchange = ''
            elif 'finance.yahoo.com/q?s=' in ticker_url:
                result_dict = {}
                self.ticker_source = 'Yahoo Finance'
                temp_string_split = ticker_url.split('finance.yahoo.com/q?s=')
                if len(temp_string_split)>1:
                    temp_string=temp_string_split[1]
                else:
                    temp_string=''
                self.ticker = temp_string
                self.ticker_country = ''
                self.ticker_exchange = ''
            elif 'google.com/finance?cid=' in ticker_url:
                result_dict = {}
                self.ticker_source = 'Google Finance'
                if ticker_url_title and ' quotes & news' in ticker_url_title:
                    t_tick_list = ticker_url_title.split(" quotes & news")[0].split(":")
                    self.ticker = t_tick_list[-1]
                    self.ticker_exchange = str(t_tick_list[-2]).strip()
                self.ticker_country = ''
                if ticker_url_description and 'Get detailed financial information on' in ticker_url_description and ':' in ticker_url_description and '(' in ticker_url_description:
                    tick = ticker_url_description.split('(')[1].split(')')[0]
                    if ':' in tick and tick.split(':')[1] == self.ticker:
                        self.ticker_exchange = tick.split(':')[0]
                if self.ticker_exchange in google_finance_ticker_country.keys(): 
                    self.ticker_country = google_finance_ticker_country[self.ticker_exchange]
            elif 'www.nasdaq.com/symbol/' in ticker_url:
                result_dict = {}
                self.ticker_source = 'Nasdaq'
                self.ticker = ticker_url.split('www.nasdaq.com/symbol/')[1].upper()
                self.ticker_country = ''
                self.ticker_exchange = ''
        except Exception as e:
            self._print_(print_prefix + 'error while processing ' + ticker_url + '. Error:' + str(e))
    def get_website_country_name(self,website_link=None):
        if website_link:
            if website_link == self.website_url:
                pass
            else:
                self.set_url(website_url=website_link)
        return self.website_country_name
    def get_website_parent(self,website_link=None):
        if website_link:
            if website_link == self.website_url:
                pass
            else:
                self.set_url(website_url=website_link)
        return self.website_parent
    def get_website_domain_name(self,website_link=None):
        if website_link:
            if website_link == self.website_url:
                pass
            else:
                self.set_url(website_url=website_link)
        return self.website_domain_name
    def get_website_suffix(self,website_link=None):
        if website_link:
            if website_link == self.website_url:
                pass
            else:
                self.set_url(website_url=website_link)
        return self.website_suffix
    def get_website_domain_alone(self,website_link=None):
        if website_link:
            if website_link == self.website_url:
                pass
            else:
                self.set_url(website_url=website_link)
        return self.website_parent
    def get_website_schema(self,website_link=None):
        if website_link:
            if website_link == self.website_url:
                pass
            else:
                self.set_url(website_url=website_link)
        return self.website_schema
    def get_website_www_type(self,website_link=None):
        if website_link:
            if website_link == self.website_url:
                pass
            else:
                self.set_url(website_url=website_link)
        return self.website_www_type
    def get_website_sub_domain_name(self,website_link=None):
        if website_link:
            if website_link == self.website_url:
                pass
            else:
                self.set_url(website_url=website_link)
        return self.website_sub_domain_name
    def get_website_param(self,website_link=None):
        if website_link:
            if website_link == self.website_url:
                pass
            else:
                self.set_url(website_url=website_link)
        return self.website_param
    def get_website_path(self,website_link=None):
        if website_link:
            if website_link == self.website_url:
                pass
            else:
                self.set_url(website_url=website_link)
        return self.website_path
    def get_website_port(self,website_link=None):
        if website_link:
            if website_link == self.website_url:
                pass
            else:
                self.set_url(website_url=website_link)
        return self.port
    def get_domain_details(self,website_link=None):
        if website_link:
            if website_link == self.website_url:
                pass
            else:
                self.set_url(website_url=website_link)
        if not self.valid_website:
            return {'schema':'','input':'','www_type':'','sub_domain':'','domain_name':'','domain_alone':'','path':'','param':'','suffix':'','country':'','has_ticker':'','ticker':'','ticker_exchange':'','ticker_country':'','ticker_source':''}
        return {'schema':self.website_schema,'input':self.website_url,'www_type':self.website_www_type,'sub_domain':self.website_sub_domain_name,'domain_name':self.website_domain_name,'domain_alone':self.website_parent,'path':self.website_path,'param':self.website_param,'suffix':self.website_suffix,'country':self.website_country_name,'has_ticker':self.ticker_available,'ticker':self.ticker,'ticker_exchange':self.ticker_exchange,'ticker_country':self.ticker_country,'ticker_source':self.ticker_source}
    def get_international_presence_details(self,website_link=None):
        if website_link:
            if website_link == self.website_url:
                pass
            else:
                self.set_url(website_url=website_link)
        return self.website_int_presence_elements_details
    def display(self):
        if self.developer_mode:
            self._print_('Website:' + self.website_url)
            self._print_('schema:' + self.website_schema)
            self._print_('domain_name:' + self.website_domain_name)
            self._print_('Sub Domain:' + self.website_sub_domain_name)
            self._print_('domain_alone:' + self.website_parent)
            self._print_('suffix:' + self.website_suffix)
            self._print_('Port:' + self.port)
            self._print_('www:' + self.website_www_type)
            self._print_('Path:' + self.website_path)
            self._print_('Param:' + self.website_param)
'''
def get_website_country_name(input_website_in,input_format='url',output_none=False): #Other input_format is suffix - future use
    ins=WebURLParse(website_url_in)
    return ins.get_website_country_name
def get_website_parent(website_url_in):
    ins=WebURLParse(website_url_in)
    return ins.get_website_parent
def get_website_domain_name(website_url_in):
    ins=WebURLParse(website_url_in)
    return ins.get_website_domain_name
def get_website_suffix(website_url_in):
    ins=WebURLParse(website_url_in)
    return ins.get_website_suffix
def get_domain_details(website_url_in):
    ins=WebURLParse(website_url_in)
    return ins.get_domain_details
'''    
if __name__ == '__main__':
    if not True:
        web_ins=WebURLParse('fiind.com',ignore_errors=False,developer_mode=True)
        link_list=['http://www.wsgwww.com/']#['https://www.d-labs.com:443/','http://www.preferredmart.com:80/','https://eservices.steveco.fi:8090/kct/ShowLogin']#['https://www.d-labs.com:443/','http://www.preferredmart.com:80/']
        for each_link in link_list:
            web_ins.set_url(each_link)
            '''
            print 'LINK:',each_link
            print 'DOMAIN:',web_ins.get_website_domain_name()
            print 'PARENT:',web_ins.get_website_parent()
            print 'SUFFIX:',web_ins.get_website_suffix()
            print 'COUNTRY:',web_ins.get_website_country_name()
            print 'DETAILS:',web_ins.get_domain_details()
            print 'INT:',web_ins.get_international_presence_details()
            '''
            output_string=each_link + '\t Domain:' + web_ins.get_website_domain_name() + '\t Parent:' + web_ins.get_website_parent()  + '\t Suffix:' + web_ins.get_website_suffix()  + '\t Country:' + web_ins.get_website_country_name()  + '\t Sub Domain:' + web_ins.get_domain_details()['sub_domain']  + '\t Path:' + web_ins.get_domain_details()['path']  + '\t Param:' + web_ins.get_domain_details()['param'] + '\t WWW:' + web_ins.get_website_www_type() +'\t Port:' + web_ins.get_website_port()
            output_string = output_string + '\t International Presence Status:' + str(web_ins.get_international_presence_details()['status']) + '\t International Presence Country:' + web_ins.get_international_presence_details()['country'] + '\t Data Found:' + web_ins.get_international_presence_details()['data_found']
            print output_string + '\n'
    elif True:
        web_ins=WebURLParse('fiind.com',ignore_errors=True,developer_mode=False)
        link_list=[
                    'http://www.Hoovers.com/company-information/cs/company-profile.Telstra_Corporation_Limited.a460e6e5b09e1a98.html'
                    ,'mywebsite.testing.aero'
                    ,'http://www.granbyindustries.com/en-us/brands/brand//4'
                    ,'http://www.wsgwww.com/'
                    ,'jp.fujitsu.com//group/fom'
        #          ]
        #'''
                    ,'https://www.cams.com.au/media/news/latest-news/preview-tatts-finke-desert-race'
                    ,'https://camsshop.shopdesq.com/hans-devices'
                    ,'http://corporate.evonik.com/en/company/locations/africa/Pages/default.aspx'
                    ,'http://corporate.evonik.com/en/company/locations/location-asia/Pages/default.aspx'
                    ,'http://corporate.evonik.com/en/company/locations/australia/Pages/default.aspx'
                    ,'http://corporate.evonik.com/en/company/locations/europe/Pages/default.aspx'
                    ,'http://corporate.evonik.com/en/company/locations/north-america/Pages/default.aspx'
                    ,'http://corporate.evonik.com/en/company/locations/south-america/Pages/default.aspx'
                    ,'https://honeywell.com/country/at/Pages/home.aspx'
                    ,'https://honeywell.com/country/ru/Pages/home.aspx'
                    ,'https://honeywell.com/country/me/Pages/home.aspx'
                    ,'http://www.nielsen.com/au/en/contact-us.html'
                    ,'https://eservices.steveco.fi:8090/kct/ShowLogin'
                    ,'http://fusion.google.com/add?feedurl=http://blog.ignify.com/feed/'
                    ,'http://185.15.169.148/web_asi/'
                    ,'http://www.suny.edu/howmuch/netpricecalculator.xhtml?embed=n&headerUrl=http://www.oldwestbury.edu/images/index/header_logo.jpg&bgColor=006000&id=13'
                ]
        #'''
        for each_link in link_list:
            web_ins.set_url(each_link)
            '''
            print 'LINK:',each_link
            print 'DOMAIN:',web_ins.get_website_domain_name()
            print 'PARENT:',web_ins.get_website_parent()
            print 'SUFFIX:',web_ins.get_website_suffix()
            print 'COUNTRY:',web_ins.get_website_country_name()
            print 'DETAILS:',web_ins.get_domain_details()
            print 'INT:',web_ins.get_international_presence_details()
            '''
            output_string=each_link + '\t Domain:' + web_ins.get_website_domain_name() + '\t Parent:' + web_ins.get_website_parent()  + '\t Suffix:' + web_ins.get_website_suffix()  + '\t Country:' + web_ins.get_website_country_name()  + '\t Sub Domain:' + web_ins.get_domain_details()['sub_domain']  + '\t Path:' + web_ins.get_domain_details()['path']  + '\t Param:' + web_ins.get_domain_details()['param'] + '\t WWW:' + web_ins.get_website_www_type()  +'\t Port:' + web_ins.get_website_port()
            output_string = output_string + '\t International Presence Status:' + str(web_ins.get_international_presence_details()['status']) + '\t International Presence Country:' + web_ins.get_international_presence_details()['country'] + '\t Data Found:' + web_ins.get_international_presence_details()['data_found']
            print output_string + '\n'
    elif not True:
        web_ins=WebURLParse('fiind.com',ignore_errors=True,developer_mode=True)
        link_list=[
                    'http://N/a/'
                    ,'http://http:/www.jboats.com'
                    ,'http://http:/www.ecobears.com/'
                    ,'http://http:/www.aisreporting.com'
                    ,'http://http:/www.bestbuddies.de'
                    ,'http://http:/www.thecomputercentre.co.uk'
            ]
        for each_link in link_list:
            web_ins.set_url(each_link)
            '''
            print 'LINK:',each_link
            print 'DOMAIN:',web_ins.get_website_domain_name()
            print 'PARENT:',web_ins.get_website_parent()
            print 'SUFFIX:',web_ins.get_website_suffix()
            print 'COUNTRY:',web_ins.get_website_country_name()
            print 'DETAILS:',web_ins.get_domain_details()
            print 'INT:',web_ins.get_international_presence_details()
            '''
            print each_link,'\t',web_ins.get_website_domain_name(each_link)