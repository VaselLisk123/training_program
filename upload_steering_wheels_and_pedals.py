from turtle import down
from numpy import product
import pandas as pd
import config
import shopify
from exceptions import CantCreateVariant
import requests

def if_variant(variants,check_sku):
    for variant in variants:
        if variant.sku == check_sku:
            return variant
    return None

def get_url_image_dropbox(row):
    downloaded_file = requests.get(str(row["Asset Link"]))
    file_dest = open("D:\\Piton\\training_program\\downloaded_images\\images.zip","wb")
    file_dest.write(downloaded_file.content)

def update_product_inventory(variant_instance,row,location_id):
    inventory_item_id = variant_instance.inventory_item_id
    inventory_item = shopify.InventoryItem.find(inventory_item_id)
    inventory_item.harmonized_system_code = str(row["Commodity Code"]).strip()
    inventory_item.save()
    shopify.InventoryLevel.set(location_id=location_id, inventory_item_id=inventory_item_id, available=row["Carton Quantity"])

def update_product_metafields(row,product_id):
    product = shopify.Product.find(product_id)
    metafield_keys = ["Model","Wheel Diameter","Wheel Rotation","Compatibility","HGHTA (CMS)","WDTHA (CMS)","LGTHA (CMS)"]
    for key in metafield_keys:
        product_metafield = shopify.Metafield({
            "namespace": f"trm_{(key.replace(' ','')).lower()}",
            "key": key,
            "value": str(row[key]),
            "type": "string",
        })
        product.add_metafield(product_metafield)

def new_product_with_variant(row):
    new_product = shopify.Product.create({
        "title": str(row["Name"]),
        "body_html": str(row["Product Description"])+f"<br>{str(row['Features'])}</br>",
        "vendor": str(row["Brand"]),
    })
    new_variant = shopify.Variant.create({
        "product_id": new_product.id,
        "barcode": str(row["Barcode"]),
        "sku": str(row["CentreSoft Code"]),
        "price": str(row["Trade (Inc VAT)"]),
        "compare_at_price": str(row["RRP"]),
        "weight": str(row["WGHTA (KG)"]),
        "option1": "Title"
    })
    if new_variant.exists(new_variant.id):
        return new_variant
    else:
        raise CantCreateVariant

def update_product(variant_instance,row,location_id):
    variant_instance.price = str(row["Trade (Inc VAT)"])
    inventory_item = variant_instance.inventory_item_id
    shopify.InventoryLevel.set(location_id=location_id, inventory_item_id=inventory_item, available=row["Carton Quantity"])

def create_product(row,location_id):
    try:
        variant = new_product_with_variant(row)
    except CantCreateVariant:
        #Запись в лог
        return None 
    product_id = variant.product_id
    update_product_inventory(variant,row,location_id)
    get_url_image_dropbox(row)
    update_product_metafields(row,product_id)

def upload_products(excel_info):
    all_variants = shopify.Variant.find()
    for i,row in excel_info.iterrows():
        check_sku = (str(row["CentreSoft Code"]))
        current_variant = if_variant(all_variants,check_sku)
        if not current_variant:
            create_product(row,default_location_id)
        else:
            variant = shopify.Variant.find(current_variant.id)
            update_product(variant,row,default_location_id)

file_reader = pd.read_excel(config.DOWNLOADED_FILE_NEW_PATH,sheet_name="Steering Wheels & Pedals",skiprows=1)          
api_version = "2022-04"
session = shopify.Session(config.SHOP_URL, api_version,"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")
shopify.ShopifyResource.activate_session(session)
default_location_id = shopify.Shop.current().primary_location_id
upload_products(file_reader)
shopify.ShopifyResource.clear_session()