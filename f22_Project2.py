from xml.sax import parseString
from bs4 import BeautifulSoup
import re
import os
import csv
import unittest

#Worked with Noah Young

def get_listings_from_search_results(html_file):
    with open(html_file, "r") as file:
        soup = BeautifulSoup(file, 'html.parser')
        titles = []
        l_id = []
        cost = []
        final = []
        listing = soup.find_all("div", class_ = "t1jojoys dir dir-ltr")
        price = soup.find_all("span", class_="_tyxjp1")
        for i in range(len(listing)):
            titles.append(listing[i].text)
            l_id.append(listing[i].get('id').split("_")[1])
            cost.append(price[i].text.strip('$'))
    for i in range(len(titles)):
        final.append((titles[i], int(cost[i]), l_id[i]))
    return final

#print(get_listings_from_search_results("html_files/mission_district_search_results.html"))

def get_listing_information(listing_id):
    url = "html_files/" + "listing_" + str(listing_id) + ".html"
    with open(url, "r") as file:
        soup = BeautifulSoup(file, 'html.parser')
        bedroom_l = []
        room_type = None
        policy = soup.find_all('li', class_="f19phm7j dir dir-ltr")
        room = soup.find('h2', class_='_14i3z6h')
        bedroom = soup.find_all('span')
        for i in range(len(policy)):
            if policy[i].contents[0] == "Policy number: ":
                policynumber = policy[i].contents[1].text
                if 'pending' in policynumber.lower():
                    policynumber = "Pending"
                elif re.search(r'[0-9]', policynumber):
                    continue
                else:
                    policynumber = "Exempt"
        words = room.text
        if "entire" in words.lower():
            room_type = "Entire Room"
        elif "private" in words.lower():
            room_type = "Private Room"
        else:
            room_type = "Shared Room"                 
        for i in range(len(bedroom)):
            if "bedroom" in bedroom[i].text:
                bedroom_l.append(bedroom[i].text)
        if len(bedroom_l) > 0:
            numberbeds = bedroom_l[0].split(" ")
            numberbeds = numberbeds[0]
            if numberbeds == 'Cozy':
                numberbeds = 1
            numberbeds = int(numberbeds)
        else:
            numberbeds = 1
    return (policynumber, room_type, numberbeds)

def get_detailed_listing_database(html_file):
    two_lst = []
    final = []
    one_lst = get_listings_from_search_results(html_file)
    for item in one_lst:
        two_lst.append(get_listing_information(item[2]))
    for i in range(len(one_lst)):
        final.append(one_lst[i] + two_lst[i])
    return final

# data = get_detailed_listing_database("html_files/mission_district_search_results.html")
# print(data)

def write_csv(data, filename):
    sorted_data = data.sort(key = lambda x: x[1])
    with open(filename,'w') as new:
        csv_new = csv.writer(new)
        csv_new.writerow(['Listing Title','Cost', 'Listing ID', 'Policy Number', 'Place Type', 'Number of Bedrooms'])
        for row in data:
            csv_new.writerow(row)
    return None

def check_policy_numbers(data):
    false = []
    for item in data:
        if item[3] == 'Pending' or item[3] == 'Exempt':
            continue
        else:
            if re.search('20[0-9]{2}-00[0-9]{4}STR|STR-000[0-9]{4}', item[3]):
                continue
            else:
                false.append(item[2])
    return false

# print(check_policy_numbers(data))          

def extra_credit(listing_id):
    url = "html_files/listing_" + str(listing_id) + "_reviews.html"
    with open(url, "r") as file:
        years = []
        year_dict = {}
        soup = BeautifulSoup(file, 'html.parser')
        year = soup.find_all('li', class_='_1f1oir5')
        for item in year:
            item = item.text
            years.append(item.split(" ")[1])
        for item in years:
            if item not in year_dict:
                year_dict[item] = 1
            else:
                year_dict[item] += 1
        sorted_dict = sorted(year_dict.items(), key=lambda x : x[1], reverse=True)
        if sorted_dict[0][1] > 90:
            return False
        else:
            return True

extra_credit(1944564)

