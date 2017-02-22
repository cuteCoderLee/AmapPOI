#this module use amap api to get POI data of Wuhan
#thanks to amap company. please visit http://ditu.amap.com/ to get more information

#coding:utf-8

from urllib.request import urlopen
import xml.dom.minidom as minidom
import string

file_name='result.txt'                 #write result to this file
url_amap=r'http://restapi.amap.com/v3/place/text?&keyword=&types=01&city=4201&citylimit=true&output=xml&offset=20&page=1&key=e4ead3525fd497b1ca7a0dd97a7af55a&extensions=base'

facility_type=r'types=05'           #eating&shopping facilities
region=r'city=4201'                 #wuhan city
each_page_rec=20                    #results that displays in one page
which_pach=r'page=1'                #display which page
xml_file='tmp.xml'                  #xml file name

#write logs
def log2file(file_handle,text_info):
    file_handle.write(text_info)

#get html by url and save the data to xml file
def getHtml(url):
    page = urlopen(url)
    html = page.read()
    #print(type(html))

    try: 
        #open xml file and save data to it
        with open(xml_file,'wb') as xml_file_handle:
            xml_file_handle.write(html)
    except IOError as err:
        print("IO error: "+str(err))
        return -1

    return 0

#phrase data from xml
def parseXML(typecode):
    total_rec=1                      #record number
    
    #open xml file and get data record
    try:
        with open(file_name,'ab') as file_handle:
            dom = minidom.parse(xml_file)
            root = dom.getElementsByTagName("response") #The function getElementsByTagName returns NodeList.

            for node in root:
                total_rec=node.getElementsByTagName('count')[0].childNodes[0].nodeValue
                
                pois = node.getElementsByTagName("pois")
                for poi in pois[0].getElementsByTagName('poi'):
                    name=poi.getElementsByTagName("name")[0].childNodes[0].nodeValue
                    biztype=poi.getElementsByTagName("type")[0].childNodes[0].nodeValue
                    location=poi.getElementsByTagName("location")[0].childNodes[0].nodeValue
                    text_info=''+typecode+','+name+','+biztype+','+location+'\n'
                    #print(text_info)
                    #save data record
                    log2file(file_handle,text_info.encode('utf-8'))
                
    except IOError as err:
        print("IO error: "+str(err))

    return total_rec

def getPOIdata(url,typecode):
	if getHtml(url)==0:
		print('parsing page 1 ... ...')
		#parse the xml file and get the total record number
		total_record_str=parseXML(typecode)
		total_record=int(total_record_str)
		if (total_record%each_page_rec)!=0:
			page_number=int(total_record/each_page_rec)+2
		else:
			page_number=int(total_record/each_page_rec)+1
		#print(type(page_number))
		#retrive the other records
		for each_page in range(2,page_number):
			print('parsing page '+str(each_page)+' ... ...')
			url=url.replace('page='+str(each_page-1),'page='+str(each_page))
			getHtml(url)
			parseXML(typecode)
	else:
		print('error: fail to get xml from amap')

if __name__=='__main__':
	getPOIdata(url_amap,'01')
	for i in range(2,21):
		if i<10:
			typecode='0'+str(i)
			p_typecpde='0'+str(i-1)
		else:
			typecode=str(i)
			p_typecpde=str(i-1)
		url_amap=url_amap.replace('types='+p_typecpde, 'types='+typecode)
		getPOIdata(url_amap,typecode)
		print("the type of poi is "+typecode)