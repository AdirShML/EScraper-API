from pymongo import MongoClient
from scrap import scrap_per_key
import re
from requests import post

# connect to MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# access a specific database
db = client['Scraperdb']

# access a collection in the DB
collection = db['itemscraper']
tracklist = db['tracklist']

# this will store the item we already searched for 
KEYS = []
LIST_OF_INTEREST = []

# insert the scraped data to DB, one by one
def insert_scraped_data(product_to_scrap: str):
    db_data = scrap_per_key(product_to_scrap)
    print(f'data is collected and ready to save: {db_data}') ## make sure we get the data
    try:
        results = collection.insert_many(db_data)
        print(f'data inserted successfully: {results.inserted_ids}')
    except Exception as e:
        print(f'error inserting data: {e}')
    
    KEYS.append(product_to_scrap)

# get all the available products
def get_products():
    return KEYS

# this function shows only the relevant data from db collection according to
# what the user want
def get_filtered_data(product_to_show: str):
    print(f'shows data for: {product_to_show}')
    try:
        results = collection.find({'title': product_to_show})
        if not results:
            print('Cannot find the item.')
        else:
            for result in results:
                print(result)
    except Exception as e:
        print(f'error querying {e}')
        # for easier debug and flexibility, convert the cursor to a list 
    list_results = list(results)
    return list_results
    
# checks wether the search key is existing in db already or not
# will return the filtered data if exsisting or will save the new data
def check_existing_data(search_key: str):
    print(f'check if the searching input is already existing in the list')
    try:
        results = collection.find({'title': search_key})
        if results:
            print(f'data already exists')
        else:
            print(f'scraping new data:{search_key}')
            insert_scraped_data(search_key)
                
    except Exception as e:
        print(f'error checking for exsisting data: {e}')
    
    finally:
        existing_data = get_filtered_data(search_key)
        return existing_data
 
# removes a value from the DB (and from the list)
def remove_data(remove: str):
    try:
        results = collection.delete_many({'title': remove})
        if results:
            print(f'deleted {results.deleted_count} docs')
            return True
        
        else: return None
         
    except Exception as e:
        print(f'error deleting data: {e}')

# this function shows the average price of specific product according
# to the founded results 
def calculate_avg_price_of_product(product_to_calc: str):
    prices_list = []
    try:
        documets = collection.find({'title': product_to_calc})
        print(f'calculates average price of: {product_to_calc}...')
        for doc in documets:
            if 'price' in doc:
                price_str = doc['price']
                converted_price = convert_price_str_to_float(price_str)
                if converted_price is not None:
                    prices_list.append(converted_price)
                    
    except Exception as e:
        print(f'error calculating avg value: {e}')
        #return 0
    # if there are not valid prices/empty list     
    if not prices_list:
        return 0
    
    total_sum = sum(prices_list)
    avg = total_sum/ len(prices_list)
    print(f'the average price for this product:{avg}')
    return avg

# this function converts the prices to float in order to calc average price
def convert_price_str_to_float(price_str):
     # Extract the numeric part using a regular expression
    match = re.search(r'[\d,]+\.\d{2}', price_str)
    if match:
        # Remove commas and convert to float
        numeric_str = match.group().replace(',', '')
        return float(numeric_str)
    return None
    
# this function will show the cheapest results for a saved search
def show_cheapest_data(product: str):
    cheapest_results = []
    results = get_filtered_data(product)
    for res in results:
        if 'price' in res:
            title_str = res['title']
            price_str = res['price']
            link_str = res['link']
            convert = convert_price_str_to_float(price_str)
            if convert is not None:
                cheapest_results.append({'title': title_str, 'price': convert, 'link': link_str})
    
    top_results = sorted(cheapest_results, key=lambda x: x['price'])
    print(top_results)
    return top_results

# this function take an item from the main DB (according to objectsID)
# save it in a new collection - 'track list' + will add the overall avg price                      
def focus_on_data(tracked_item: str):
    result_to_focus = collection.find_one({'title': tracked_item})
    print(f'{result_to_focus} add to the tracklist')
    if result_to_focus['objectid'] is None:
        print(f'there is no such item or its removed')
    else:
        avg_price = calculate_avg_price_of_product(tracked_item)
        item = tracklist.insert_one(result_to_focus, {'average price': avg_price})
        LIST_OF_INTEREST.append(item)
        print(f'inserted to tracklist: {item.inserted_id}')
        
    return LIST_OF_INTEREST

# removes from the tracklist
def remove_item_from_tracklist(remove_value: str):
    try:
        result = tracklist.delete_one({'title': remove_value})
        print(f'deleted {result.deleted_count}')
        LIST_OF_INTEREST.remove(remove_value)
        
    except Exception as e:
        print(f'error deleting data: {e}')

# make a post request for this app 
def post_results(results, endpoint, search_text):
    headers = {
        "Content-Type": "application/json"
    }        
    data = {"data": results, "search_text": search_text}
    print("Sending request to", endpoint)
    response = post("http://localhost:8000" + endpoint,
                    headers=headers, json=data)
    print("Status code:", response.status_code)
    
###### maybe there will be a function that add item to the tracklist!!! ######

# main function:
def main(search_text: str, endpoint):
    print(f'connecting to the browser')
    insert_scraped_data(search_text)
    results = get_filtered_data(search_text)
    post_results(results, endpoint, search_text)
    client.close()
    

if __name__ == "__main__":
    # example of usage/demo run
    main('Gibson Les Paul')
                              



