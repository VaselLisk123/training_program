import pandas as pd
import config
import shopify

def sku_filter(variants):
        for variant in variants:
            variant_sku = variant.sku
            if variant_sku == "":
                return variant


def product_exists(check_sku,variants):
        for variant in variants:
                if variant.sku == check_sku:
                    variants.remove(variant)
                    return variant.id
                else:
                    return False
            

def create_product(excel_info):
    metafield_keys = ["Platform","Product","HGHTA (CMS)","WDTHA (CMS)","LGTHA (CMS)","RELEASE_DATE"]
    var = shopify.Variant.find()
    for i,row in excel_info.iterrows():
        check_sku = (str(row["CentreSoft Code"]))
        blank_sku = sku_filter(var)
        if len(var) != 0:
            if blank_sku != None:
                var.remove(blank_sku)
            variant_id = product_exists(check_sku,var)
            if variant_id != False:
                variant = shopify.Variant.find(variant_id)
                variant_existance = shopify.Variant.exists(variant.id)
            else:
                variant_existance = False
        else:
            variant_existance = False
        if variant_existance == False:
            new_product = shopify.Product.create({
            "title": "Default Title",
            "product_type": str(row["Product Type"]),
            "vendor": str(row["Brand"]),
            "tags": str(row["Category"]),
            })
            current_product_id = new_product.get_id()
            new_product = shopify.Variant.create({
            "product_id": current_product_id,
            "barcode": str(row["Barcode"]),
            "sku": str(row["CentreSoft Code"]),
            "price": str(row["Trade (Inc Vat)"]),
            "compare_at_price": str(row["RRP#T"]),
            "weight": row["WGHTA (KG)"],
            "option1": "Title",
            })
            inventory_item_id = new_product.inventory_item_id
            inventory_item = shopify.InventoryItem.find(inventory_item_id)
            inventory_item.harmonized_system_code = str(row["Commodity Code"]).strip()
            inventory_item.country_code_of_origin = str(row["Country Code"])
            inventory_item.save()
            default_location_id = shopify.Shop.current().primary_location_id
            shopify.InventoryLevel.set(
                location_id=default_location_id,
                inventory_item_id=inventory_item_id,
                available=row["Carton Qty"],
            )
            image = shopify.Image.create({
            "product_id": current_product_id,
            "src": str(row["IMAGE_URL"])
            })
            for key in metafield_keys:
                product_metafield = shopify.Metafield.create({
                    "namespace": "trm_test",
                    "key": key,
                    "value": str(row[key]),
                    "type": "string",
                })
        else:
            variant.price = str(row["Trade (Inc Vat)"])
            inventory_item = variant.inventory_item_id
            id_location = shopify.Shop.current().primary_location_id
            shopify.InventoryLevel.set(location_id=id_location,inventory_item_id=inventory_item,available=row["Carton Qty"])
           
            

file_reader = pd.read_excel(config.DOWNLOADED_FILE_NEW_PATH,sheet_name="Brand & Category",skiprows=6)          
api_version = "2022-04"
session = shopify.Session(config.SHOP_URL, api_version,"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")
shopify.ShopifyResource.activate_session(session)
create_product(file_reader)
shopify.ShopifyResource.clear_session()