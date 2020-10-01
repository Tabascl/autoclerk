class AvailabilityEvent:
    def __init__(self, old_value, update_product):
        self.payload = {
            "username": "Verfügbarkeitsupdate",
            "content": "**{}** für {}\n(alter Wert: {})\nZum Preis von {:.2f}€".format(update_product.availability, update_product.name, old_value, update_product.price),
            "embeds": [
                {
                    "title": "{}".format(update_product.shop),
                    "url": update_product.product_link
                }
            ]
        }


class PriceEvent:
    def __init__(self, old_value, update_product, is_new_lowest):
        if is_new_lowest:
            username = "Neuer Tiefpreis"
        else:
            username = "Preisupdate"

        self.payload = {
            "username": username,
            "content": "**{:.2f}€** für {}\n(alter Wert: {:.2f}€)".format(update_product.price, update_product.name, old_value),
            "embeds": [
                {
                    "title": "{}".format(update_product.shop),
                    "url": update_product.product_link
                }
            ]
        }


class InsertEvent:
    def __init__(self, update_product):
        self.payload = {
            "username": "Neues Produkt",
            "content": "**{}** für **{:.2f}€**\n{}".format(update_product.name, update_product.price, update_product.availability),
            "embeds": [
                {
                    "title": "{}".format(update_product.shop),
                    "url": update_product.product_link
                }
            ]
        }
