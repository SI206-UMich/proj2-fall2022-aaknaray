from xml.sax import parseString
from bs4 import BeautifulSoup
import re
import os
import csv
import unittest

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

#get_listings_from_search_results("html_files/mission_district_search_results.html")

def get_listing_information(listing_id):
    url = "html_files/" + "listing_" + str(listing_id) + ".html"
    with open(url, "r") as file:
        soup = BeautifulSoup(file, 'html.parser')
        policynum = []
        bedroom_l = []
        room_type = None
        policy = soup.find_all('li', class_="f19phm7j dir dir-ltr")
        room = soup.find_all('span')
        bedroom = soup.find_all('span')
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
        for i in range(len(room)):
            word_lst = room[i].text.split(" ")
            if "entire" in word_lst:
                room_type = "Entire Room"
            elif "shared" in word_lst:
                room_type = "Shared Room"
            elif "private" in word_lst:
                room_type = "Private Room"
        for i in range(len(policy)):
            policynum.append(policy[i].text.split(" "))
        policynumber = policynum[0][2]
        if policynumber == "City":
            policynumber = 'Pending'
        elif policynumber == 'pending':
            policynumber = policynumber.capitalize()
        elif policynumber == 'License':
            policynumber = 'Exempt'
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
            if re.search('20[0-9]{2}-00[0-9]{4}STR|STR-000[0-9]{4}''', item[3]):
                continue
            else:
                false.append(item[3])
    return False
            

def extra_credit(listing_id):
    """
    There are few exceptions to the requirement of listers obtaining licenses
    before listing their property for short term leases. One specific exception
    is if the lister rents the room for less than 90 days of a year.

    Write a function that takes in a listing id, scrapes the 'reviews' page
    of the listing id for the months and years of each review (you can find two examples
    in the html_files folder), and counts the number of reviews the apartment had each year.
    If for any year, the number of reviews is greater than 90 (assuming very generously that
    every reviewer only stayed for one day), return False, indicating the lister has
    gone over their 90 day limit, else return True, indicating the lister has
    never gone over their limit.
    """
    pass

'''

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

        # check that the first title, cost, and listing id tuple is correct (open the search results html and find it)

        # check that the last title is correct (open the search results html and find it)
        pass

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

        # check that the last listing in the html_list is a "Private Room"

        # check that the third listing has one bedroom

        pass

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

        # check that the first tuple is made up of the following:
        # 'Loft in Mission District', 210, '1944564', '2022-004088STR', 'Entire Room', 1

        # check that the last tuple is made up of the following:
        # 'Guest suite in Mission District', 238, '32871760', 'STR-0004707', 'Entire Room', 1

        pass

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

        # check that the next row is Private room in Mission District,82,51027324,Pending,Private Room,1

        # check that the last row is Apartment in Mission District,399,28668414,Pending,Entire Room,2

        pass

    def test_check_policy_numbers(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save the result to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")
        # call check_policy_numbers on the variable created above and save the result as a variable
        invalid_listings = check_policy_numbers(detailed_database)
        # check that the return value is a list
        self.assertEqual(type(invalid_listings), list)
        # check that there is exactly one element in the string

        # check that the element in the list is a string

        # check that the first element in the list is '16204265'
        pass
'''

if __name__ == '__main__':
    database = get_detailed_listing_database("html_files/mission_district_search_results.html")
    write_csv(database, "airbnb_dataset.csv")
    check_policy_numbers(database)
    unittest.main(verbosity=2)
