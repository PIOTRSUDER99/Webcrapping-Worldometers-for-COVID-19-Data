from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from xlwt import Workbook

cont = True
while(cont):
    country_name = input("Country name: ")
    my_url = input("URL: ")
    user_agent = input("Please provide the name and version of the browser you are using. For example \"Mozilla/74.0\": ")

    # Opening the page
    req = Request(my_url, headers = {'User-Agent': user_agent})
    webpage = urlopen(req).read()

    # html parsing
    page_soup = soup(webpage, "html.parser")
    Content_array = page_soup.findAll("script", {"type" : "text/javascript", "class" : None, "src" : None})

    chart_string_list = list(filter(lambda s : str(s).find("coronavirus-cases-linear") != -1, Content_array))
    chart_string = str(chart_string_list[0])

    begin_index = chart_string.find("data: ")
    begin_index = 1 + begin_index + chart_string[begin_index ::].find("[")
    end_index = begin_index + chart_string[begin_index ::].find("]")
    
    num_list = chart_string[begin_index : end_index].split(",")

    begin_index = chart_string.find("categories: ")
    begin_index = 1 + begin_index + chart_string[begin_index ::].find("[")
    end_index = begin_index + chart_string[begin_index ::].find("]")

    category_list = chart_string[begin_index : end_index].split(",")

    # Writing into the file
    wb = Workbook()
    sheet1 = wb.add_sheet("Sheet 1")
    sheet1.write(0,0, "Day")
    sheet1.write(0,1, "Cases")
    sheet1.write(0,6, "Day")
    sheet1.write(0,7, "Cases")
    
    for i in range(len(num_list)):
        category_list[i] = category_list[i].replace("\"", "")
        sheet1.write(i + 1, 0, category_list[i])
        sheet1.write(i + 1, 1, num_list[i])
        sheet1.write(i + 1, 6, i + 1)
        sheet1.write(i + 1, 7, num_list[i])

    file_name = country_name + ".xls"
    wb.save(file_name)

    print("Done downloading data for " + country_name)
    cont_ans = input("To continue press \"y\". To exit press any other key. ")
    if cont_ans != "y":
        cont = False

