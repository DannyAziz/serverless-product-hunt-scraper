from chalice import Chalice
from requests_html import HTMLSession

app = Chalice(app_name='producthunt-scraper')


@app.route("/product-hunt/top-product")
def get_top_product_product_hunt():
    session = HTMLSession()
    url = 'https://www.producthunt.com/'
    resp = session.get(url)

    product_list_containers = resp.html.find(".postsList_b2208")

    if len(product_list_containers) == 1:
        product_list = product_list_containers[0]
    else:
        product_list = product_list_containers[1]

    if product_list:
        top_product = product_list.find("li")[0]
        product_obj = {
            "name": top_product.find(".content_31491", first=True).find("h3", first=True).text,
            "url": "https://producthunt.com{url}".format(url=top_product.find("a", first=True).attrs["href"]),
            "description": top_product.find(".content_31491", first=True).find("p", first=True).text,
            "upvote_count": top_product.find(".voteButtonWrap_4c515", first=True).text,

        }
        return product_obj
    else:
        return {"error": "Product List Element Not Found"}


