import os
import json

# Define directory and load products from products.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "products.json")

# Standard list of fertilizers, fungicides, and crop care products (fallback)
FALLBACK_PRODUCTS = {
    "NPK_19_19_19": {
        "id": "NPK_19_19_19",
        "name": "Balanced NPK Fertilizer (19-19-19)",
        "category": "Fertilizer",
        "description": "Premium water-soluble nitrogen, phosphorus, and potassium formula. Boosts overall plant growth, root architecture, and fruit size.",
        "price": 14.99,
        "rating": 4.8,
        "image": "🧪",
        "image_path": "assets/products/npk_fertilizer.png",
        "suitability": "All Crops (Tomato, Potato, Pepper)",
        "benefits": "Provides balanced macronutrients, improves flowering, and accelerates vegetative growth."
    },
    "COPPER_FUNGICIDE": {
        "id": "COPPER_FUNGICIDE",
        "name": "Liquid Copper Fungicide",
        "category": "Fungicide",
        "description": "Organic-approved copper octanoate controls early/late blight, bacterial spot, and leaf mold on vegetable crops.",
        "price": 18.50,
        "rating": 4.9,
        "image": "🧴",
        "image_path": "assets/products/copper_fungicide.png",
        "suitability": "Tomato, Potato, Pepper",
        "benefits": "Halts spore germination, controls bacterial infections, and leaves no toxic soil residue."
    },
    "NEEM_OIL_SPRAY": {
        "id": "NEEM_OIL_SPRAY",
        "name": "Cold-Pressed Organic Neem Oil Spray",
        "category": "Pest Control",
        "description": "Ready-to-use botanical insecticide, miticide, and fungicide. Ideal for controlling spider mites, whiteflies, and aphids.",
        "price": 12.99,
        "rating": 4.7,
        "image": "🌿",
        "image_path": "assets/products/neem_oil.png",
        "suitability": "All Crops",
        "benefits": "Disrupts pest reproductive cycles, eco-friendly, and safe for beneficial insects like bees."
    },
    "CALCIUM_NITRATE": {
        "id": "CALCIUM_NITRATE",
        "name": "Calcium Nitrate Foliar Spray",
        "category": "Soil & Nutrient Care",
        "description": "Targeted mineral fertilizer to cure calcium deficiencies. Prevents blossom end rot in tomatoes and pepper fruits.",
        "price": 16.25,
        "rating": 4.6,
        "image": "❄️",
        "image_path": "assets/products/calcium_nitrate.png",
        "suitability": "Tomato, Pepper",
        "benefits": "Strengthens cell walls, stops fruit tip rotting, and improves shelf-life."
    },
    "ORGANIC_COMPOST": {
        "id": "ORGANIC_COMPOST",
        "name": "Bio-Active Vermicompost",
        "category": "Soil & Nutrient Care",
        "description": "Enriched with mycorrhizal fungi and humic acids to restore soil microbiome and boost natural crop immunity.",
        "price": 9.99,
        "rating": 4.8,
        "image": "🧫",
        "image_path": "assets/products/organic_compost.png",
        "suitability": "All Crops",
        "benefits": "Improves soil moisture retention, provides complete trace minerals, and encourages robust root growth."
    },
    "MANCOZEB_WP": {
        "id": "MANCOZEB_WP",
        "name": "Mancozeb 75% WP Fungicide",
        "category": "Fungicide",
        "description": "Broad-spectrum contact fungicide that forms a protective layer on leaves to stop fungal blights and Septoria spot.",
        "price": 22.00,
        "rating": 4.5,
        "image": "📦",
        "image_path": "assets/products/mancozeb.png",
        "suitability": "Tomato, Potato",
        "benefits": "Multi-site activity prevents resistance build-up, rains-fast, and provides zinc/manganese supplements."
    },
    "SULFUR_DUST": {
        "id": "SULFUR_DUST",
        "name": "Micronized Sulfur Powder",
        "category": "Fungicide",
        "description": "Dual-action natural dust/spray protecting crops against powdery mildew, leaf molds, and microscopic spider mites.",
        "price": 11.49,
        "rating": 4.4,
        "image": "🟡",
        "image_path": "assets/products/sulfur_powder.png",
        "suitability": "Tomato, Pepper",
        "benefits": "Eco-friendly, acts as both a fungicide and miticide, and provides essential sulfur nutrient."
    },
    "EPSOM_SALT": {
        "id": "EPSOM_SALT",
        "name": "Pure Agricultural Epsom Salt",
        "category": "Soil & Nutrient Care",
        "description": "Highly soluble magnesium sulfate crystals. Cures leaf yellowing between veins and intensifies green color.",
        "price": 8.75,
        "rating": 4.7,
        "image": "🧂",
        "image_path": "assets/products/epsom_salt.png",
        "suitability": "All Crops",
        "benefits": "Improves chlorophyll synthesis, maximizes fertilizer uptake, and increases crop yields."
    }
}

