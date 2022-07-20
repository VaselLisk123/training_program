import pandas as pd
import config
import shopify

def variant_sku_empty_filter(variants,check_sku):
    for variant in variants:
        if variant.sku == check_sku:
            return variant
    return None
 
def update_product_inventory(variant_instance,row,location_id):
    inventory_item_id = variant_instance.inventory_item_id
    inventory_item = shopify.InventoryItem.find(inventory_item_id)
    inventory_item.harmonized_system_code = str(row["Commodity Code"]).strip()
    inventory_item.country_code_of_origin = str(row["Country Code"])
    inventory_item.save()
    shopify.InventoryLevel.set(location_id=location_id, inventory_item_id=inventory_item_id, available=row["Carton Qty"])

def update_product_image(row,product_id):
    image = shopify.Image.create({
    "product_id": product_id,
    "src": str(row["IMAGE_URL"])
    })

def update_product_metafields(row):
    metafield_keys = ["Platform","Product","HGHTA (CMS)","WDTHA (CMS)","LGTHA (CMS)","RELEASE_DATE"]
    for key in metafield_keys:
        product_metafield = shopify.Metafield.create({
            "namespace": "trm_test",
            "key": key,
            "value": str(row[key]),
            "type": "string",
        })

def new_product_with_variant(row):
    new_product = shopify.Product.create({
    "title": "Default Title",
    "product_type": str(row["Product Type"]),
    "vendor": str(row["Brand"]),
    "tags": str(row["Category"]),
    })
    product_id = new_product.get_id()
    new_product = shopify.Variant.create({
    "product_id": product_id,
    "barcode": str(row["Barcode"]),
    "sku": str(row["CentreSoft Code"]),
    "price": str(row["Trade (Inc Vat)"]),
    "compare_at_price": str(row["RRP#T"]),
    "weight": row["WGHTA (KG)"],
    "option1": "Title",
    })
    variant_id = new_product.get_id()
    variant = shopify.Variant.find(variant_id)
    return variant

def update_product(variant_instance,row,location_id):
    variant_instance.price = str(row["Trade (Inc Vat)"])
    inventory_item = variant_instance.inventory_item_id
    shopify.InventoryLevel.set(location_id=location_id, inventory_item_id=inventory_item, available=row["Carton Qty"])

def create_product(row,location_id):
    variant = new_product_with_variant(row)
    product_id = variant.product_id
    update_product_inventory(variant,row,location_id)
    update_product_image(row,product_id)
    update_product_metafields(row)

def upload_products(excel_info):
    all_variants = shopify.Variant.find()
    for i,row in excel_info.iterrows():
        check_sku = (str(row["CentreSoft Code"]))
        current_variant = variant_sku_empty_filter(all_variants,check_sku)
        if not current_variant:
            create_product(row,default_location_id)
        else:
            variant = shopify.Variant.find(current_variant.id)
            update_product(variant,row,default_location_id)

file_reader = pd.read_excel(config.DOWNLOADED_FILE_NEW_PATH,sheet_name="Brand & Category",skiprows=6)          
api_version = "2022-04"
session = shopify.Session(config.SHOP_URL, api_version,"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")
shopify.ShopifyResource.activate_session(session)
default_location_id = shopify.Shop.current().primary_location_id
upload_products(file_reader)
shopify.ShopifyResource.clear_session()