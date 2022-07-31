import pandas as pd
import config
import shopify
from exceptions import CantCreateProduct, CantCreateVariant
import download_images_dropbox as dbox
import product_functions
import log

sheet_fields = {
    # "Brand & Category":{
    #     "skiprows": 6,
    #     "Title": "Default Title",
    #     "Type": "Product Type",
    #     "Vendor": "Brand",
    #     "Tag": "Category",
    #     "Barcode": "Barcode",
    #     "CentreSoft Code": "CentreSoft Code",
    #     "Carton Quantity": "Carton Qty",
    #     "Price": "Trade (Inc Vat)",
    #     "Compare Price": "RRP#T",
    #     "Commodity Code": "Commodity Code",
    #     "Country Code": "Country Code",
    #     "Platform": "Platform",
    #     "Product": "Product",
    #     "Weight": "WGHTA (KG)",
    #     "Height": "HGHTA (CMS)",
    #     "Width": "WDTHA (CMS)",
    #     "Length": "LGTHA (CMS)",
    #     "Release Date": "RELEASE_DATE",
    #     "Image Url": "IMAGE_URL",
    #     "metafield_keys": ["Platform","Product","HGHTA (CMS)","WDTHA (CMS)","LGTHA (CMS)","RELEASE_DATE"],
    #     "create product": product_functions.create_product_sheet_1,
    #     "create product variant": product_functions.create_product_variant_sheet_1,
    #     "update product inventory": product_functions.update_product_inventory_sheet_1,
    #     "update product image": product_functions.update_product_image_sheet_1,
    #     "update product metafields": product_functions.update_product_metafields,
    #     "update product": product_functions.update_product,
    # },
    # "Recommended Range Selection": {
    #     "skiprows": 15,
    #     "Title": "Product Description",
    #     "Tag": "Publisher",
    #     "Description": "Product Description",
    #     "Barcode": "EAN Code",
    #     "CentreSoft Code": "CentreSoft Item Code",
    #     "Carton Quantity": "CARTON",
    #     "Price": "SRP",
    #     "Weight": "WEIGHT",
    #     "Height": "HEIGHT",
    #     "Width": "WIDTH",
    #     "Depth": "DEPTH",
    #     "Release Date": "Release Date",
    #     "metafield_keys": ["HEIGHT","WIDTH","DEPTH","Release Date"],
    #     "create product": product_functions.create_product_sheet_2,
    #     "create product variant": product_functions.create_product_variant_sheet_2,
    #     "update product inventory": product_functions.update_product_inventory_sheet_2,
    #     "update product image": product_functions.update_product_image_is_empty,
    #     "update product metafields": product_functions.update_product_metafields,
    #     "update product": product_functions.update_product,
    # },
    # "Peripherals (Top sellers)":{
    #     "skiprows": 5,
    #     "Title": "Name",
    #     "Vendor": "Brand",
    #     "Barcode": "EAN",
    #     "CentreSoft Code": "CS Code",
    #     "Price": "Trade",
    #     "Compare Price": "Trade",
    #     "create product": product_functions.create_product_sheet_3,
    #     "create product variant": product_functions.create_product_variant_sheet_3,
    #     "update product inventory": product_functions.update_product_inventory_sheet_is_empty,
    #     "update product image": product_functions.update_product_image_is_empty,
    #     "update product metafields": product_functions.update_product_metafields_is_empty,
    #     "update product": product_functions.update_product,
    # },
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
        "Country of Origin": "Country of Origin",
        "Model": "Model",
        "Wheel Diameter": "Wheel Diameter",
        "Wheel Rotation": "Wheel Rotation",
        "Weight": "WGHTA (KG)",
        "Height": "HGHTA (CMS)",
        "Width": "WDTHA (CMS)",
        "Length": "LGTHA (CMS)",
        "Asset Link": "Asset Link",
        "metafield_keys": ["Model","Wheel Diameter","Wheel Rotation","HGHTA (CMS)","WDTHA (CMS)","LGTHA (CMS)"],
        "create product": product_functions.create_product_sheet_4,
        "create product variant": product_functions.create_product_variant_sheet_4,
        "update product inventory": product_functions.update_product_inventory_sheet_4,
        "update product image": product_functions.update_product_image_dropbox,
        "update product metafields": product_functions.update_product_metafields,
        "update product": product_functions.update_product,
    },
    "Gaming Chairs": {
        "skiprows": 0,
        "Title": "Description",
        "Vendor": "Vendor",
        "Description": "Description",
        "Features": "Features",
        "Barcode": "Barcode",
        "CentreSoft Code": "Itemcode",
        "Price": "Unit Trade",
        "Compare Price": "SRP",
        "Carton Quantity": "CARTON_QTY",
        "Weight": "WEIGHT",
        "Commodity Code": "COMMODITY CODE",
        "Country of Origin": "COUNTRY OF ORIGIN",
        "Height": "HEIGHT",
        "Width": "WIDTH",
        "Depth": "DEPTH",
        "Asset Link": "Assets",
        "metafield_keys": ["HEIGHT","WIDTH","DEPTH"],
        "create product": product_functions.create_product_sheet_5,
        "create product variant": product_functions.create_product_variant_sheet_5,
        "update product inventory": product_functions.update_product_inventory_sheet_4,
        "update product image": product_functions.update_product_image_is_empty,
        "update product metafields": product_functions.update_product_metafields,
        "update product": product_functions.update_product,
    },
    "Cable Guys": {
        "skiprows": 5,
        "Title": "Product",
        "Vendor": "Brand",
        "Description": "Bullet Point 1",
        "Features1": "Bullet Point 2",
        "Features2": "Bullet Point 3",
        "Features3": "Bullet Point 4",
        "Barcode": "Barcode",
        "CentreSoft Code": "CentreSoft Code",
        "Price": "Trade Price",
        "Compare Price": "RRP",
        "Carton Quantity": "Carton Qty",
        "create product": product_functions.create_product_sheet_6,
        "create product variant": product_functions.create_product_variant_sheet_6,
        "update product inventory": product_functions.update_product_inventory_sheet_2,
        "update product image": product_functions.update_product_image_is_empty,
        "update product metafields": product_functions.update_product_metafields_is_empty,
        "update product": product_functions.update_product,
    },
    "Switch Hardware": {
        "skiprows": 0,
        "Title": "Product Description",
        "Description": "Product Description",
        "Type": "COMDESC",
        "Barcode": "Barcode",
        "CentreSoft Code": "Advantage Code",
        "Price": "Trade (Ex VAT)",
        "Weight": "WEIGHT",
        "Commodity Code": "COMMODITY_CODE",
        "Country Code": "CNTRYCODE",
        "Height": "HEIGHT",
        "Width": "WIDTH",
        "Depth": "DEPTH",
        "metafield_keys": ["HEIGHT","WIDTH","DEPTH"],
        "create product": product_functions.create_product_sheet_7,
        "create product variant": product_functions.create_product_variant_sheet_7,
        "update product inventory": product_functions.update_product_inventory_sheet_7,
        "update product image": product_functions.update_product_image_is_empty,
        "update product metafields": product_functions.update_product_metafields,
        "update product": product_functions.update_product,   
    },
}
variant_price_quantity = {}
logger = log.create_logger()

