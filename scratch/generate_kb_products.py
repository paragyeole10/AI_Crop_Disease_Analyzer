import sys
import os
import json

# Add Crop_app backend to path to import disease_data
sys.path.append('d:/Crop_app/backend')
import disease_data

# Translation map from English to Spanish for categories, crop names, and diseases
SPANISH_TRANSLATION = {
    # Crop names
    "Corn": "Maíz",
    "Potato": "Patata",
    "Rice": "Arroz",
    "Sugarcane": "Caña de Azúcar",
    "Wheat": "Trigo",

    # Disease Names
    "Common Rust": "Roya Común",
    "Gray Leaf Spot": "Mancha Foliar Gris",
    "Healthy": "Sano",
    "Northern Leaf Blight": "Tizón Foliar del Norte",
    "Early Blight": "Tizón Temprano",
    "Late Blight": "Tizón Tardío",
    "Brown Spot": "Mancha Marrón",
    "Leaf Blast": "Añublo de la Hoja",
    "Neck Blast": "Añublo del Cuello",
    "Bacterial Blight": "Tizón Bacteriano",
    "Red Rot": "Podredumbre Roja",
    "Brown Rust": "Roya Marrón",
    "Yellow Rust": "Roya Amarilla",

    # Severities
    "Moderate": "Moderada",
    "Low": "Baja",
    "High": "Alta",
    "None": "Ninguno",

    # Product names
    "RustShield Copper Spray": "Spray de Cobre RustShield",
    "Triazole Fungicide Max": "Fungicida Triazol Max",
    "Chlorothalonil Power Spray": "Spray Potente de Clorotalonil",
    "Organic Soil Builder": "Constructor de Suelo Orgánico",
    "Micronutrient Zinc Mix": "Mezcla de Micronutrientes de Zinc",
    "Exserohilum Control Spray": "Spray de Control Exserohilum",
    "Potash Plus Tuber Booster": "Potasa Plus Potenciador de Tubérculos",
    "BlightGuard Pro Fungicide": "Fungicida BlightGuard Pro",
    "Infestans Blight Control": "Control de Tizón Infestans",
    "Organic Compost Booster": "Potenciador de Compost Orgánico",
    "All-Purpose Plant Tonic": "Tónico de Plantas Multiuso",
    "Bio-Stimulant Spikes Booster": "Potenciador de Espigas Bio-Estimulante",
    "Propiconazole Active Spray": "Spray Activo de Propiconazol",
    "Strobilurin Active 250": "Estrobirulina Activa 250",
    "Hexaconazole Anti-Spot Spray": "Spray Anti-Manchas de Hexaconazol",
    "Tricyclazole Blast Shield": "Escudo de Añublo Triciclazol",
    "Isoprothiolane Blast Master": "Maestro de Añublo Isoprotiolano",
    "Premium Paddy NPK Boost": "Potenciador NPK Paddy Premium",
    "Neck Blast Pro Defense": "Defensa Pro Añublo del Cuello",
    "Kasugamycin Organic Bactericide": "Bactericida Orgánico Kasugamicina",
    "Bactericide Copper Hydroxide": "Bactericida de Hidróxido de Cobre",
    "Trichoderma Viride Bio-Fungicide": "Bio-Fungicida Trichoderma Viride",
    "Premium Compost Fertilizer": "Fertilizante de Compost Premium",
    "Sugarcane Special Micronutrients": "Micronutrientes Especiales para Caña de Azúcar",
    "Metalaxyl Systemic Spray": "Spray Sistémico Metalaxil",
    "Propiconazole Leaf Defender": "Defensor de Hojas Propiconazol",
    "Triadimefon Stripe Controller": "Controlador de Rayas Triadimefon",
    "Wheat Micronutrient Supplement": "Suplemento de Micronutrientes de Trigo",
    "Potash Fertilizer Premium": "Fertilizante de Potasa Premium",
    "Agricultural Lime Wash": "Lavado de Cal Agrícola",
    "Bio-Organic Growth Promoter": "Promotor de Crecimiento Bio-Orgánico",
    "Field Disinfectant Liquid": "Líquido Desinfectante de Campo",
    "Premium Tebuconazole Spray": "Spray de Tebuconazol Premium",
    
    # Sentences & Paragraphs (Descriptions)
    "Common rust is a fungal disease caused by Puccinia sorghi, causing powdery rust-colored pustules on leaf surfaces.": 
        "La roya común es una enfermedad fúngica causada por Puccinia sorghi, que provoca pústulas de color marrón canela en la superficie de las hojas.",
    "Gray leaf spot is caused by the fungus Cercospora zeae-maydis, causing rectangular lesions that run parallel to leaf veins.":
        "La mancha foliar gris es causada por el hongo Cercospora zeae-maydis, que provoca lesiones rectangulares que corren paralelas a las venas de las hojas.",
    "The corn crop is in excellent condition showing strong stalk and leaf development with no active pathogen stress.":
        "El cultivo de maíz se encuentra en excelentes condiciones, mostrando un fuerte desarrollo del tallo y las hojas, sin estrés por patógenos activos.",
    "Northern leaf blight is a fungal infection caused by Exserohilum turcicum, producing long, elliptical, grayish-green lesions resembling cigar shapes.":
        "El tizón foliar del norte es una infección fúngica causada por Exserohilum turcicum, que produce lesiones largas, elípticas y de color verde grisáceo que se asemejan a la forma de un cigarro.",
    "Early blight is caused by the fungus Alternaria solani, producing circular brown spots with concentric rings on older potato leaves first.":
        "El tizón temprano es causado por el hongo Alternaria solani, que produce manchas circulares de color marrón con anillos concéntricos en las hojas más viejas de la patata primero.",
    "The potato crop is fully healthy, showing uniform green compound leaves and firm stem configurations.":
        "El cultivo de patata está completamente sano, mostrando hojas compuestas de color verde uniforme y tallos firmes.",
    "Late blight is a highly destructive oomycete disease caused by Phytophthora infestans, spreading rapidly in cool, wet weather.":
        "El tizón tardío es una enfermedad por oomicetos altamente destructiva causada por Phytophthora infestans, que se propaga rápidamente en climas frescos y húmedos.",
    "Brown spot is a fungal disease caused by Bipolaris oryzae, causing oval, reddish-brown lesions with gray centers on rice leaves.":
        "La mancha marrón es una enfermedad fúngica causada por Bipolaris oryzae, que provoca lesiones ovaladas de color marrón rojizo con centros grises en las hojas de arroz.",
    "The rice crop is healthy with vibrant green upright tillers and clean, disease-free leaf blades.":
        "El cultivo de arroz está sano con macollos erguidos de color verde vibrante y láminas foliares limpias y libres de enfermedades.",
    "Leaf blast is caused by the fungus Magnaporthe oryzae, causing spindle-shaped lesions with gray centers and reddish-brown borders.":
        "El añublo de la hoja es causado por el hongo Magnaporthe oryzae, que provoca lesiones en forma de huso con centros grises y bordes marrón rojizo.",
    "Neck blast occurs when the fungus Magnaporthe oryzae attacks the node at the base of the panicle, causing the stem to rot and break.":
        "El añublo del cuello ocurre cuando el hongo Magnaporthe oryzae ataca el nudo en la base de la panícula, haciendo que el tallo se pudra y se rompa.",
    "Bacterial blight is caused by Xanthomonas albilineans, causing long, yellow-to-white streaks along sugarcane leaf veins.":
        "El tizón bacteriano es causado por Xanthomonas albilineans, que provoca rayas largas de color amarillo a blanco a lo largo de las venas de las hojas de la caña de azúcar.",
    "The sugarcane crop displays strong cane height, lush foliage, and no signs of bacterial or fungal infection.":
        "El cultivo de caña de azúcar muestra una altura de caña fuerte, follaje exuberante y ningún signo de infección bacteriana o fúngica.",
    "Red rot is a devastating fungal disease caused by Colletotrichum falcatum, causing internal cane reddening with white patches.":
        "La podredumbre roja es una enfermedad fúngica devastadora causada por Colletotrichum falcatum, que provoca un enrojecimiento interno de la caña con manchas blancas.",
    "Brown rust is caused by Puccinia melanocephala, causing small, reddish-brown pustules on wheat leaves.":
        "La roya marrón es causada por Puccinia melanocephala, que provoca pequeñas pústulas de color marrón rojizo en las hojas de trigo.",
    "The wheat crop is fully healthy, showing uniform green tillers and strong spike development without leaf anomalies.":
        "El cultivo de trigo está completamente sano, mostrando macollos verdes uniformes y un fuerte desarrollo de las espigas sin anomalías en las hojas.",
    "Yellow rust (stripe rust) is caused by Puccinia striiformis, causing yellow-to-orange pustules arranged in long stripes on wheat leaf surfaces.":
        "La roya amarilla (roya lineal) es causada por Puccinia striiformis, que provoca pústulas de color amarillo a naranja dispuestas en líneas largas en la superficie de las hojas de trigo.",

    # Symptoms
    "Cinnamon-brown pustules on both upper and lower leaf surfaces.":
        "Pústulas de color marrón canela en la superficie superior e inferior de las hojas.",
    "Leaves turn yellow and may wither prematurely.":
        "Las hojas se vuelven amarillas y pueden marchitarse prematuramente.",
    "Pustules turn dark brown to black as the crop matures.":
        "Las pústulas se vuelven de color marrón oscuro a negro a medida que el cultivo madura.",
    "Tan to gray rectangular lesions bounded by leaf veins.":
        "Lesiones rectangulares de color tostado a gris limitadas por las venas de las hojas.",
    "Blighting of large leaf areas under severe pressure.":
        "Tizón de grandes áreas foliares bajo una presión severa de la enfermedad.",
    "Stalk lodging may occur if photosynthesis is severely restricted.":
        "Puede ocurrir el encamado del tallo si la fotosíntesis se ve gravemente limitada.",
    "Robust stalks with bright green leaf surfaces.":
        "Tallos robustos con superficies foliares de color verde brillante.",
    "Clean leaf margins without spots or dry patches.":
        "Márgenes foliares limpios sin manchas ni parches secos.",
    "Healthy tassels and developing ears without mold.":
        "Espigas sanas y mazorcas en desarrollo sin moho.",
    "Long, elliptical, grayish-green or tan lesions (1-6 inches long).":
        "Lesiones largas, elípticas, de color verde grisáceo o tostado (de 1 a 6 pulgadas de largo).",
    "Lesiones resemble cigar shapes, parallel to leaf margins.":
        "Las lesiones se asemejan a formas de cigarros, paralelas a los márgenes de las hojas.",
    "Severe leaf drying, starting from lower leaves upward.":
        "Secado severo de las hojas, comenzando desde las hojas inferiores hacia arriba.",
    "Circular brown spots with concentric rings ('target-board' pattern).":
        "Manchas circulares de color marrón con anillos concéntricos (patrón de 'blanco de tiro').",
    "Yellow halo surrounding the brown leaf spots.":
        "Halo amarillo que rodea las manchas marrones de las hojas.",
    "Lower leaves dry up and drop off prematurely.":
        "Las hojas inferiores se secan y caen prematuramente.",
    "Compound leaves are dark green and free of spots.":
        "Hojas compuestas de color verde oscuro y libres de manchas.",
    "Stems are firm, self-supporting, and clean.":
        "Los tallos son firmes, autoportantes y limpios.",
    "Tubers develop normally underground with no rot.":
        "Los tubérculos se desarrollan normalmente bajo tierra sin podredumbre.",
    "Dark green, water-soaked lesions that expand rapidly under wet conditions.":
        "Lesiones de color verde oscuro empapadas de agua que se expanden rápidamente en condiciones húmedas.",
    "White, velvety fungal growth on leaf undersides in high humidity.":
        "Crecimiento fúngico blanco y aterciopelado en el envés de las hojas con alta humedad.",
    "Tuber skin develops dark, sunken, decayed patches.":
        "La piel del tubérculo desarrolla manchas oscuras, hundidas y podridas.",
    "Small, oval brown lesions with gray or yellow centers.":
        "Pequeñas lesiones ovaladas de color marrón con centros grises o amarillos.",
    "Lesions distribute evenly across the leaf surface.":
        "Las lesiones se distribuyen uniformemente sobre la superficie de la hoja.",
    "In severe cases, leaves turn yellow, dry up, and wither.":
        "En casos severos, las hojas se vuelven amarillas, se secan y se marchitan.",
    "Tillers are upright, firm, and consistently green.":
        "Los macollos son erguidos, firmes y uniformemente verdes.",
    "Leaf blades are clean without brown streaks or yellow spots.":
        "Las láminas foliares están limpias, sin rayas marrones ni manchas amarillas.",
    "Panicles develop uniformly without empty heads.":
        "Las panículas se desarrollan uniformemente sin espiguillas vacías.",
    "Spindle-shaped (diamond-shaped) lesions on leaves.":
        "Lesiones en forma de huso (rombo) en las hojas.",
    "Lesions have gray centers and reddish-brown borders.":
        "Las lesiones tienen centros grises y bordes marrón rojizo.",
    "Lesions merge, causing the entire leaf blade to die.":
        "Las lesiones se fusionan, provocando la muerte de toda la lámina foliar.",
    "Base of the panicle turns dark brown to black and rots.":
        "La base de la panícula se vuelve de color marrón oscuro a negro y se pudre.",
    "Panicles fall over or break off easily at the neck.":
        "Las panículas se caen o se rompen fácilmente por el cuello.",
    "Grains remain empty or light, turning white (whiteheads).":
        "Los granos permanecen vacíos o ligeros, volviéndose blancos (espigas blancas).",
    "Long, narrow, chlorotic yellow-to-white streaks on leaves.":
        "Rayas estrechas y largas de color amarillo a blanco clorótico en las hojas.",
    "Streaks turn reddish-brown as tissue dies.":
        "Las rayas se vuelven de color marrón rojizo a medida que el tejido muere.",
    "Young leaves may fail to unfold, showing a 'whip-like' symptom.":
        "Las hojas jóvenes pueden no desplegarse, mostrando un síntoma de 'látigo'.",
    "Stems are tall, thick, and deep green.":
        "Los tallos son altos, gruesos y de color verde oscuro.",
    "Cane joints are firm and free of discoloration.":
        "Los nudos de la caña son firmes y libres de decoloración.",
    "Internal cane tissues turn red with white cross-wise patches.":
        "Los tejidos internos de la caña se vuelven rojos con manchas blancas transversales.",
    "Leaves turn yellow, wither, and dry from the tips downward.":
        "Las hojas se vuelven amarillas, se marchitan y se secan desde las puntas hacia abajo.",
    "Cane emits a sour, fermented odor when split open.":
        "La caña emite un olor agrio y fermentado cuando se abre.",
    "Small, oval, reddish-brown pustules on leaves.":
        "Pequeñas pústulas ovaladas de color marrón rojizo en las hojas.",
    "Pustules are scattered randomly on leaf surfaces.":
        "Las pústulas se dispersan aleatoriamente en la superficie de las hojas.",
    "Leaves yellow and dry up under heavy rust pressure.":
        "Las hojas se vuelven amarillas y se secan bajo una fuerte presión de roya.",
    "Stems and leaves have a vibrant green color.":
        "Los tallos y las hojas tienen un color verde vibrante.",
    "Tillers are dense, upright, and healthy.":
        "Los macollos son densos, erguidos y sanos.",
    "Wheat ears develop healthy grains without yellow stripes.":
        "Las espigas de trigo desarrollan granos sanos sin rayas amarillas.",
    "Yellow-to-orange pustules arranged in narrow, long stripes on leaves.":
        "Pústulas de color amarillo a naranja dispuestas en rayas estrechas y largas en las hojas.",
    "Stripes run parallel to leaf veins, resembling sewing stitches.":
        "Las rayas corren paralelas a las venas de las hojas, asemejándose a puntadas de costura.",
    "Entire leaves may yellow, dry up, and turn brown.":
        "Las hojas enteras pueden volverse amarillas, secarse y volverse marrones.",

    # Treatments
    "Apply recommended copper-based or triazole fungicides early in the season.":
        "Aplique fungicidas a base de cobre o triazol recomendados al principio de la temporada.",
    "Avoid overhead sprinkler irrigation to keep the canopy dry.":
        "Evite el riego por aspersión aérea para mantener el dosel seco.",
    "Ensure proper crop spacing to improve ventilation.":
        "Asegure un espaciado adecuado de los cultivos para mejorar la ventilación.",
    "Apply preventative strobilurin or triazole fungicides if disease pressure is high.":
        "Aplique fungicidas preventivos de estrobirulina o triazol si la presión de la enfermedad es alta.",
    "Shred and bury crop residues to accelerate decomposition.":
        "Triture y entierre los residuos de cultivos para acelerar su descomposición.",
    "No active disease treatment required.":
        "No se requiere tratamiento activo contra enfermedades.",
    "Maintain standard nitrogen-phosphorus-potassium fertilization.":
        "Mantenga la fertilización estándar de nitrógeno, fósforo y potasio.",
    "Apply a copper-based or chlorothalonil fungicide at the first sign of lesions.":
        "Aplique un fungicida a base de cobre o clorotalonil ante el primer signo de lesiones.",
    "Improve drainage in low-lying field areas.":
        "Mejore el drenaje en las áreas bajas del campo.",
    "Apply protective fungicides containing chlorothalonil, mancozeb, or copper oxychloride.":
        "Aplique fungicidas protectores que contengan clorotalonil, mancozeb o oxicloruro de cobre.",
    "Prune and destroy infected lower leaves.":
        "Pode y destruya las hojas inferiores infectadas.",
    "Apply balanced nitrogen fertilization to avoid plant stress.":
        "Aplique una fertilización nitrogenada equilibrada para evitar el estrés de la planta.",
    "No disease treatment is necessary.":
        "No se necesita tratamiento contra la enfermedad.",
    "Continue standard hilling and soil aeration.":
        "Continúe con el aporcado estándar y la aireación del suelo.",
    "Apply systemic fungicides (metalaxyl or dimethomorph) immediately upon detection.":
        "Aplique fungicidas sistémicos (metalaxil o dimetomorf) inmediatamente después de la detección.",
    "Destroy heavily infected plants; do not use for composting.":
        "Destruya las plantas muy infectadas; no las use para compostaje.",
    "Kill potato vines 2 weeks prior to harvest.":
        "Elimine las vides de patata 2 semanas antes de la cosecha.",
    "Apply preventative copper or propiconazole fungicides early.":
        "Aplique fungicidas preventivos de cobre o propiconazol temprano.",
    "Use balanced fertilizers containing silica and potassium.":
        "Utilice fertilizantes equilibrados que contengan sílice y potasio.",
    "Remove alternative weed hosts from field borders.":
        "Elimine los huéspedes alternativos de malezas de los bordes del campo.",
    "Maintain appropriate field hydration and soil aeration.":
        "Mantenga una hidratación del campo y aireación del suelo adecuadas.",
    "Apply silicon-based soil amendments.":
        "Aplique enmiendas de suelo a base de silicio.",
    "Apply systemic fungicides like tricyclazole or isoprothiolane.":
        "Aplique fungicidas sistémicos como triciclazol o isoprotiolano.",
    "Ensure nitrogen fertilizer is not applied in excess.":
        "Asegúrese de no aplicar fertilizante nitrogenado en exceso.",
    "Apply fungicides containing kasugamycin or copper hydroxide.":
        "Aplique fungicidas que contengan kasugamicina o hidróxido de cobre.",
    "Quickly drain fields showing early neck rot symptoms.":
        "Drene rápidamente los campos que muestren síntomas tempranos de podredumbre del cuello.",
    "Prune infected tillers to reduce the inoculum level.":
        "Pode los macollos infectados para reducir el nivel de inóculo.",
    "Apply copper-based bactericides to suppress bacterial multiplication.":
        "Aplique bactericidas a base de cobre para suprimir la multiplicación bacteriana.",
    "Rogue out and destroy infected sugarcane clumps.":
        "Arranque y destruya las matas de caña de azúcar infectadas.",
    "Maintain clean farm equipment to prevent mechanical transmission.":
        "Mantenga el equipo agrícola limpio para evitar la transmisión mecánica.",
    "Monitor soil moisture and maintain optimal irrigation.":
        "Monitoree la humedad del suelo y mantenga un riego óptimo.",
    "Uproot and burn infected sugarcane stalks immediately.":
        "Arranque y queme los tallos de caña de azúcar infectados inmediatamente.",
    "Apply recommended systemic fungicides to control Colletotrichum.":
        "Aplique fungicidas sistémicos recomendados para controlar Colletotrichum.",
    "Apply propiconazole or triadimefon fungicides at the first sign of rust.":
        "Aplique fungicidas de propiconazol o triadimefón al primer signo de roya.",
    "Apply foliar micronutrient sprays to boost plant recovery.":
        "Aplique aerosoles foliares de micronutrientes para acelerar la recuperación de la planta.",
    "Provide regular watering according to growth stage.":
        "Proporcione un riego regular de acuerdo con la etapa de crecimiento.",
    "Perform early weeding and maintain field cleanliness.":
        "Realice un deshierbe temprano y mantenga la limpieza del campo.",
    "Apply stripe-rust targeted triazole fungicides (tebuconazole or propiconazole).":
        "Aplique fungicidas triazol específicos para la roya lineal (tebuconazol o propiconazol).",
    "Avoid overhead irrigation during rust outbreaks.":
        "Evite el riego aéreo durante los brotes de roya.",

    # Preventions
    "Use rust-resistant hybrid corn seeds.":
        "Utilice semillas de maíz híbrido resistentes a la roya.",
    "Practice proper crop rotation with non-host crops.":
        "Practique una rotación de cultivos adecuada con cultivos no hospedantes.",
    "Maintain optimal soil health with balanced nitrogen application.":
        "Mantenga una salud óptima del suelo con una aplicación equilibrada de nitrógeno.",
    "Select crop hybrids with strong disease resistance ratings.":
        "Seleccione híbridos de cultivos con calificaciones sólidas de resistencia a enfermedades.",
    "Practice a minimum 2-year crop rotation.":
        "Practique una rotación de cultivos mínima de 2 años.",
    "Implement conservation tillage only with resistant varieties.":
        "Implemente labranza de conservación solo con variedades resistentes.",
    "Rotate corn crops with soybeans or alfalfa.":
        "Rote los cultivos de maíz con soja o alfalfa.",
    "Ensure balanced fertilization according to soil tests.":
        "Asegure una fertilización equilibrada según los análisis del suelo.",
    "Sow seeds at recommended densities to avoid high canopy humidity.":
        "Siembre semillas a las densidades recomendadas para evitar una alta humedad del dosel.",
    "Choose corn hybrids with high resistance to E. turcicum.":
        "Elija híbridos de maíz con alta resistencia a E. turcicum.",
    "Bury crop residues via deep plowing after harvest.":
        "Entierre los residuos de cultivos mediante arado profundo después de la cosecha.",
    "Plant certified, disease-resistant seed tubers.":
        "Plante únicamente tubérculos de semilla certificados y resistentes a enfermedades.",
    "Space plants adequately to encourage rapid leaf drying.":
        "Espacie las plantas adecuadamente para favorecer el secado rápido de las hojas.",
    "Rotate potato crops with corn, small grains, or grasses.":
        "Rote los cultivos de patata con maíz, granos pequeños o pastos.",
    "Practice a 3-year crop rotation schedule.":
        "Practique un programa de rotación de cultivos de 3 años.",
    "Provide deep watering once a week rather than shallow watering.":
        "Proporcione un riego profundo una vez a la semana en lugar de riegos superficiales.",
    "Plant only certified, disease-free seed tubers.":
        "Plante únicamente tubérculos de semilla certificados y libres de enfermedades.",
    "Select late blight-resistant cultivars.":
        "Seleccione cultivares resistentes al tizón tardío.",
    "Avoid overhead watering; irrigate early in the morning.":
        "Evite el riego aéreo; irrigue temprano en la mañana.",
    "Use disease-free certified seeds.":
        "Utilice semillas certificadas libres de enfermedades.",
    "Maintain balanced soil fertility (avoid excess nitrogen).":
        "Mantenga una fertilidad del suelo equilibrada (evite el exceso de nitrógeno).",
    "Monitor fields weekly for brown spots.":
        "Monitoree los campos semanalmente para detectar manchas marrones.",
    "Implement seed treatment before sowing.":
        "Implemente el tratamiento de semillas antes de la siembra.",
    "Maintain continuous soil health monitoring.":
        "Mantenga un monitoreo continuo de la salud del suelo.",
    "Avoid excessive nitrogen application; use split doses.":
        "Evite la aplicación excesiva de nitrógeno; use dosis divididas.",
    "Maintain appropriate water level in the field (avoid water logging).":
        "Mantenga un nivel de agua adecuado en el campo (evite el encharcamiento).",
    "Burn crop residues after harvest to destroy pathogen inoculum.":
        "Queme los residuos de cultivos después de la cosecha para destruir el inóculo de patógenos.",
    "Select blast-resistant rice cultivars.":
        "Seleccione cultivares de arroz resistentes al añublo.",
    "Space seedlings properly during transplantation.":
        "Espacie las plántulas adecuadamente durante el trasplante.",
    "Avoid late transplanting of seedlings.":
        "Evite el trasplante tardío de plántulas.",
    "Use healthy, disease-free seed setts for planting.":
        "Utilice trozos de semillas saludables y libres de enfermedades para plantar.",
    "Grow resistant sugarcane varieties.":
        "Cultive variedades de caña de azúcar resistentes.",
    "Sanitize cutting tools before preparing seed setts.":
        "Desinfecte las herramientas de corte antes de preparar los trozos de semillas.",
    "Implement crop rotation with green manure crops.":
        "Implemente la rotación de cultivos con cultivos de abono verde.",
    "Clean the field boundaries from alternative hosts.":
        "Limpie los límites del campo de huéspedes alternativos.",
    "Select red rot resistant sugarcane cultivars.":
        "Seleccione cultivares de caña de azúcar resistentes a la podredumbre roja.",
    "Use healthy seed setts from certified nurseries.":
        "Utilice trozos de semillas saludables de viveros certificados.",
    "Treat setts with hot water before planting.":
        "Trate los trozos con agua caliente antes de plantar.",
    "Plant rust-resistant wheat varieties.":
        "Plante variedades de trigo resistentes a la roya.",
    "Avoid sowing wheat too late in the season.":
        "Evite sembrar trigo demasiado tarde en la temporada.",
    "Monitor crops during warm, humid spring periods.":
        "Monitoree los cultivos durante los períodos de primavera cálidos y húmedos.",
    "Use high-quality certified wheat seeds.":
        "Utilice semillas de trigo certificadas de alta calidad.",
    "Ensure balanced NPK soil application.":
        "Asegure una aplicación equilibrada de NPK en el suelo.",
    "Rotate wheat with non-cereal crops every two years.":
        "Rote el trigo con cultivos no cereales cada dos años.",
    "Sow yellow-rust resistant wheat cultivars.":
        "Siembre cultivares de trigo resistentes a la roya amarilla.",
    "Sow wheat early in the recommended window.":
        "Siembre trigo temprano en el período recomendado.",
    "Remove wild grasses from field edges.":
        "Elimine las hierbas silvestres de los bordes del campo.",
}