class TestCases(unittest.TestCase):

    def test_get_listings_from_search_results(self):
        # call get_listings_from_search_results("html_files/mission_district_search_results.html")
        # and save to a local variable
        listings = get_listings_from_search_results("html_files/mission_district_search_results.html")
        # check that the number of listings extracted is correct (20 listings)
        self.assertEqual(len(listings), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(listings), list)
        # check that each item in the list is a tuple
        for item in listings:
            self.assertEqual(type(item), tuple)
        # check that the first title, cost, and listing id tuple is correct (open the search results html and find it)
        self.assertEqual(listings[0], ('Loft in Mission District', 210, '1944564'))
        # check that the last title is correct (open the search results html and find it)
        self.assertEqual(listings[-1][0], 'Guest suite in Mission District')

    def test_get_listing_information(self):
        html_list = ["1623609",
                     "1944564",
                     "1550913",
                     "4616596",
                     "6600081"]
        # call get_listing_information for i in html_list:
        listing_informations = [get_listing_information(id) for id in html_list]
        # check that the number of listing information is correct (5)
        self.assertEqual(len(listing_informations), 5)
        for listing_information in listing_informations:
            # check that each item in the list is a tuple
            self.assertEqual(type(listing_information), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(listing_information), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(listing_information[0]), str)
            self.assertEqual(type(listing_information[1]), str)
            # check that the third element in the tuple is an int
            self.assertEqual(type(listing_information[2]), int)
        # check that the first listing in the html_list has policy number 'STR-0001541'
        self.assertEqual(listing_informations[0][0], 'STR-0001541')
        # check that the last listing in the html_list is a "Private Room"
        self.assertEqual(listing_informations[-1][1], "Private Room")
        # check that the third listing has one bedroom
        self.assertEqual(listing_informations[2][-1], 1)

    def test_get_detailed_listing_database(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save it to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")
        # check that we have the right number of listings (20)
        self.assertEqual(len(detailed_database), 20)
        for item in detailed_database:
            # assert each item in the list of listings is a tuple
            self.assertEqual(type(item), tuple)
            # check that each tuple has a length of 6
            for item in detailed_database:
                self.assertEqual(len(item), 6)
        # check that the first tuple is made up of the following:
        # 'Loft in Mission District', 210, '1944564', '2022-004088STR', 'Entire Room', 1
        self.assertEqual(detailed_database[0], ('Loft in Mission District', 210, '1944564', '2022-004088STR', 'Entire Room', 1))
        # check that the last tuple is made up of the following:
        # 'Guest suite in Mission District', 238, '32871760', 'STR-0004707', 'Entire Room', 1
        self.assertEqual(detailed_database[-1], ('Guest suite in Mission District', 238, '32871760', 'STR-0004707', 'Entire Room', 1))

    def test_write_csv(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save the result to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")
        # call write csv on the variable you saved
        write_csv(detailed_database, "test.csv")
        # read in the csv that you wrote
        csv_lines = []
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.csv'), 'r') as f:
            csv_reader = csv.reader(f)
            for i in csv_reader:
                csv_lines.append(i)
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0], ['Listing Title', 'Cost', 'Listing ID', 'Policy Number', 'Place Type', 'Number of Bedrooms'])
        # check that the next row is Private room in Mission District,82,51027324,Pending,Private Room,1
        self.assertEqual(csv_lines[1], ['Private room in Mission District','82','51027324','Pending','Private Room','1'])
        # check that the last row is Apartment in Mission District,399,28668414,Pending,Entire Room,2
        self.assertEqual(csv_lines[-1], ['Apartment in Mission District','399','28668414','Pending','Entire Room','2'])

    def test_check_policy_numbers(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save the result to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")
        # call check_policy_numbers on the variable created above and save the result as a variable
        invalid_listings = check_policy_numbers(detailed_database)
        # check that the return value is a list
        self.assertEqual(type(invalid_listings), list)
        # check that there is exactly one element in the string
        self.assertEqual(len(invalid_listings), 1)
        # check that the element in the list is a string
        self.assertEqual(type(invalid_listings[0]), str)
        # check that the first element in the list is '16204265'
        self.assertEqual(invalid_listings[0], '16204265')

if __name__ == '__main__':
    database = get_detailed_listing_database("html_files/mission_district_search_results.html")
    write_csv(database, "airbnb_dataset.csv")
    check_policy_numbers(database)
    unittest.main(verbosity=2)
