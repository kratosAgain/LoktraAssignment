#!/usr/bin/python

import requests
import re
import argparse
from bs4 import BeautifulSoup


class Crawler(object):
    #http://www.shopping.com/clothing/batman/products~PG-2?KW=batman  is the url of shopping.com when searched for batman and page 2
    #so , pattern is defined in
    #search_tag  = item we want to search,,,,,,,,,page_tag = page we want to search
    Search = 'http://www.shopping.com/batman/products?CLT=SCH&KW={search_tag}'
    Search_in_page = 'http://www.shopping.com/products~PG-{page_tag}?KW={search_tag}'

    def __init__(self, search, page=1):
        self.search = search
        self.page=1
        if page != 1:
            self.page = page


    #returns data from HTML page

    def data_from_page(self,modified = 0):
        '''
        Each item is class="gridBox term, so fetching items based on that keyword
        '''
        if modified != 0:
            page = requests.get(self.Search_in_page.format(page_tag=modified,search_tag=self.search,))
        else:
            page = requests.get(self.Search_in_page.format(page_tag=self.page, search_tag=self.search, ))

        if page.status_code != 200:
            raise ValueError ("Something Went Wrong, Wrong Request\nAborting...\nAborting ...")


        soup = BeautifulSoup(page.text,'html.parser')
        item_list = soup.select('.gridBox')
        return item_list


    def items_from_page(self):
        #Items having class 'gridItemBtm' are search results.
        items_to_return = []
        item_list = self.data_from_page()

        for item in item_list:
            selected = item.select_one('.gridItemBtm')
            if selected:
                name = selected.select_one('.productName')
                if name:
                    #print ("i am here")
                    f_name = name.attrs.get('title')  or name.select_one('span').attrs.get('title')

                price = selected.select_one('.productPrice')
                if price:
                    f_price = price.string or price.select_one('a').string

                seller = selected.select_one('.newMerchantName')
                if seller:
                    f_seller = seller.string or seller.select_one('a').string

                if f_name and f_price and f_seller:
                    #print (f_name +"     "+f_price.strip)
                    items_to_return.append({'name':f_name,'price':f_price,'seller':f_seller})


        return items_to_return


    #if number of results are mentioned as 1500+ then we use this
    def using_PL_way(self):
        page = requests.get(self.Search.format(search_tag=self.search))
        if page.status_code != 200:
            raise ValueError("Something Went Wrong, Wrong Request\nAborting...\nAborting...")
        soup = BeautifulSoup(page.text, 'html.parser')
        items = soup.findAll("div", {"class": "paginationNew"})
        #print (len(items))
        #print(str(items[0]))
        #finding all digits in this segment
        num_list = re.findall(r'\d+',str(items))
        results = map(int, num_list)
        #print(max(results));

        #each page has 40 items , we have to find the items in last page now, which is the largest number in the list

        #self.page = max(results)
        item_list = self.data_from_page(max(results))
        count = 0
        for item in item_list:
            selected = item.select_one('.gridItemBtm')
            if selected:
                name = selected.select_one('.productName')
                price = selected.select_one('.productPrice')
                seller = selected.select_one('.newMerchantName')
                if name and price and seller:
                    count = count + 1

        return (max(results)-1)*40 + count;




    def number_of_items(self):
        page = requests.get(self.Search.format(search_tag=self.search))
        if page.status_code != 200:
            raise ValueError("Something Went Wrong, Wrong Request\nAborting...")
        #print(page.text);
        soup = BeautifulSoup(page.text, 'html.parser')
        #soup = BeautifulSoup(open(self.Search.format(search_tag=self.search)))
        #print(soup);
        result = None
        try:
            items = soup.findAll("span", {"class": "numTotalResults"})[0].string
            #items = soup.select('span#numTotalResults')[0].text
            item_str = ""
            #print(items);
            for item in items:
                item_str = item_str + str(item)
            #print(item_str)
            delim = "of"
            after_split = item_str.split(delim)
            result = (str(after_split[1]).strip())
            if "1500" in result:
                result = self.using_PL_way()
        except (IndexError, ValueError) as err:
            print("Something Went Wrong, No items present for your search item\nAborting ...")

        return result


    def print_items(self,items):
        print ("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        for item in items:
            print ("Item  : "+item.get('name').strip()+"\nPrice : "+item.get('price').strip()+"\nSeller: "+item.get('seller'))
            print ("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")




if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('search_tag',help="<enter search keyword here>")
    args.add_argument('page_tag', default=None,help="<enter page number here {optional}> ",nargs='?')

    args_list = args.parse_args()

    try:
        if args_list.page_tag and args_list.search_tag:
            crawler = Crawler(args_list.search_tag,args_list.page_tag)
            items = crawler.number_of_items()
            if items:
                print(("No of Items for {} : {}").format(args_list.search_tag,items))
                ans = (crawler.items_from_page())
                if ans:
                    crawler.print_items(ans)
                else:
                    print("This page is not available for this product")
        elif args_list.search_tag:
            crawler = Crawler(args_list.search_tag)
            items = crawler.number_of_items()
            if items:
                print(("No of Items for {} : {}").format(args_list.search_tag, items))
            #else:
            #    print(("No of Items for {} : 0").format(args_list.search_tag))
    except ValueError:
        args.print_help()