# English knowledge base
kb_en = {}
# Hindi knowledge base
kb_hi = {}
# Spanish knowledge base
kb_es = {}
# Marathi knowledge base
kb_mr = {}

# Set of all unique product names across the dataset
unique_products = {}

# Map product names to categories
def get_product_category(name):
    name_l = name.lower()
    if 'fungicide' in name_l or 'rustshield' in name_l or 'blight' in name_l or 'spray' in name_l or 'blast' in name_l or 'anti-spot' in name_l or 'triadimefon' in name_l:
        return 'Fungicide'
    elif 'fertilizer' in name_l or 'npk' in name_l or 'potash' in name_l or 'builder' in name_l or 'compost' in name_l or 'micronutrient' in name_l or 'zinc' in name_l:
        return 'Fertilizer'
    elif 'bactericide' in name_l or 'disinfectant' in name_l or 'lime' in name_l:
        return 'Pest Control'
    else:
        return 'Soil & Nutrient Care'

def get_product_image(category):
    if category == 'Fungicide':
        return '🧴'
    elif category == 'Fertilizer':
        return '🧪'
    elif category == 'Pest Control':
        return '🌿'
    else:
        return '🧫'

for class_name, data in disease_data.DISEASE_DATA.items():
    crop_en = data['English'].get('crop', '')
    crop_es = SPANISH_TRANSLATION.get(crop_en, crop_en)
    
    # Process English
    kb_en[class_name] = {
        "disease_name": data['English']['disease_name'],
        "description": data['English']['description'],
        "symptoms": data['English']['symptoms'],
        "treatment": data['English']['treatment'],
        "prevention": data['English']['prevention']
    }
    
    # Process Hindi
    kb_hi[class_name] = {
        "disease_name": data['Hindi']['disease_name'],
        "description": data['Hindi']['description'],
        "symptoms": data['Hindi']['symptoms'],
        "treatment": data['Hindi']['treatment'],
        "prevention": data['Hindi']['prevention']
    }
    
    # Process Marathi
    kb_mr[class_name] = {
        "disease_name": data['Marathi']['disease_name'],
        "description": data['Marathi']['description'],
        "symptoms": data['Marathi']['symptoms'],
        "treatment": data['Marathi']['treatment'],
        "prevention": data['Marathi']['prevention']
    }
    
    # Translate to Spanish
    s_name = data['English']['disease_name']
    s_desc = data['English']['description']
    
    trans_name = SPANISH_TRANSLATION.get(s_name, f"Enfermedad {s_name}")
    trans_desc = SPANISH_TRANSLATION.get(s_desc, f"[ES] {s_desc}")
    
    trans_symptoms = [SPANISH_TRANSLATION.get(s, f"[ES] {s}") for s in data['English']['symptoms']]
    trans_treatment = [SPANISH_TRANSLATION.get(t, f"[ES] {t}") for t in data['English']['treatment']]
    trans_prevention = [SPANISH_TRANSLATION.get(p, f"[ES] {p}") for p in data['English']['prevention']]
    
    kb_es[class_name] = {
        "disease_name": trans_name,
        "description": trans_desc,
        "symptoms": trans_symptoms,
        "treatment": trans_treatment,
        "prevention": trans_prevention
    }
    
    # Gather products information
    for lang in ['English', 'Hindi']:
        prods = data[lang].get('products', [])
        for p in prods:
            pname = p['name']
            pprice = p['price']
            
            # Convert price from rupees to dollars (approx 75 INR = 1 USD)
            price_usd = round(pprice / 75.0, 2)
            if price_usd < 4.99:
                price_usd = 9.99
            
            # Map names
            pname_en = pname if lang == 'English' else list(SPANISH_TRANSLATION.keys())[list(SPANISH_TRANSLATION.values()).index(pname)] if pname in SPANISH_TRANSLATION.values() else pname
            pid = pname_en.upper().replace(" ", "_").replace("-", "_")
            
            if pid not in unique_products:
                cat = get_product_category(pname_en)
                unique_products[pid] = {
                    "id": pid,
                    "English": {
                        "id": pid,
                        "name": pname_en,
                        "category": cat,
                        "description": f"High-quality {pname_en} formulated specifically for crop health protection and growth maximization.",
                        "price": price_usd,
                        "rating": round(4.4 + (hash(pname_en) % 6) * 0.1, 1),
                        "image": get_product_image(cat),
                        "image_path": f"assets/products/{pid.lower()}.png",
                        "suitability": crop_en,
                        "benefits": f"Fights crop infection, improves nutritional uptake, and increases crop yield in {crop_en}."
                    },
                    "Hindi": {
                        "id": pid,
                        "name": SPANISH_TRANSLATION.get(pname_en, pname_en) if lang == 'English' else pname,
                        "category": "उर्वरक" if cat == "Fertilizer" else ("कवकनाशी" if cat == "Fungicide" else ("कीट नियंत्रण" if cat == "Pest Control" else "मिट्टी और पोषण")),
                        "description": f"फसल स्वास्थ्य सुरक्षा और विकास को अधिकतम करने के लिए विशेष रूप से तैयार किया गया उच्च गुणवत्ता वाला {pname_en}।",
                        "price": price_usd,
                        "rating": round(4.4 + (hash(pname_en) % 6) * 0.1, 1),
                        "image": get_product_image(cat),
                        "image_path": f"assets/products/{pid.lower()}.png",
                        "suitability": data['Hindi'].get('crop', crop_en),
                        "benefits": f"संक्रमण से लड़ता है, पोषक तत्वों के अवशोषण में सुधार करता है, और उपज बढ़ाता है।"
                    },
                    "Spanish": {
                        "id": pid,
                        "name": SPANISH_TRANSLATION.get(pname_en, pname_en),
                        "category": "Fertilizante" if cat == "Fertilizer" else ("Fungicida" if cat == "Fungicide" else ("Control de Plagas" if cat == "Pest Control" else "Suelo y Nutrientes")),
                        "description": f"{SPANISH_TRANSLATION.get(pname_en, pname_en)} de alta calidad formulado específicamente para la protección de la salud del cultivo y la maximización del crecimiento.",
                        "price": price_usd,
                        "rating": round(4.4 + (hash(pname_en) % 6) * 0.1, 1),
                        "image": get_product_image(cat),
                        "image_path": f"assets/products/{pid.lower()}.png",
                        "suitability": crop_es,
                        "benefits": f"Combate la infección del cultivo, mejora la absorción nutricional y aumenta el rendimiento."
                    }
                }

