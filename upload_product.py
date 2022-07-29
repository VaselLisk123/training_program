import pandas as pd
import config
import shopify
from exceptions import CantCreateProduct, CantCreateVariant
import download_images_dropbox as dbox
import product_functions

sheet_fields = {
    "Brand & Category":{
        "skiprows": 6,
        "Title": "Default Title",
        "Type": "Product Type",
        "Vendor": "Brand",
        "Tag": "Category",
        "Barcode": "Barcode",
        "CentreSoft Code": "CentreSoft Code",
        "Carton Quantity": "Carton Qty",
        "Price": "Trade (Inc Vat)",
        "Compare Price": "RRP#T",
        "Commodity Code": "Commodity Code",
        "Country Code": "Country Code",
        "Platform": "Platform",
        "Product": "Product",
        "Weight": "WGHTA (KG)",
        "Height": "HGHTA (CMS)",
        "Width": "WDTHA (CMS)",
        "Length": "LGTHA (CMS)",
        "Release Date": "RELEASE_DATE",
        "Image Url": "IMAGE_URL",
        "metafield_keys": ["Platform","Product","HGHTA (CMS)","WDTHA (CMS)","LGTHA (CMS)","RELEASE_DATE"],
        "create product": product_functions.create_product_sheet_1,
        "create product variant": product_functions.create_product_variant_sheet_1,
        "update product inventory": product_functions.update_product_inventory_sheet_1,
        "update product image": product_functions.update_product_image_sheet_1,
        "update product metafields": product_functions.update_product_metafields,
        "update product": product_functions.update_product,
    },
    "Recommended Range Selection": {
        "skiprows": 15,
        "Title": "Product Description",
        "Tag": "Publisher",
        "Description": "Product Description",
        "Barcode": "EAN Code",
        "CentreSoft Code": "CentreSoft Item Code",
        "Carton Quantity": "CARTON",
        "Price": "SRP",
        "Weight": "WEIGHT",
        "Height": "HEIGHT",
        "Width": "WIDTH",
        "Depth": "DEPTH",
        "Release Date": "Release Date",
        "metafield_keys": ["HEIGHT","WIDTH","DEPTH","Release Date"],
        "create product": product_functions.create_product_sheet_2,
        "create product variant": product_functions.create_product_variant_sheet_2,
        "update product inventory": product_functions.update_product_inventory_sheet_2,
        "update product image": product_functions.update_product_image_sheet_2,
        "update product metafields": product_functions.update_product_metafields,
        "update product": product_functions.update_product,
    },
    "Steering Wheels & Pedals":{
        "skiprows": 1,
        "Title": "Name",
        "Vendor": "Brand",
        "Description": "Product Description",
        "Features": "Features",
        "Barcode": "Barcode",
        "CentreSoft Code": "CentreSoft Code",
        "Price": "Trade (Inc VAT)",
        "Compare Price": "RRP",
        "Carton Quantity": "Carton Quantity",
        "Commodity Code": "Commodity Code",
        "Country Code": "Country of Origin",
        "Model": "Model",
        "Wheel Diameter": "Wheel Diameter",
        "Wheel Rotation": "Wheel Rotation",
        "Weight": "WGHTA (KG)",
        "Height": "HGHTA (CMS)",
        "Width": "WDTHA (CMS)",
        "Length": "LGTHA (CMS)",
        "Asset Link": "Asset Link",
        "metafield_keys": ["Model","Wheel Diameter","Wheel Rotation","HGHTA (CMS)","WDTHA (CMS)","LGTHA (CMS)"],
        "create product": product_functions.create_product_sheet_7,
        "create product variant": product_functions.create_product_variant_sheet_7,
        "update product inventory": product_functions.update_product_inventory_sheet_7,
        "update product image": product_functions.update_product_image_sheet_7,
        "update product metafields": product_functions.update_product_metafields,
        "update product": product_functions.update_product,
    },
}

def if_variant(variants,check_sku):
    for variant in variants:
        if variant.sku == check_sku:
            return variant
    return None

def create_product(row,value,location_id,check_sku):
    try:
        product = value.get("create product")(row,value,check_sku)
    except CantCreateProduct:
        #Запись в лог
        return None 
    check_weight = row[value.get("Weight")] 
    variant = value.get("create product variant")(row,product,value,check_weight)
    value.get("update product inventory")(variant,row,value,location_id)
    value.get("update product image")(row,value,product)
    value.get("update product metafields")(row,product,value)

def upload_products():
    all_variants = shopify.Variant.find()
    for header,value in sheet_fields.items():
        excel_info = pd.read_excel(config.DOWNLOADED_FILE_NEW_PATH,sheet_name=header,skiprows=value.get("skiprows"))  
        for i,row in excel_info.iterrows():
            check_sku = (row[value.get("CentreSoft Code")])
            current_variant = if_variant(all_variants,check_sku)
            if current_variant:
                variant = shopify.Variant.find(current_variant.id)
                value.get("update product")(variant,row,value,default_location_id)
            else:
                create_product(row,value,default_location_id,check_sku)

api_version = "2022-04"
session = shopify.Session(config.SHOP_URL, api_version,"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")
shopify.ShopifyResource.activate_session(session)
default_location_id = shopify.Shop.current().primary_location_id
upload_products()
shopify.ShopifyResource.clear_session()