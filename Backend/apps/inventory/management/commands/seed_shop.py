"""Seed shop categories and products. python manage.py seed_shop"""
from django.core.management.base import BaseCommand
from apps.inventory.shop_models import ShopCategory, ShopProduct
from decimal import Decimal


CATALOGUE = [
    {
        "category": "Air Pressure System (APS)", "slug": "aps", "icon": "💨", "sort": 1,
        "products": [
            {"name": "APS Air Compressor Unit",          "brand": "Knorr-Bremse", "pn": "K015396",  "price": "5800", "orig": "6500", "stock": 4,  "emoji": "⚙️",  "compat": "APS,APS_COMPRESSOR",    "desc": "OEM replacement APS compressor for heavy trucks"},
            {"name": "Air Dryer Cartridge",               "brand": "WABCO",        "pn": "4324100002","price": "1200", "orig": "1400", "stock": 8,  "emoji": "🌬️", "compat": "APS,APS_DRYER",          "desc": "Complete air dryer replacement cartridge"},
            {"name": "APS Pressure Governor",             "brand": "Bosch",        "pn": "0481026043","price": "2100", "orig": None,   "stock": 3,  "emoji": "🎛️", "compat": "APS,APS_GOVERNOR",       "desc": "Pressure governor — regulates system pressure"},
            {"name": "Air Reservoir Tank 20L",            "brand": "Haldex",       "pn": "HR20L001",  "price": "3400", "orig": "3800", "stock": 2,  "emoji": "🫙",  "compat": "APS,APS_RESERVOIR",      "desc": "20-litre aluminium air reservoir"},
            {"name": "APS Control Valve",                 "brand": "Knorr-Bremse", "pn": "K019453",   "price": "1850", "orig": None,   "stock": 6,  "emoji": "🔩",  "compat": "APS,APS_VALVE",          "desc": "Air control valve for pneumatic system"},
            {"name": "APS Service Kit (Full)",            "brand": "Knorr-Bremse", "pn": "APSKIT-V2", "price": "3200", "orig": "4000", "stock": 5,  "emoji": "🧰",  "compat": "APS",                    "desc": "Complete APS service kit — compressor + dryer + valve"},
        ]
    },
    {
        "category": "Brakes", "slug": "brakes", "icon": "🛑", "sort": 2,
        "products": [
            {"name": "Front Brake Pad Set (HD)",          "brand": "Brembo",       "pn": "P85073",    "price": "950",  "orig": "1100", "stock": 12, "emoji": "🔴",  "compat": "BRAKES,BRAKE_PAD,brake_caliper", "desc": "Heavy duty front brake pads for commercial vehicles"},
            {"name": "Brake Caliper (Front Left)",        "brand": "Bosch",        "pn": "0986473974","price": "4200", "orig": "4800", "stock": 3,  "emoji": "🔧",  "compat": "BRAKES,BRAKE_CALIPER,brake_caliper", "desc": "Front left brake caliper — complete assembly"},
            {"name": "Brake Caliper (Front Right)",       "brand": "Bosch",        "pn": "0986473975","price": "4200", "orig": "4800", "stock": 3,  "emoji": "🔧",  "compat": "BRAKES,BRAKE_CALIPER,brake_caliper", "desc": "Front right brake caliper — complete assembly"},
            {"name": "Brake Disc (Vented)",               "brand": "Zimmermann",   "pn": "100330052", "price": "2800", "orig": None,   "stock": 6,  "emoji": "⭕",  "compat": "BRAKES,BRAKE_DISC",      "desc": "Vented brake disc for heavy vehicle front axle"},
            {"name": "Rear Brake Drum",                   "brand": "BPW",          "pn": "BPW-BD001", "price": "1600", "orig": "1900", "stock": 5,  "emoji": "🥁",  "compat": "BRAKES,BRAKE_DRUM",      "desc": "Rear brake drum — compatible with standard axles"},
        ]
    },
    {
        "category": "Engine & Drivetrain", "slug": "engine", "icon": "⚙️", "sort": 3,
        "products": [
            {"name": "Turbocharger Assembly (HD)",        "brand": "Garrett",      "pn": "GTB2256VK", "price": "18500","orig": "21000","stock": 1,  "emoji": "🌪️", "compat": "ENGINE,ENGINE_TURBO,engine", "desc": "High-performance turbocharger for heavy diesel engines"},
            {"name": "Engine Oil Filter",                 "brand": "Mann-Filter",  "pn": "W11102/14", "price": "380",  "orig": None,   "stock": 20, "emoji": "🛢️", "compat": "ENGINE,engine",           "desc": "Heavy duty engine oil filter"},
            {"name": "Fuel Injector Set (6-cylinder)",    "brand": "Bosch",        "pn": "0432193635","price": "12400","orig": "14000","stock": 2,  "emoji": "💉",  "compat": "FUEL,ENGINE,engine",      "desc": "Complete 6-cylinder fuel injector set"},
            {"name": "Radiator Core Assembly",            "brand": "Nippondenso",  "pn": "NRD-002",   "price": "6800", "orig": "7500", "stock": 2,  "emoji": "🌡️", "compat": "ENGINE,ENGINE_COOLING,engine", "desc": "Aluminium radiator core — engine cooling system"},
            {"name": "Engine Air Filter",                 "brand": "Donaldson",    "pn": "P546555",   "price": "650",  "orig": None,   "stock": 15, "emoji": "🌀",  "compat": "ENGINE,engine",           "desc": "Heavy duty engine air filter"},
        ]
    },
    {
        "category": "Suspension & Axle", "slug": "suspension", "icon": "🔩", "sort": 4,
        "products": [
            {"name": "Shock Absorber Set (Front)",        "brand": "Gabriel",      "pn": "G57008",    "price": "3600", "orig": "4200", "stock": 4,  "emoji": "〰️", "compat": "SUSPENSION,suspension",   "desc": "Front shock absorber pair for heavy vehicles"},
            {"name": "Leaf Spring Pack",                  "brand": "Hendrickson",  "pn": "LSP-HD-04", "price": "5200", "orig": None,   "stock": 3,  "emoji": "🌿",  "compat": "SUSPENSION,SUSPENSION_LEAF_SPRING,suspension", "desc": "Heavy duty leaf spring pack — rear axle"},
            {"name": "Differential Seal Kit",             "brand": "SKF",          "pn": "VKJP9122",  "price": "1800", "orig": "2100", "stock": 6,  "emoji": "🔄",  "compat": "AXLE,AXLE_DIFF,suspension", "desc": "Complete differential seal and gasket kit"},
            {"name": "Wheel Bearing Hub Assembly",        "brand": "FAG",          "pn": "713630930",  "price": "4500", "orig": "5000", "stock": 4,  "emoji": "⭕",  "compat": "AXLE,TYRES,wheels,suspension", "desc": "Complete wheel bearing hub — includes ABS ring"},
        ]
    },
    {
        "category": "Tyres & Wheels", "slug": "tyres", "icon": "🔵", "sort": 5,
        "products": [
            {"name": "Apollo EnduRace HA 10.00R20",       "brand": "Apollo",       "pn": "AE-HA-1020","price": "7800", "orig": "8500", "stock": 8,  "emoji": "⬛",  "compat": "TYRES,TYRE_FRONT,tyres",  "desc": "Long-haul highway tyre for front axle"},
            {"name": "MRF Zigma-ATT 295/80R22.5",         "brand": "MRF",          "pn": "MRF-ZA-295","price": "6900", "orig": None,   "stock": 10, "emoji": "⬛",  "compat": "TYRES,TYRE_REAR,tyres",   "desc": "All-terrain tyre for rear drive axle"},
            {"name": "Bridgestone R150 11R22.5",          "brand": "Bridgestone",  "pn": "BSR150-11R","price": "9200", "orig": "10500","stock": 6,  "emoji": "⬛",  "compat": "TYRES,tyres",              "desc": "Premium long-haul radial tyre"},
            {"name": "Steel Wheel Rim 22.5×8.25",         "brand": "Accuride",     "pn": "ACC-WR-225","price": "2800", "orig": "3200", "stock": 5,  "emoji": "⚪",  "compat": "TYRES,AXLE,wheels,tyres",  "desc": "Heavy duty steel wheel rim"},
        ]
    },
    {
        "category": "Electrical", "slug": "electrical", "icon": "⚡", "sort": 6,
        "products": [
            {"name": "SMF Battery 200Ah 12V",             "brand": "Amara Raja",   "pn": "AR-SMF-200","price": "4200", "orig": "4800", "stock": 5,  "emoji": "🔋",  "compat": "ELECTRICAL,ELEC_BATTERY", "desc": "Sealed maintenance-free battery 200Ah"},
            {"name": "Alternator 24V 90A",                "brand": "Bosch",        "pn": "0124655028","price": "6800", "orig": "7500", "stock": 3,  "emoji": "⚡",  "compat": "ELECTRICAL,ELEC_ALTERNATOR", "desc": "Heavy duty alternator for commercial vehicles"},
            {"name": "Starter Motor 24V",                 "brand": "Valeo",        "pn": "TS20E5",    "price": "5400", "orig": None,   "stock": 2,  "emoji": "🔌",  "compat": "ELECTRICAL,engine",        "desc": "24V heavy duty starter motor"},
        ]
    },
]


class Command(BaseCommand):
    help = "Seed shop categories and spare parts."

    def handle(self, *args, **options):
        created_cats = 0
        created_prods = 0

        for cat_data in CATALOGUE:
            cat, cc = ShopCategory.objects.get_or_create(
                slug=cat_data["slug"],
                defaults={"name": cat_data["category"], "icon": cat_data["icon"], "sort_order": cat_data["sort"]},
            )
            if cc:
                created_cats += 1

            for p in cat_data["products"]:
                _, cp = ShopProduct.objects.get_or_create(
                    part_number=p["pn"],
                    defaults={
                        "category":       cat,
                        "name":           p["name"],
                        "brand":          p["brand"],
                        "price":          Decimal(p["price"]),
                        "original_price": Decimal(p["orig"]) if p["orig"] else None,
                        "stock":          p["stock"],
                        "image_emoji":    p["emoji"],
                        "compatible_with":p["compat"],
                        "description":    p["desc"],
                    },
                )
                if cp:
                    created_prods += 1

        total_prods = ShopProduct.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f"Shop seeded: {created_cats} new categories, {created_prods} new products. "
            f"Total: {total_prods} products."
        ))