# Write knowledge base JSON files
os.makedirs('knowledge_base', exist_ok=True)
with open('knowledge_base/disease_info.json', 'w', encoding='utf-8') as f:
    json.dump(kb_en, f, indent=2, ensure_ascii=False)

with open('knowledge_base/disease_info_hi.json', 'w', encoding='utf-8') as f:
    json.dump(kb_hi, f, indent=2, ensure_ascii=False)

with open('knowledge_base/disease_info_es.json', 'w', encoding='utf-8') as f:
    json.dump(kb_es, f, indent=2, ensure_ascii=False)

with open('knowledge_base/disease_info_mr.json', 'w', encoding='utf-8') as f:
    json.dump(kb_mr, f, indent=2, ensure_ascii=False)

print("Generated disease knowledge base files successfully!")

# Write products JSON files
products_en = {}
products_hi = {}
products_es = {}

for pid, prod in unique_products.items():
    products_en[pid] = prod['English']
    products_hi[pid] = prod['Hindi']
    products_es[pid] = prod['Spanish']

# Write products files
with open('src/products.json', 'w', encoding='utf-8') as f:
    json.dump(products_en, f, indent=2, ensure_ascii=False)

with open('src/products_hi.json', 'w', encoding='utf-8') as f:
    json.dump(products_hi, f, indent=2, ensure_ascii=False)

with open('src/products_es.json', 'w', encoding='utf-8') as f:
    json.dump(products_es, f, indent=2, ensure_ascii=False)

print("Generated products JSON databases successfully!")

# Build Disease to Product mapping
disease_product_mapping = {}
for class_name, data in disease_data.DISEASE_DATA.items():
    prods = data['English'].get('products', [])
    prod_ids = []
    for p in prods:
        pname_en = p['name']
        pid = pname_en.upper().replace(" ", "_").replace("-", "_")
        prod_ids.append(pid)
    disease_product_mapping[class_name] = prod_ids

print("DISEASE_PRODUCT_MAPPING:")
print(json.dumps(disease_product_mapping, indent=2))
