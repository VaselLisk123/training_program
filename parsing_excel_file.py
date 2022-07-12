import pandas as pd
import config
import shopify

def create_product():
    metafield_keys = ["Platform","Product","HGHTA (CMS)","WDTHA (CMS)","LGTHA (CMS)","RELEASE_DATE"]
    file_reader = pd.read_excel(config.DOWNLOADED_FILE_NEW_PATH,sheet_name="Brand & Category",skiprows=6)
    for i,row in file_reader.iterrows():
        new_product = shopify.Product.create({
            "title": "test",
            "product_type": str(row["Product Type"]),
            "vendor": str(row["Brand"]),
            "tags": str(row["Category"]),
            "inventory_quantity": row["Carton Qty"],
            "compare_at_price": row["RRP#T"],
        })
        new_product = shopify.Variant.create({
            "product_id": new_product.get_id(),
            "barcode": str(row["Barcode"]),
            "sku": str(row["CentreSoft Code"]),
            "price": str(row["Trade (Inc Vat)"]),
            "weight": row["WGHTA (KG)"],
            "option1": 1
        })
        new_product.save()
        for key in metafield_keys:
            shopify_request = shopify.Metafield({
                "key": key,
                "value": str(row[key]),
                "value_type": "string",
                "namespace": "trm_test",
            })
            new_product.add_metafield(shopify_request)
            new_product.save()  
        break
             
api_version = "2022-04"
session = shopify.Session(config.SHOP_URL, api_version,"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")
shopify.ShopifyResource.activate_session(session)
create_product()
shopify.ShopifyResource.clear_session()