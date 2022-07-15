import pandas as pd
import config
import shopify

def product_exists(check_sku,variants):
    variant_sku = []
    for variant in variants:
        if (variant.sku == ""):
            continue
        variant_sku.append(variant.sku)
    for variant in variant_sku:
        if variant == check_sku:
            return True
        elif variant != check_sku:
            return False

            

def create_product(excel_info):
    metafield_keys = ["Platform","Product","HGHTA (CMS)","WDTHA (CMS)","LGTHA (CMS)","RELEASE_DATE"]
    var = shopify.Variant.find()
    for i,row in excel_info.iterrows():
        check_sku = (str(row["CentreSoft Code"]))
        if product_exists(check_sku,var) == False:
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
            "price": str(row["Trade (Inc Vat)"]),
            "compare_at_price": str(row["RRP#T"]),
            "weight": row["WGHTA (KG)"],
            "option1": "Title",
            })
            inventory_item = new_product.inventory_item_id
            default_location_id = shopify.Shop.current().primary_location_id
            shopify.InventoryLevel.set(
                location_id=default_location_id,
                inventory_item_id=inventory_item,
                available=row["Carton Qty"],
            )       
            for key in metafield_keys:
                product_metafield = shopify.Metafield({
                    "key": key,
                    "value": str(row[key]),
                    "type": "string",
                    "namespace": "trm_test",
                })
                new_product.add_metafield(product_metafield)
                new_product.save()
        else:
            print("updated")

file_reader = pd.read_excel(config.DOWNLOADED_FILE_NEW_PATH,sheet_name="Brand & Category",skiprows=6)          
api_version = "2022-04"
session = shopify.Session(config.SHOP_URL, api_version,"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")
shopify.ShopifyResource.activate_session(session)
create_product(file_reader)
shopify.ShopifyResource.clear_session()