class LocalizedProducts(dict):
    def _get_lang_products(self):
        try:
            import streamlit as st
            lang = st.session_state.get("language", "en")
        except Exception:
            lang = "en"
            
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if lang == "hi":
            path = os.path.join(base_dir, "products_hi.json")
        elif lang == "es":
            path = os.path.join(base_dir, "products_es.json")
        else:
            path = os.path.join(base_dir, "products.json")
            
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return FALLBACK_PRODUCTS

    def __getitem__(self, key):
        return self._get_lang_products()[key]

    def __contains__(self, key):
        return key in self._get_lang_products()

    def get(self, key, default=None):
        return self._get_lang_products().get(key, default)

    def values(self):
        return self._get_lang_products().values()

    def items(self):
        return self._get_lang_products().items()

    def keys(self):
        return self._get_lang_products().keys()

    def __len__(self):
        return len(self._get_lang_products())

    def __iter__(self):
        return iter(self._get_lang_products())

PRODUCTS = LocalizedProducts()

# Map each class output from the disease predictor to recommended product IDs
DISEASE_PRODUCT_MAPPING = {
  "Corn___Common_Rust": [
    "RUSTSHIELD_COPPER_SPRAY",
    "TRIAZOLE_FUNGICIDE_MAX"
  ],
  "Corn___Gray_Leaf_Spot": [
    "STROBILURIN_ACTIVE_250",
    "POTASH_FERTILIZER_PREMIUM"
  ],
  "Corn___Healthy": [
    "ORGANIC_SOIL_BUILDER",
    "ALL_PURPOSE_PLANT_TONIC"
  ],
  "Corn___Northern_Leaf_Blight": [
    "EXSEROHILUM_CONTROL_SPRAY",
    "BLIGHTGUARD_PRO_FUNGICIDE"
  ],
  "Potato___Early_Blight": [
    "MANCOZEB_DEFENDER_75",
    "CHLOROTHALONIL_POWER_SPRAY"
  ],
  "Potato___Healthy": [
    "POTASH_PLUS_TUBER_BOOSTER",
    "ORGANIC_COMPOST_BOOSTER"
  ],
  "Potato___Late_Blight": [
    "METALAXYL_SYSTEMIC_SPRAY",
    "INFESTANS_BLIGHT_CONTROL"
  ],
  "Rice___Brown_Spot": [
    "HEXACONAZOLE_ANTI_SPOT_SPRAY",
    "MICRONUTRIENT_ZINC_MIX"
  ],
  "Rice___Healthy": [
    "PREMIUM_PADDY_NPK_BOOST",
    "BIO_ORGANIC_GROWTH_PROMOTER"
  ],
  "Rice___Leaf_Blast": [
    "TRICYCLAZOLE_BLAST_SHIELD",
    "KASUGAMYCIN_ORGANIC_BACTERICIDE"
  ],
  "Rice___Neck_Blast": [
    "ISOPROTHIOLANE_BLAST_MASTER",
    "NECK_BLAST_PRO_DEFENSE"
  ],
  "Sugarcane___Bacterial_Blight": [
    "BACTERICIDE_COPPER_HYDROXIDE",
    "FIELD_DISINFECTANT_LIQUID"
  ],
  "Sugarcane___Healthy": [
    "SUGARCANE_SPECIAL_MICRONUTRIENTS",
    "PREMIUM_COMPOST_FERTILIZER"
  ],
  "Sugarcane___Red_Rot": [
    "TRICHODERMA_VIRIDE_BIO_FUNGICIDE",
    "AGRICULTURAL_LIME_WASH"
  ],
  "Wheat___Brown_Rust": [
    "PROPICONAZOLE_LEAF_DEFENDER",
    "PREMIUM_TEBUCONAZOLE_SPRAY"
  ],
  "Wheat___Healthy": [
    "WHEAT_MICRONUTRIENT_SUPPLEMENT",
    "BIO_STIMULANT_SPIKES_BOOSTER"
  ],
  "Wheat___Yellow_Rust": [
    "TRIADIMEFON_STRIPE_CONTROLLER",
    "PROPICONAZOLE_ACTIVE_SPRAY"
  ]
}

def get_recommended_products(disease_class):
    """
    Get a list of product dictionaries recommended for a specific disease class.
    """
    product_ids = DISEASE_PRODUCT_MAPPING.get(disease_class, ["ORGANIC_SOIL_BUILDER", "ALL_PURPOSE_PLANT_TONIC"])
    return [PRODUCTS[pid] for pid in product_ids if pid in PRODUCTS]
