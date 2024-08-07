from fastapi import FastAPI, Request
from scraper.main import *

app =FastAPI()

# the main view of the app - will show all of the exsisting products
@app.get("/products/")
async def main_page():
    keys = get_products()
    if not keys:
        return {'note': 'there is no data to show'}

    products = []
    for key in keys.split(','):
        products.append({'product': key})

    return {'products': products}

# this will scrap a product and show the filtered results
@app.post('/products/insert')
async def insert_product(request: Request):
    data = await request.json()
    single_results = []
    results = check_existing_data(data)
    for result in results:
        single_results.append(result)
        
    return single_results

# this function will remove a value from the db
@app.delete('/products/remove_data/{value_to_remove}')
async def remove_product(value_to_remove: str):
    remove_approval = remove_data(value_to_remove)
    if remove_approval:
        print(f'data {value_to_remove} is removed')
        return main_page()
    
    else:
        print(f'there is no such data')
        return main_page()
    
# this function calculates the avg of a specific product
@app.get('/products/average_price/{product_to_calc}')
async def average_price(product_to_calc: str):
    average_of_product = calculate_avg_price_of_product(product_to_calc)
    if average_of_product:
        return {'average price for the relevant product': average_of_product}
    
# this will return the top cheapest product of a specific
@app.get('/products/cheapest_top/{product}')
async def cheapest_product(product: str):
    returned_results = [] # the top results to return to the user 
    top_results = show_cheapest_data(product)
    for top in top_results:
        returned_results.append(top)
        
    return returned_results

# this is the focus on list that will run everyday (once in a day)
@app.get('/products/focus_list/{item}')
async def focus_list(item: str):
    track_list = []
    focus_items = focus_on_data(item)
    for i in focus_items:
        track_list.append(i)
        
    return track_list

# remove a product from the tracklist
@app.delete('/products/focus_list/remove/{item}')
async def remove_from_tracklist(item:str):
    remove_from_tracklist(item)
    print(f'data deleted from list')
    

        
    
             

        
        
    
    