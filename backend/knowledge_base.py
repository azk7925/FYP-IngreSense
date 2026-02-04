INGREDIENT_KNOWLEDGE_BASE = {
    # Animal-derived ingredients
    'lanolin': {
        'synonyms': ['wool grease', 'wool wax', 'wool fat'],
        'chemical_class': 'wax_ester',
        'source': 'animal',
        'halal': 0, 'vegan': 0, 'allergen': 0.9, 'eco': 0.2,
        'reasoning': 'Derived from sheep wool; not vegan, strong allergen'
    },
    'collagen': {
        'synonyms': ['hydrolyzed collagen', 'collagen peptides'],
        'chemical_class': 'protein',
        'source': 'animal',
        'halal': 0.3, 'vegan': 0, 'allergen': 0.2, 'eco': 0.2,
        'reasoning': 'Animal protein; marine-derived may be halal but still not vegan'
    },
    'beeswax': {
        'synonyms': ['cera alba', 'white wax', 'cera flava'],
        'chemical_class': 'wax',
        'source': 'animal',
        'halal': 1, 'vegan': 0, 'allergen': 0.1, 'eco': 0.8,
        'reasoning': 'Bee product; halal but not vegan, sustainable'
    },
    'honey': {
        'synonyms': ['mel', 'bee honey'],
        'chemical_class': 'natural_sweetener',
        'source': 'animal',
        'halal': 1, 'vegan': 0, 'allergen': 0.2, 'eco': 0.8,
        'reasoning': 'Bee product; halal but not vegan'
    },
    'carmine': {
        'synonyms': ['cochineal', 'ci 75470', 'natural red 4'],
        'chemical_class': 'colorant',
        'source': 'animal',
        'halal': 0, 'vegan': 0, 'allergen': 0.3, 'eco': 0.3,
        'reasoning': 'Derived from insects; not halal or vegan'
    },
    'keratin': {
        'synonyms': ['hydrolyzed keratin'],
        'chemical_class': 'protein',
        'source': 'animal',
        'halal': 0.2, 'vegan': 0, 'allergen': 0.1, 'eco': 0.2,
        'reasoning': 'Animal protein from hair/feathers; not vegan'
    },
    'gelatin': {
        'synonyms': ['gelatine'],
        'chemical_class': 'protein',
        'source': 'animal',
        'halal': 0.1, 'vegan': 0, 'allergen': 0.1, 'eco': 0.2,
        'reasoning': 'From animal bones/skin; usually not halal or vegan'
    },
    'snail mucin': {
        'synonyms': ['snail secretion filtrate', 'snail slime'],
        'chemical_class': 'protein',
        'source': 'animal',
        'halal': 0.7, 'vegan': 0, 'allergen': 0.2, 'eco': 0.6,
        'reasoning': 'From snails; not vegan but may be halal'
    },

    # Plant-derived ingredients
    'shea butter': {
        'synonyms': ['butyrospermum parkii', 'karite butter'],
        'chemical_class': 'plant_oil',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.05, 'eco': 0.9,
        'reasoning': 'Plant-based, sustainable, very safe'
    },
    'coconut oil': {
        'synonyms': ['cocos nucifera oil', 'copra oil'],
        'chemical_class': 'plant_oil',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.3, 'eco': 0.8,
        'reasoning': 'Plant oil; potential tree nut allergen'
    },
    'aloe vera': {
        'synonyms': ['aloe barbadensis', 'aloe vera gel'],
        'chemical_class': 'plant_extract',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.1, 'eco': 0.95,
        'reasoning': 'Natural plant extract; very safe'
    },
    'jojoba oil': {
        'synonyms': ['simmondsia chinensis', 'jojoba seed oil'],
        'chemical_class': 'plant_oil',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.05, 'eco': 0.9,
        'reasoning': 'Plant-based liquid wax; very safe'
    },
    'argan oil': {
        'synonyms': ['argania spinosa oil'],
        'chemical_class': 'plant_oil',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.1, 'eco': 0.85,
        'reasoning': 'Plant oil; safe and sustainable'
    },
    'tea tree oil': {
        'synonyms': ['melaleuca alternifolia oil'],
        'chemical_class': 'essential_oil',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.4, 'eco': 0.9,
        'reasoning': 'Essential oil; can irritate sensitive skin'
    },
    'rose water': {
        'synonyms': ['rosa damascena water', 'rose hydrosol'],
        'chemical_class': 'plant_extract',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.2, 'eco': 0.9,
        'reasoning': 'Natural extract; generally safe'
    },
    'green tea extract': {
        'synonyms': ['camellia sinensis extract'],
        'chemical_class': 'plant_extract',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.1, 'eco': 0.9,
        'reasoning': 'Antioxidant extract; safe'
    },
    'chamomile extract': {
        'synonyms': ['chamomilla recutita extract'],
        'chemical_class': 'plant_extract',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.2, 'eco': 0.9,
        'reasoning': 'Soothing extract; generally safe'
    },
    'vitamin c': {
        'synonyms': ['ascorbic acid', 'l-ascorbic acid'],
        'chemical_class': 'vitamin',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.15, 'eco': 0.9,
        'reasoning': 'Plant-derived antioxidant; safe'
    },

    # Ambiguous (plant or animal source)
    'stearic acid': {
        'synonyms': ['octadecanoic acid', 'stearate', 'magnesium stearate', 'calcium stearate'],
        'chemical_class': 'fatty_acid',
        'source': 'ambiguous',
        'halal': 0, 'vegan': 0, 'allergen': 0.05, 'eco': 0.5,
        'reasoning': 'Ambiguous source (animal/plant); treating as not halal/vegan per dataset'
    },
    'oleic acid': {
        'synonyms': ['decyl oleate', 'sorbitan oleate'],
        'chemical_class': 'fatty_acid',
        'source': 'ambiguous',
        'halal': 0, 'vegan': 0.5, 'allergen': 0.05, 'eco': 0.5,
        'reasoning': 'Fatty acid; can be animal/plant-derived; not halal per dataset'
    },
    'squalene': {
        'synonyms': ['squalane'],
        'chemical_class': 'lipid',
        'source': 'ambiguous',
        'halal': 0.5, 'vegan': 0, 'allergen': 0.02, 'eco': 0.5,
        'reasoning': 'Can be shark-derived (not vegan) or plant-derived; ambiguous halal'
    },
    'lecithin': {
        'synonyms': ['soy lecithin', 'phosphatidylcholine'],
        'chemical_class': 'phospholipid',
        'source': 'ambiguous',
        'halal': 0.6, 'vegan': 0.6, 'allergen': 0.3, 'eco': 0.7,
        'reasoning': 'Usually soy-based but can be from eggs'
    },
    'ceramide': {
        'synonyms': ['ceramide np', 'ceramide ap'],
        'chemical_class': 'lipid',
        'source': 'ambiguous',
        'halal': 0.5, 'vegan': 0.5, 'allergen': 0.05, 'eco': 0.6,
        'reasoning': 'Can be plant, animal, or synthetic'
    },
    'palmitic acid': {
        'synonyms': ['hexadecanoic acid'],
        'chemical_class': 'fatty_acid',
        'source': 'ambiguous',
        'halal': 0.5, 'vegan': 0.5, 'allergen': 0.05, 'eco': 0.4,
        'reasoning': 'From palm oil or animal sources'
    },
    'glycerin': {
        'synonyms': ['glycerol', 'glycerine'],
        'chemical_class': 'alcohol',
        'source': 'ambiguous',
        'halal': 0.5, 'vegan': 0.5, 'allergen': 0.02, 'eco': 0.6,
        'reasoning': 'Usually plant-based but needs verification'
    },

    # Synthetic/Lab-made ingredients
    'dimethicone': {
        'synonyms': ['polydimethylsiloxane', 'pdms'],
        'chemical_class': 'silicone',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.02, 'eco': 0.2,
        'reasoning': 'Synthetic silicone; not biodegradable'
    },
    'cyclopentasiloxane': {
        'synonyms': ['d5', 'cyclomethicone', 'cyclohexasiloxane'],
        'chemical_class': 'silicone',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.02, 'eco': 0.15,
        'reasoning': 'Volatile silicone; environmental concerns'
    },
    'parabens': {
        'synonyms': ['methylparaben', 'propylparaben', 'butylparaben'],
        'chemical_class': 'preservative',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.4, 'eco': 0.2,
        'reasoning': 'Synthetic preservative; controversial'
    },
    'phenoxyethanol': {
        'synonyms': ['phenoxetol'],
        'chemical_class': 'preservative',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.25, 'eco': 0.4,
        'reasoning': 'Synthetic preservative; potential irritant'
    },
    'sodium lauryl sulfate': {
        'synonyms': ['sls', 'sodium dodecyl sulfate'],
        'chemical_class': 'surfactant',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.6, 'eco': 0.3,
        'reasoning': 'Harsh surfactant; can irritate'
    },
    'sodium laureth sulfate': {
        'synonyms': ['sles'],
        'chemical_class': 'surfactant',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.4, 'eco': 0.3,
        'reasoning': 'Milder than SLS but still potential irritant'
    },
    'peg compounds': {
        'synonyms': ['polyethylene glycol', 'peg-100', 'peg-8', 'peg-9', 'peg-40', 'peg-75', 'peg/ppg'],
        'chemical_class': 'polymer',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.3, 'eco': 0.3,
        'reasoning': 'Synthetic polymers; environmental concerns'
    },
    'petrolatum': {
        'synonyms': ['petroleum jelly', 'mineral oil jelly'],
        'chemical_class': 'petroleum_derivative',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.05, 'eco': 0.1,
        'reasoning': 'Petroleum-based; not eco-friendly'
    },
    'mineral oil': {
        'synonyms': ['paraffinum liquidum', 'liquid paraffin'],
        'chemical_class': 'petroleum_derivative',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.05, 'eco': 0.1,
        'reasoning': 'Petroleum-based; not biodegradable'
    },
    'paraffin': {
        'synonyms': ['paraffin wax', 'isohexadecane', 'isoparaffin'],
        'chemical_class': 'petroleum_derivative',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.05, 'eco': 0.1,
        'reasoning': 'Petroleum-based wax; not eco-friendly'
    },

    # Allergen-prone ingredients
    'fragrance': {
        'synonyms': ['parfum', 'perfume'],
        'chemical_class': 'fragrance',
        'source': 'ambiguous',
        'halal': 0.5, 'vegan': 0.5, 'allergen': 0.95, 'eco': 0.3,
        'reasoning': 'Mixed ingredients; major allergen'
    },
    'limonene': {
        'synonyms': ['d-limonene'],
        'chemical_class': 'terpene',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.7, 'eco': 0.9,
        'reasoning': 'Natural; can cause allergies when oxidized'
    },
    'linalool': {
        'synonyms': ['linalyl alcohol'],
        'chemical_class': 'terpene_alcohol',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.65, 'eco': 0.9,
        'reasoning': 'Natural fragrance; potential allergen'
    },
    'citral': {
        'synonyms': ['lemonal'],
        'chemical_class': 'terpene',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.6, 'eco': 0.9,
        'reasoning': 'Citrus fragrance; potential allergen'
    },
    'geraniol': {
        'synonyms': [],
        'chemical_class': 'terpene_alcohol',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.6, 'eco': 0.9,
        'reasoning': 'Floral fragrance; potential allergen'
    },
    'eugenol': {
        'synonyms': [],
        'chemical_class': 'phenylpropanoid',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.65, 'eco': 0.9,
        'reasoning': 'Spice fragrance; potential allergen'
    },
    'cinnamal': {
        'synonyms': ['cinnamaldehyde'],
        'chemical_class': 'aldehyde',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.7, 'eco': 0.85,
        'reasoning': 'Cinnamon fragrance; known allergen'
    },
    'citronellol': {
        'synonyms': [],
        'chemical_class': 'terpene_alcohol',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.6, 'eco': 0.9,
        'reasoning': 'Natural fragrance; potential allergen'
    },

    # Vitamins and active ingredients
    'hyaluronic acid': {
        'synonyms': ['sodium hyaluronate', 'hyaluronan', 'hydrolyzed hyaluronic acid'],
        'chemical_class': 'polysaccharide',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.02, 'eco': 0.95,
        'reasoning': 'Bacterial fermentation; very safe'
    },
    'niacinamide': {
        'synonyms': ['vitamin b3', 'nicotinamide'],
        'chemical_class': 'vitamin',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.05, 'eco': 0.95,
        'reasoning': 'Synthetic vitamin; very safe'
    },
    'retinol': {
        'synonyms': ['vitamin a', 'retinyl palmitate'],
        'chemical_class': 'vitamin',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.35, 'eco': 0.9,
        'reasoning': 'Synthetic; may irritate sensitive skin'
    },
    'tocopherol': {
        'synonyms': ['vitamin e', 'tocopheryl acetate', 'tocopheryl succinate'],
        'chemical_class': 'vitamin',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.05, 'eco': 0.95,
        'reasoning': 'Plant-derived antioxidant; very safe'
    },
    'salicylic acid': {
        'synonyms': ['bha', 'beta hydroxy acid'],
        'chemical_class': 'hydroxy_acid',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.3, 'eco': 0.85,
        'reasoning': 'Synthetic exfoliant; can irritate'
    },
    'glycolic acid': {
        'synonyms': ['aha', 'alpha hydroxy acid'],
        'chemical_class': 'hydroxy_acid',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.35, 'eco': 0.85,
        'reasoning': 'Synthetic exfoliant; can irritate'
    },
    'lactic acid': {
        'synonyms': [],
        'chemical_class': 'hydroxy_acid',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.3, 'eco': 0.85,
        'reasoning': 'AHA exfoliant; can irritate'
    },
    'peptides': {
        'synonyms': ['palmitoyl pentapeptide', 'matrixyl', 'oligopeptide', 'polypeptide', 'hexapeptide', 'heptapeptide', 'tetrapeptide', 'tripeptide'],
        'chemical_class': 'peptide',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.05, 'eco': 0.85,
        'reasoning': 'Synthetic peptides; generally safe'
    },
    'caffeine': {
        'synonyms': [],
        'chemical_class': 'alkaloid',
        'source': 'plant',
        'halal': 1, 'vegan': 1, 'allergen': 0.1, 'eco': 0.85,
        'reasoning': 'Plant extract; safe'
    },

    # Alcohol-based ingredients
    'alcohol denat': {
        'synonyms': ['denatured alcohol', 'sd alcohol'],
        'chemical_class': 'alcohol',
        'source': 'synthetic',
        'halal': 0.1, 'vegan': 1, 'allergen': 0.5, 'eco': 0.6,
        'reasoning': 'Denatured ethanol; not halal, can dry skin'
    },
    'ethanol': {
        'synonyms': ['ethyl alcohol', 'alcohol'],
        'chemical_class': 'alcohol',
        'source': 'synthetic',
        'halal': 0.1, 'vegan': 1, 'allergen': 0.45, 'eco': 0.6,
        'reasoning': 'Ethanol; not halal, can dry skin'
    },
    'benzyl alcohol': {
        'synonyms': [],
        'chemical_class': 'aromatic_alcohol',
        'source': 'synthetic',
        'halal': 1, 'vegan': 1, 'allergen': 0.3, 'eco': 0.7,
        'reasoning': 'Preservative alcohol; potential irritant'
    },
    'cetyl alcohol': {
        'synonyms': ['palmityl alcohol'],
        'chemical_class': 'fatty_alcohol',
        'source': 'ambiguous',
        'halal': 0.7, 'vegan': 0.7, 'allergen': 0.05, 'eco': 0.7,
        'reasoning': 'Fatty alcohol; usually plant-based, safe'
    },
    'stearyl alcohol': {
        'synonyms': [],
        'chemical_class': 'fatty_alcohol',
        'source': 'ambiguous',
        'halal': 0.7, 'vegan': 0.7, 'allergen': 0.05, 'eco': 0.7,
        'reasoning': 'Fatty alcohol; usually plant-based, safe'
    },
    'cetearyl alcohol': {
        'synonyms': [],
        'chemical_class': 'fatty_alcohol',
        'source': 'ambiguous',
        'halal': 0.7, 'vegan': 0.7, 'allergen': 0.05, 'eco': 0.7,
        'reasoning': 'Mix of cetyl and stearyl; usually safe'
    },

    # Common base ingredients
    'water': {
        'synonyms': ['aqua', 'eau'],
        'chemical_class': 'solvent',
        'source': 'natural',
        'halal': 1, 'vegan': 1, 'allergen': 0, 'eco': 1,
        'reasoning': 'Water; completely safe'
    },
    'silica': {
        'synonyms': ['silicon dioxide'],
        'chemical_class': 'mineral',
        'source': 'natural',
        'halal': 1, 'vegan': 1, 'allergen': 0.05, 'eco': 0.9,
        'reasoning': 'Natural mineral; safe'
    },
}
