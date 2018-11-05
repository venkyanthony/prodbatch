import json
import re
import time
from selenium import webdriver
status_array=[]
all_status_array=[]
with open(r'input_1.json', 'r', encoding='utf-8') as f:
    input = json.load(f)
for row in input:
    company_name=row['Company']
    location_name=row['Location']
    title_name=row['Title']
    man_company_name =  re.sub(r'[\W_]+', '', company_name)
    man_company_name =  re.sub(r'(llc|inc|co|pvt|llp)', '', man_company_name)
    ori_company_name=company_name.lstrip()
    ori_company_name=ori_company_name.replace(" ","+")
    ori_company_name=ori_company_name.replace("&", "")
    title_name=title_name.replace(" ","+")
    title_name=title_name.replace("&", "")
    location_name=location_name.replace(" ","+")
    location_name=location_name.replace("&", "")
    google_url="https://www.google.co.in/search?q="+ori_company_name+"+in+"+location_name+"&ibp=htl;jobs";
    browser = webdriver.Chrome('D://chromedriver.exe')
    time.sleep(3)
    browser.get(google_url)
    time.sleep(5)
    browser.maximize_window()
    elems=browser.find_elements_by_xpath("//div[contains(@class,'nsol9b hxSlV') or contains(@class, 'k8RiQ nsol9b hxSlV')]")
    
    i=0
    links=''
    list=[]
    listOfApplys=[]
    list_of_list=[]
    for ele in elems:
        list.append(ele.text)
        if(i==2):
            i=0
            list_of_list.append(list)
            list=[]
        else:
            i=i+1

    apply_links=browser.find_elements_by_xpath("//a[@class='D7VqAe LwS2ce']")
    for link in apply_links:
        tag_=link.text
        if(tag_!=''):
            listOfApplys.append(tag_)

    def compare_1(via,company):
        #print("\n via ",via)
        #print("company ",company)
        if(via.find(company) == -1 or '-' in via):
            return 0
        else:
            return 1

    def compare_2(via,company):
        #print("\n via  ",via)
        #print("company   ",company)
        if(company.find(via)== -1 or '-' in via):
            return 0
        else:
            return 1

    job_type=0
    company_value=0
    regex_com=re.compile(r'(llc|inc|co|pvt|llp)',re.IGNORECASE)
    regex_via=re.compile(r'(at|the|via|jobs|,)',re.IGNORECASE)
    for i in (list_of_list):
        ori_resp_com=i[0]
        #print(ori_resp_com)
        #print(company_name)
        if(ori_resp_com==company_name):
            #print("First if")
            company_value=1
            matchedcompany = ori_resp_com
            matchedvia=i[2]
            resp_com =  re.sub(r'[\W_]+', '', ori_resp_com)
            resp_com =  re.sub(regex_com, '', resp_com)
            resp_com = re.sub(regex_via, '', resp_com)
            resp_com = resp_com.strip()
            via_temp=i[2]
            via_value=via_temp.strip()
            via_value=re.sub(r'[\W_]+', '', via_value)
            via_value =  re.sub(regex_com, '', via_value )
            via_value=re.sub(regex_via, '', via_value)
            #print(via_temp,via_value)
            #print(resp_com)
            job_type = compare_1(via_value,resp_com) if len(via_value)>=len(resp_com) else compare_2(via_value,resp_com)
            if(job_type==1):
                break
        elif(len(ori_resp_com) < len(company_name)):
            if(company_name.find(ori_resp_com) != -1):
                #print("Second if")
                company_value=1
                matchedcompany = ori_resp_com
                matchedvia=i[2]
                resp_com =  re.sub(r'[\W_]+', '', ori_resp_com)
                resp_com =  re.sub(regex_com, '', resp_com)
                resp_com = re.sub(regex_via, '', resp_com)
                resp_com = resp_com.strip()
                via_temp=i[2]
                via_value=via_temp.strip()
                via_value=re.sub(r'[\W_]+', '', via_value)
                via_value =  re.sub(regex_com, '', via_value )
                via_value=re.sub(regex_via, '', via_value)
                #print(via_temp,via_value)
                #print(resp_com)
                job_type = compare_1(via_value,resp_com) if len(via_value)>=len(resp_com) else compare_2(via_value,resp_com)
                if(job_type==1):
                    break
        elif(len(ori_resp_com) > len(company_name)):
            if(ori_resp_com.find(company_name) != -1):
                company_value=1
                #print("Third if")
                matchedcompany = ori_resp_com
                matchedvia=i[2]
                resp_com =  re.sub(r'[\W_]+', '', ori_resp_com)
                resp_com =  re.sub(regex_com, '', resp_com)
                resp_com = re.sub(regex_via, '', resp_com)
                resp_com = resp_com.strip()
                via_temp=i[2]
                via_value=via_temp.strip()
                via_value=re.sub(r'[\W_]+', '', via_value)
                via_value =  re.sub(regex_com, '', via_value )
                via_value=re.sub(regex_via, '', via_value)
                #print(via_temp,via_value)
                #print(resp_com)
                job_type = compare_1(via_value,resp_com) if len(via_value)>=len(resp_com) else compare_2(via_value,resp_com)
                if(job_type==1):
                    break
        if(job_type==0):
            for i in listOfApplys:
                #print("Fourth if")
                matchedvia=i
                resp_com =  re.sub(r'[\W_]+', '', ori_resp_com)
                resp_com =  re.sub(regex_com, '', resp_com)
                resp_com = re.sub(regex_via, '', resp_com)
                resp_com = resp_com.strip()
                via_temp=i[2]
                via_value=via_temp.strip()
                via_value=re.sub(r'[\W_]+', '', via_value)
                via_value =  re.sub(regex_com, '', via_value )
                via_value=re.sub(regex_via, '', via_value)
                #print(via_temp,via_value)
                #print(resp_com)
                job_type = compare_1(via_value,resp_com) if len(via_value)>=len(resp_com) else compare_2(via_value,resp_com)
                if(job_type==1):
                    company_value=1
                    break
        else:
            company_value=0
            job_type=0

    if (company_value == 1 and job_type == 1) :
        viaStatus = "Congrats! Your jobs are appearing on Google for Jobs."
        status=1
    elif ( company_value == 1 and job_type == 0) :
        viaStatus = "It does appear that your jobs are available on Google for Jobs, but only through a third party job board and as a result, they are not fully optimized. Ensure job seekers land on your careers page and stop paying extra for each job post by posting your jobs to Google for Jobs directly"
        status=2
    elif ( company_value == 0 and job_type == 0) :
        viaStatus = "Hmm, we were not able to find your job post on Google for Jobs."
        status=3
    status_array.append(viaStatus)
    status_array.append(status)
    status_array.append(google_url) 
    print(viaStatus)
    all_status_array.append(status_array)
    status_array=[]
    
    browser.quit()

with open('output_1.json', 'w') as outfile:
        json.dump(all_status_array, outfile)
    
