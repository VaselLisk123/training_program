from cmath import isnan
import shopify
from exceptions import CantCreateProduct, CantCreateVariant
import download_images_dropbox as dbox
import pandas as pd

def create_product_sheet_1(row,value):
    check_sku = row[value.get("CentreSoft Code")]
    if pd.isna(check_sku):
        raise CantCreateProduct
    new_product = shopify.Product({
        "title": "Default Title",
        "product_type": str(row[value.get("Type")]),
        "vendor": str(row[value.get("Vendor")]),
        "tags": str(row[value.get("Tag")]),
    })
    new_product.save()
    return new_product

def create_product_sheet_7(row,value):
    check_sku = row[value.get("CentreSoft Code")]
    if pd.isna(check_sku):
        raise CantCreateProduct
    new_product = shopify.Product({
            "title": str(row[value.get("Title")]),
            "body_html": str(row[value.get("Description")])+f"<br>{str(row[value.get('Features')])}</br>",
            "vendor": str(row[value.get("Vendor")]),
        })
    new_product.save()
    return new_product

def create_product_variant_sheet_1(row,product,value):
    check_weight = row[value.get("Weight")] 
    product_variants = product.variants
    for variant in product_variants:
        variant.barcode = str(row[value.get("Barcode")])
        variant.sku = str(row[value.get("CentreSoft Code")])
        variant.price = str(row[value.get("Price")])
        variant.compare_at_price = str(row[value.get("Compare Price")])
        variant.weight = row[value.get("Weight")]
        variant.iventory_management = "shopify"
        variant.option1 = "Title"
    try:
        float(check_weight)
    except ValueError:
        variant.weight = 0
    variant.save()
    return variant

def create_product_variant_sheet_7(row,product,value):
    check_weight = row[value.get("Weight")] 
    product_variants = product.variants
    for variant in product_variants:
        variant.barcode = str(row[value.get("Barcode")])
        variant.sku = str(row[value.get("CentreSoft Code")])    
        variant.price = str(row[value.get("Price")])
        variant.compare_at_price = str(row[value.get("Compare Price")])
        variant.weight = str(row[value.get("Weight")])
        variant.inventory_management = "shopify"
        variant.option1 = "Title"
    try:
        float(check_weight)
    except ValueError:
       variant.weight = 0
    variant.save()
    return variant

def update_product_metafields(row,product,value):
    product = shopify.Product.find(product.id)
    for key in value.get("metafield_keys"):
        product_metafield = shopify.Metafield({
            "namespace": f"trm_{(key.replace(' ','')).lower()}",
            "key": key,
            "value": str(row[key]),
            "type": "string",
        })
        product.add_metafield(product_metafield)

def update_product_inventory_sheet_1(variant_instance,row,value,location_id):
    inventory_item_id = variant_instance.inventory_item_id
    inventory_item = shopify.InventoryItem.find(inventory_item_id)
    inventory_item.harmonized_system_code = str(row[value.get("Commodity Code")]).strip()
    inventory_item.save()
    shopify.InventoryLevel.set(location_id=location_id, inventory_item_id=inventory_item_id, available=row[value.get("Carton Quantity")])

def update_product_inventory_sheet_7(variant_instance,row,value,location_id):
    inventory_item_id = variant_instance.inventory_item_id
    inventory_item = shopify.InventoryItem.find(inventory_item_id)
    inventory_item.harmonized_system_code = str(row[value.get("Commodity Code")]).strip()
    inventory_item.country_code_of_origin = str(row[value.get("Country Code")])
    inventory_item.save()
    shopify.InventoryLevel.set(location_id=location_id, inventory_item_id=inventory_item_id, available=row[value.get("Carton Quantity")])

def update_product_image_sheet_1(row,value,product):
    image = shopify.Image.create({
        "product_id": product.id,
        "src": str(row[value.get("Image Url")])
    })

def update_product_image_sheet_7(row,value,product):
    dbox.download_file_dropbox(row)
    list_of_images = dbox.get_images(row)
    for image in list_of_images:
        new_image = shopify.Image({
            "product_id": product.id,
        })
        with open(image,"rb") as f:
            encoded = f.read()
        new_image.attach_image(encoded,image)
        new_image.save()

def update_product(variant_instance,row,value,location_id):
    variant_instance.price = str(row[value.get("Price")])
    inventory_item = variant_instance.inventory_item_id
    shopify.InventoryLevel.set(location_id=location_id, inventory_item_id=inventory_item, available=row[value.get("Carton Quantity")],disconnect_if_necessary=False)

