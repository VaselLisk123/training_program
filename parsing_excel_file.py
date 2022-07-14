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
        })
        new_product = shopify.Variant.create({
            "product_id": new_product.get_id(),
            "barcode": str(row["Barcode"]),
            "sku": str(row["CentreSoft Code"]),
            "inventory_quantity": row["Carton Qty"],
            "price": str(row["Trade (Inc Vat)"]),
            "compare_at_price": str(row["RRP#T"]),
            "weight": row["WGHTA (KG)"],
            "option1": "Title",
        })
        inventory_level = shopify.InventoryLevel({
            "location_id": 321321,
            "inventory_item_id": new_product.inventory_item_id,
            "relocate_if_necessary": False,
        })

        for key in metafield_keys:
            product_metafield = shopify.Metafield({
                "key": key,
                "value": str(row[key]),
                "type": "string",
                "namespace": "trm_test",
            })
            new_product.add_metafield(product_metafield)
            new_product.save()  
        break
             
api_version = "2022-04"
session = shopify.Session(config.SHOP_URL, api_version,"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")
shopify.ShopifyResource.activate_session(session)
create_product()
shopify.ShopifyResource.clear_session()