def fulfill_variant_price_quantity(stock_excel):
    global variant_price_quantity
    for i,row in stock_excel.iterrows():
        variant_price_quantity.update({
            row["ITEML"]: {
                "price": row["TRADE"],
                "quantity": row["CARTON QTY"]
            }
        })

def if_variant(variants,check_sku):
    for variant in variants:
        if variant.sku == check_sku:
            return variant
    return None

def create_product(line_number,row,value,header,location_id,check_sku):
    try:
        product = value.get("create product")(line_number,row,value,check_sku,header)
    except CantCreateProduct:
        logger.warning(f"Product [Sheet: {header}, Line: {line_number}] not created due invalid SKU: {row[value.get('CentreSoft Code')]}")
        return None 
    variant = value.get("create product variant")(row,product,value,header,line_number)
    value.get("update product inventory")(variant,row,value,location_id)
    value.get("update product image")(row,value,product)
    value.get("update product metafields")(row,product,value)

def upload_products():
    all_variants = shopify.Variant.find()
    for header,value in sheet_fields.items():
        product_excel = pd.read_excel(config.DOWNLOADED_FILE_NEW_PATH,sheet_name=header,skiprows=value.get("skiprows"))  
        line_number = 1 + value.get("skiprows")
        for i,row in product_excel.iterrows():
            line_number += 1
            check_sku = (row[value.get("CentreSoft Code")])
            current_variant = if_variant(all_variants,check_sku)
            if current_variant:
                variant = shopify.Variant.find(current_variant.id)
                value.get("update product")(variant,default_location_id,variant_price_quantity,header,line_number)
            else:
                create_product(line_number,row,value,header,default_location_id,check_sku)

api_version = "2022-04"
session = shopify.Session(config.SHOP_URL, api_version,"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")
shopify.ShopifyResource.activate_session(session)
default_location_id = shopify.Shop.current().primary_location_id
stock_excel = pd.read_excel(config.STOCK_FILE_PATH,sheet_name="ALLSTK12")
fulfill_variant_price_quantity(stock_excel)
upload_products()
shopify.ShopifyResource.clear_session()