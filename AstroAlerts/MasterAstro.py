def replace_spl_characters(content,spl_characters=['\r\n','\n','\r','\t','   ','  '],replace_by=' '): # removes spaces,tabs,new lines 
    for each_spl_char in spl_characters:
        content=content.replace(each_spl_char,replace_by)
    return content
    
def fetch_for_url2(url,skip_file_check=False): # returns url content from saved files/ direct hit  
    file_name=get_file_name_to_save(url)
    full_file_path=os.path.join(collected_path,file_name)
    if not skip_file_check:
        if os.path.isfile(full_file_path):
            file_presence=True
            print ('File exists !!')
            html_content=open(full_file_path).read()
            #print ('from file html_content :',html_content.encode('utf-8'))
    else:
        try:
            r = requests.get(url)
            status_code=r.status_code
            html_content=r.text
            len_html_content=len(html_content)
            #print ('content received from URL Hit :',len_html_content)
            if len_html_content>500 and r.status_code==200:
                with open(full_file_path,'a') as fp:
                    fp.write(str(html_content.encode('utf-8')))
                print ('File content saved !!')
        except Exception as  e:
            print  ('Exception in getting URL content :',e)
            html_content=''
    if html_content:
        soup = BeautifulSoup(html_content)
        for elem in soup.findAll(['script', 'style','select','nav']):
            elem.extract()
        soup_text=str(soup.text)
        soup_text=replace_spl_characters(soup_text)
        return soup_text
    return html_content
