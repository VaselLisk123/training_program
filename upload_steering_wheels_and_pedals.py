from numpy import imag
import pandas as pd
import config
import shopify
from exceptions import CantCreateVariant
import download_images_dropbox as dbox

def if_variant(variants,check_sku):
    for variant in variants:
        if variant.sku == check_sku:
            return variant
    return None

def update_product_images(row,product_id):
    dbox.download_file_dropbox(row)
    list_of_images = dbox.get_images(row)
    for image in list_of_images:
        new_image = shopify.Image({
            "product_id": product_id,
        })
        with open(image,"rb") as f:
            encoded = f.read()
        new_image.attach_image(encoded,image)
        new_image.save()
    
def update_product_inventory(variant_instance,row,location_id):
    inventory_item_id = variant_instance.inventory_item_id
    inventory_item = shopify.InventoryItem.find(inventory_item_id)
    inventory_item.harmonized_system_code = str(row["Commodity Code"]).strip()
    inventory_item.save()
    shopify.InventoryLevel.set(location_id=location_id, inventory_item_id=inventory_item_id, available=row["Carton Quantity"])

def update_product_metafields(row,product_id):
    product = shopify.Product.find(product_id)
    metafield_keys = ["Model","Wheel Diameter","Wheel Rotation","HGHTA (CMS)","WDTHA (CMS)","LGTHA (CMS)"]
    for key in metafield_keys:
        product_metafield = shopify.Metafield({
            "namespace": f"trm_{(key.replace(' ','')).lower()}",
            "key": key,
            "value": str(row[key]),
            "type": "string",
        })
        product.add_metafield(product_metafield)

def new_product_with_variant(row):
    check_sku = row["CentreSoft Code"]
    check_weight = row["WGHTA (KG)"]
    if type(check_sku) == str:
        new_product = shopify.Product.create({
            "title": str(row["Name"]),
            "body_html": str(row["Product Description"])+f"<br>{str(row['Features'])}</br>",
            "vendor": str(row["Brand"]),
        })
        if type(check_weight) == float:
            new_variant = shopify.Variant.create({
                "product_id": new_product.id,
                "barcode": str(row["Barcode"]),
                "sku": str(row["CentreSoft Code"]),
                "price": str(row["Trade (Inc VAT)"]),
                "compare_at_price": str(row["RRP"]),
                "weight": str(row["WGHTA (KG)"]),
                "option1": "Title"
            })
        else:
            new_variant = shopify.Variant.create({
                "product_id": new_product.id,
                "barcode": str(row["Barcode"]),
                "sku": str(row["CentreSoft Code"]),
                "price": str(row["Trade (Inc VAT)"]),
                "compare_at_price": str(row["RRP"]),
                "weight": 0,
                "option1": "Title"
            })
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
    update_product_images(row,product_id)
    update_product_metafields(row,product_id)

def upload_products(excel_info):
    all_variants = shopify.Variant.find()
    for i,row in excel_info.iterrows():
        check_sku = (str(row["CentreSoft Code"]))
        current_variant = if_variant(all_variants,check_sku)
        if current_variant:
            variant = shopify.Variant.find(current_variant.id)
            update_product(variant,row,default_location_id)
        else:
            create_product(row,default_location_id)

file_reader = pd.read_excel(config.DOWNLOADED_FILE_NEW_PATH,sheet_name="Steering Wheels & Pedals",skiprows=1)          
api_version = "2022-04"
session = shopify.Session(config.SHOP_URL, api_version,"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")
shopify.ShopifyResource.activate_session(session)
default_location_id = shopify.Shop.current().primary_location_id
upload_products(file_reader)
shopify.ShopifyResource.clear_session()