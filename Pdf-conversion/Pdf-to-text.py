import PyPDF2,sys,os,time

# creating a pdf file object
def pdf_to_text(file_name):
    text = []
    status = False
    pdfFileObj =''
    try:
        pdfFileObj = open(file_name, 'rb')
    except:
        status = 'file missing'
    if pdfFileObj:
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        total_pages = pdfReader.numPages
        for each_page in range(total_pages):
            pageObj = pdfReader.getPage(each_page)
            # time.sleep(10)
            text.append(str(pageObj.extractText()))

        # closing the pdf file object
        pdfFileObj.close()
    return {
            'text':text
            ,'total_pages':total_pages
    }
if __name__ == '__main__':
    input_file = sys.argv[1]
    # input_file = 'SuperExcel_2019.pdf'
    text_dict = pdf_to_text(file_name = input_file)
    text_list = text_dict['text']
    print('Total pages :',text_dict['total_pages'])
    for index,data in enumerate(text_list):
        print(index+1,len(data))




