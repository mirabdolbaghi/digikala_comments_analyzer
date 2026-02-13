import requests
from tqdm import tqdm
def digikala_comment_pages(product_id,page):
    url = f"https://api.digikala.com/v1/rate-review/products/{product_id}/?page={page}"

    payload = {}
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://www.digikala.com',
    'priority': 'u=1, i',
    'referer': 'https://www.digikala.com/',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'x-web-client': 'desktop',
    'x-web-client-id': 'web',
    'x-web-optimize-response': '1',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()
    
def digikala_category_products(category_name,page=1):
    url = f"https://api.digikala.com/v1/categories/{category_name}/search/?page={page}"

    payload = {}
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.digikala.com',
        'priority': 'u=1, i',
        'referer': 'https://www.digikala.com/',
        'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        'x-web-client': 'desktop',
        'x-web-client-id': 'web',
        'x-web-optimize-response': '1',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()
def digikala_category_product_ids(category_name):
    data= digikala_category_products(category_name,1)
    total_page = data['data']['pager']['total_pages']
    product_ids = []
    for product in data["data"]["products"]:
        product_ids.append(product['id'])
    if total_page > 2:
        for i in tqdm(range(2,min(101,total_page+1))):
            data = digikala_category_products(category_name,i)
            for product in data["data"]["products"]:
                product_ids.append(product['id'])
    return product_ids
def digikala_clean_comments(dirty_comments,min_rate=0):
    comments_text=[]
    for c in dirty_comments:
        if min_rate <= c['rate']:
            comments_text.append((c["body"],c['rate']))
    return comments_text

def digikala_category_comments(category_name):
    product_ids = digikala_category_product_ids(category_name)
    comments=[]
    for id in tqdm(product_ids):
        comments += digikala_product_comments(id)
    return comments    
def digikala_product_comments(product_id):
    data= digikala_comment_pages(product_id,1)
    total_page = data['data']['pager']['total_pages']
    comments = []
    if 'comments' in data['data']:
        comments = digikala_clean_comments(data['data']['comments'])
    if total_page > 2:
        for i in range(2,total_page+1):
            data = digikala_comment_pages(product_id,i)
            if 'comments' in data['data']:
                comments += digikala_clean_comments(data['data']['comments'])
    return comments
# comments = digikala_category_comments('notebook-netbook-ultrabook')
# db = CommentDB()
# db.create_comments_batch(comments)