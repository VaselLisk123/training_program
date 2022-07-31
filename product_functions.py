from logging import warning
from requests import head
import shopify
from exceptions import CantCreateProduct, CantCreateVariant
import download_images_dropbox as dbox
import pandas as pd
import log

logger = log.create_logger()

def create_product_sheet_1(line_number,row,value,check_sku,header): # Brands & Category
    if pd.isna(check_sku):
        raise CantCreateProduct
    new_product = shopify.Product({
        "title": value.get("Title"),
        "product_type": str(row[value.get("Type")]),
        "vendor": str(row[value.get("Vendor")]),
        "tags": str(row[value.get("Tag")]),
    })
    new_product.save()
    logger.info(f"Product successfully created from [Sheet: {header}, Line: {line_number}]")
    return new_product

def create_product_sheet_2(line_number,row,value,check_sku,header): # Recommended Range Selection
    if pd.isna(check_sku):
        raise CantCreateProduct
    new_product = shopify.Product({
        "title": str(row[value.get("Title")]),
        "tags": str(row[value.get("Tag")]),
        "body_html": str(row[value.get("Description")]),
    })
    new_product.save()
    logger.info(f"Product successfully created from [Sheet: {header}, Line: {line_number}]")
    return new_product

def create_product_sheet_3(line_number,row,value,check_sku,header): # Peripherals (Top sellers)
    if pd.isna(check_sku):
        raise CantCreateProduct
    new_product = shopify.Product({
        "title": str(row[value.get("Title")]),
        "vendor": str(row[value.get("Vendor")]),
    })
    new_product.save()
    logger.info(f"Product successfully created from [Sheet: {header}, Line: {line_number}]")
    return new_product

def create_product_sheet_4(line_number,row,value,check_sku,header): # Steering Wheels & Pedals
    if pd.isna(check_sku):
        raise CantCreateProduct
    new_product = shopify.Product({
        "title": str(row[value.get("Title")]),
        "body_html": str(row[value.get("Description")])+f"<br>{str(row[value.get('Features')])}</br>",
        "vendor": str(row[value.get("Vendor")]),
    })
    new_product.save()
    logger.info(f"Product successfully created from [Sheet: {header}, Line: {line_number}]")
    return new_product

def create_product_sheet_5(line_number,row,value,check_sku,header): # Gaming Chairs
    if pd.isna(check_sku):
        raise CantCreateProduct
    new_product = shopify.Product({
        "title": str(row[value.get("Title")]),
        "body_html": str(row[value.get("Description")])+f"<br>{str(row[value.get('Features')])}</br>",
        "vendor": str(row[value.get("Vendor")]),
    })
    new_product.save()
    logger.info(f"Product successfully created from [Sheet: {header}, Line: {line_number}]")
    return new_product

def create_product_sheet_6(line_number,row,value,check_sku,header): # Cable Guys
    if pd.isna(check_sku):
        raise CantCreateProduct
    new_product = shopify.Product({
        "title": str(row[value.get("Title")]),
        "body_html": str(row[value.get("Description")])+f"<br>{str(row[value.get('Features1')])}</br>"+f"<br>{str(row[value.get('Features2')])}</br>"+f"<br>{str(row[value.get('Features3')])}</br>",
        "vendor": str(row[value.get("Vendor")]),
    })
    new_product.save()
    logger.info(f"Product successfully created from [Sheet: {header}, Line: {line_number}]")
    return new_product

def create_product_sheet_7(line_number,row,value,check_sku,header): # Switch Hardware
    if pd.isna(check_sku):
        raise CantCreateProduct
    new_product = shopify.Product({
        "title": str(row[value.get("Title")]),
        "body_html": str(row[value.get("Description")]),
        "product_type": str(row[value.get("Type")]),
    })
    new_product.save()
    logger.info(f"Product successfully created from [Sheet: {header}, Line: {line_number}]")
    return new_product

def create_product_variant_sheet_1(row,product,value,header,line_number):
    product_variants = product.variants
    for variant in product_variants:
        variant.barcode = str(row[value.get("Barcode")])
        variant.sku = str(row[value.get("CentreSoft Code")])
        variant.price = str(row[value.get("Price")])
        variant.compare_at_price = str(row[value.get("Compare Price")])
        variant.weight = row[value.get("Weight")]
        variant.inventory_management = "shopify"
        variant.option1 = "Title"
    try:
        float(variant.weight)
    except ValueError:
        logger.warning(f"Variant [Sheet: {header}, Line: {line_number}] weight changed to 0 cause weight: {row[value.get('Weight')]}")
        variant.weight = 0
    variant.save()
    return variant

def create_product_variant_sheet_2(row,product,value,header,line_number):
    product_variants = product.variants
    for variant in product_variants:
        variant.barcode = int(row[value.get("Barcode")])
        variant.sku = str(row[value.get("CentreSoft Code")])
        variant.price = str(row[value.get("Price")])
        variant.weight = row[value.get("Weight")]
        variant.inventory_management = "shopify"
        variant.option1 = "Title"
    try:
        float(variant.weight)
    except ValueError:
        logger.warning(f"Variant [Sheet: {header}, Line: {line_number}] weight changed to 0 cause weight has invalid record type: {row[value.get('Weight')]}")
        variant.weight = 0
    variant.save()
    return variant

def create_product_variant_sheet_3(row,product,value,header,line_number):
    product_variants = product.variants
    for variant in product_variants:
        variant.barcode = int(row[value.get("Barcode")])
        variant.sku = str(row[value.get("CentreSoft Code")])
        variant.price = str(row[value.get("Price")])
        variant.compare_at_price = str(row[value.get("Compare Price")])
        variant.inventory_management = "shopify"
        variant.option1 = "Title"
        variant.save()
    return variant

def create_product_variant_sheet_4(row,product,value,header,line_number):
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
        float(variant.weight)
    except ValueError:
        logger.warning(f"Variant [Sheet: {header}, Line: {line_number}] weight changed to 0 cause weight has invalid record type: {row[value.get('Weight')]}")
        variant.weight = 0
    variant.save()
    return variant

def create_product_variant_sheet_5(row,product,value,header,line_number):
    product_variants = product.variants
    for variant in product_variants:
        variant.barcode = str(row[value.get("Barcode")])
        variant.sku = str(row[value.get("CentreSoft Code")])
        variant.price = str(row[value.get("Price")])
        variant.compare_at_price = str(row[value.get("Compare Price")])
        variant.weight = row[value.get("Weight")]
        variant.inventory_management = "shopify"
        variant.option1 = "Title"
    try:
        float(variant.weight)
    except ValueError:
        logger.warning(f"Variant [Sheet: {header}, Line: {line_number}] weight changed to 0 cause weight has invalid record type: {row[value.get('Weight')]}")
        variant.weight = 0
    variant.save()
    return variant

def create_product_variant_sheet_6(row,product,value,header,line_number):
    product_variants = product.variants
    for variant in product_variants:
        variant.barcode = int(row[value.get("Barcode")])
        variant.sku = str(row[value.get("CentreSoft Code")])
        variant.price = str(row[value.get("Price")])
        variant.compare_at_price = str(row[value.get("Compare Price")])
        variant.inventory_management = "shopify"
        variant.option1 = "Title"
    variant.save()
    return variant

def create_product_variant_sheet_7(row,product,value,header,line_number):
    product_variants = product.variants
    for variant in product_variants:
        variant.barcode = str(row[value.get("Barcode")])
        variant.sku = str(row[value.get("CentreSoft Code")])
        variant.price = str(row[value.get("Price")])
        variant.weight = row[value.get("Weight")]
        variant.inventory_management = "shopify"
        variant.option1 = "Title"
    try:
        float(variant.weight)
    except ValueError:
        logger.warning(f"Variant [Sheet: {header}, Line: {line_number}] weight changed to 0 cause weight has invalid record type: {row[value.get('Weight')]}")
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

def update_product_metafields_is_empty(row,product,value):
    pass

def update_product_inventory_sheet_1(variant_instance,row,value,location_id):
    inventory_item_id = variant_instance.inventory_item_id
    inventory_item = shopify.InventoryItem.find(inventory_item_id)
    inventory_item.harmonized_system_code = str(row[value.get("Commodity Code")]).strip()
    inventory_item.country_code_of_origin = str(row[value.get("Country Code")])
    inventory_item.save()
    shopify.InventoryLevel.set(location_id=location_id, inventory_item_id=inventory_item_id, available=row[value.get("Carton Quantity")])

def update_product_inventory_sheet_2(variant_instance,row,value,location_id):
    inventory_item_id = variant_instance.inventory_item_id
    shopify.InventoryLevel.set(location_id=location_id, inventory_item_id=inventory_item_id, available=int(row[value.get("Carton Quantity")]))

def update_product_inventory_sheet_is_empty(variant_instance,row,value,location_id):
    pass

def update_product_inventory_sheet_4(variant_instance,row,value,location_id):
    inventory_item_id = variant_instance.inventory_item_id
    inventory_item = shopify.InventoryItem.find(inventory_item_id)
    inventory_item.harmonized_system_code = str(row[value.get("Commodity Code")]).strip()
    inventory_item.country_code_of_origin = str(row[value.get("Country of Origin")])
    inventory_item.save()
    shopify.InventoryLevel.set(location_id=location_id, inventory_item_id=inventory_item_id, available=int(row[value.get("Carton Quantity")]))

def update_product_inventory_sheet_7(variant_instance,row,value,location_id):
    inventory_item_id = variant_instance.inventory_item_id
    inventory_item = shopify.InventoryItem.find(inventory_item_id)
    inventory_item.harmonized_system_code = str(row[value.get("Commodity Code")]).strip()
    inventory_item.country_code_of_origin = str(row[value.get("Country Code")])
    inventory_item.save()

def update_product_image_sheet_1(row,value,product):
    image = shopify.Image.create({
        "product_id": product.id,
        "src": str(row[value.get("Image Url")])
    })

def update_product_image_is_empty(row,value,product):
    pass

def update_product_image_dropbox(row,value,product):
    dbox.download_file_dropbox(row,value)
    list_of_images = dbox.get_images(row,value)
    for image in list_of_images:
        new_image = shopify.Image({
            "product_id": product.id,
        })
        with open(image,"rb") as f:
            encoded = f.read()
        new_image.attach_image(encoded,image)
        new_image.save()

def update_product(variant_instance,location_id,variant_price_quantity,header,line_number):
    try:
        price,quantity = variant_price_quantity.get(variant_instance.sku).values()
    except AttributeError:
        logger.warning(f"Product not found by sku: {variant_instance.sku}")
        return None
    if variant_instance.price != price:
        variant_instance.price = price
        variant_instance.save()
    if variant_instance.inventory_quantity != quantity:
        inventory_item = variant_instance.inventory_item_id
        shopify.InventoryLevel.set(location_id=location_id, inventory_item_id=inventory_item, available=quantity)
    else:
        pass
    logger.warning(f"Product [Sheet: {header}, Line: {line_number}] successfully updated")
