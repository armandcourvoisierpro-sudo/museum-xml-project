# -*- coding: utf-8 -*-
"""
SYNTHETIC / FICTIONAL dataset generator for the Museum & Cultural Heritage
Management Platform (DSTI S26 Data Pipeline Part 1).

This data is entirely invented for schema development and testing.
It is NOT sourced from any real museum, archive, or public dataset,
and must not be presented as such.

Design notes (why the data looks the way it does):
- Artifacts are grouped into 10 thematic "acquisition groups" (European
  paintings, Egyptian antiquities, Greek/Roman antiquities, Chinese art,
  Japanese art, Pre-Columbian, African art, textiles, manuscripts,
  photography/jewelry) so that period/site/artist/collection references
  are internally consistent rather than randomly assigned.
- Ancient/archaeological artifacts (Egyptian, Greek/Roman, Pre-Columbian)
  are mostly anonymous (no artistRef) and DO have a siteRef, reflecting
  real museum cataloguing practice.
- Studio-made works (paintings, photographs, modern jewelry) are mostly
  attributed (artistRef present) and do NOT have a siteRef, since they
  were not excavated from a findspot.
- collectionRef and artistRef stay single-valued per artifact, matching
  the existing XSD (1:N Collection->Artifact, 1:N Artist->Artifact).
  The existing XSD does NOT support Artifact<->Collection or
  Artifact<->Artist as many-to-many, so this generator does not attempt
  to fabricate that -- see SCHEMA_REVIEW.md for the recommendation.
- Artifact<->Exhibition and Visitor<->Exhibition ARE many-to-many in the
  existing XSD (via the FeaturedArtifact and Visit join elements), so
  several artifacts deliberately appear in more than one exhibition.
"""
import random
from datetime import date, timedelta
from xml.etree import ElementTree as ET
from xml.dom import minidom

random.seed(42)  # fixed seed: reproducible, not "random nonsense"

# ---------------------------------------------------------------------------
# 1. HISTORICAL PERIODS
# ---------------------------------------------------------------------------
historical_periods = [
    dict(id="HP-001", name="New Kingdom of Egypt", startYear=-1550, endYear=-1070,
         description="Era of major pharaonic construction and elaborate funerary practices in ancient Egypt."),
    dict(id="HP-002", name="Classical Antiquity (Greece)", startYear=-480, endYear=-323,
         description="Height of Greek philosophy, drama, and classical sculpture, from the Persian Wars to the death of Alexander the Great."),
    dict(id="HP-003", name="Roman Empire", startYear=-27, endYear=476,
         description="From the reign of Augustus to the fall of the Western Roman Empire."),
    dict(id="HP-004", name="Tang Dynasty", startYear=618, endYear=907,
         description="A golden age of Chinese art, poetry, and ceramic innovation."),
    dict(id="HP-005", name="Heian Period", startYear=794, endYear=1185,
         description="Japanese imperial court culture centered in Kyoto, known for refined aesthetics."),
    dict(id="HP-006", name="Edo Period", startYear=1603, endYear=1868,
         description="Period of Japanese history under Tokugawa shogunate rule, marked by stability and artistic flourishing."),
    dict(id="HP-007", name="Italian Renaissance", startYear=1400, endYear=1600,
         description="Revival of classical learning and the arts across the Italian city-states."),
    dict(id="HP-008", name="Baroque", startYear=1600, endYear=1750,
         description="Dramatic, ornate artistic style that spread across Catholic Europe."),
    dict(id="HP-009", name="Neoclassicism", startYear=1760, endYear=1830,
         description="Return to classical restraint following the excesses of the Baroque and Rococo."),
    dict(id="HP-010", name="Impressionism", startYear=1860, endYear=1900,
         description="French movement characterized by visible brushwork and emphasis on light."),
    dict(id="HP-011", name="Teotihuacan Classic Period", startYear=100, endYear=550,
         description="Height of the Mesoamerican city of Teotihuacan, predating the Aztec Empire."),
    dict(id="HP-012", name="Benin Kingdom Golden Age", startYear=1400, endYear=1700,
         description="Height of the Kingdom of Benin's bronze- and ivory-casting traditions in West Africa."),
    dict(id="HP-013", name="Inca Imperial Era", startYear=1438, endYear=1533,
         description="Expansion and height of the Inca Empire in the Andes, prior to Spanish conquest."),
    dict(id="HP-014", name="Medieval European Age", startYear=500, endYear=1400,
         description="Early through late Middle Ages in Europe, encompassing monastic manuscript production."),
    dict(id="HP-015", name="Modern Era", startYear=1850, endYear=1950,
         description="19th-20th century period encompassing the birth and early development of photography as an art form."),
]

# ---------------------------------------------------------------------------
# 2. CULTURAL SITES
# ---------------------------------------------------------------------------
cultural_sites = [
    dict(id="CS-001", name="Valley of the Kings", country="Egypt", region="Luxor Governorate",
         description="Royal necropolis on the Nile's west bank, burial site of New Kingdom pharaohs."),
    dict(id="CS-002", name="Pompeii", country="Italy", region="Campania",
         description="Roman city buried by the eruption of Mount Vesuvius in 79 CE."),
    dict(id="CS-003", name="Athens Acropolis", country="Greece", region="Attica",
         description="Fortified hilltop complex containing the Parthenon and other classical monuments."),
    dict(id="CS-004", name="Ephesus", country="Turkey", region="Izmir Province",
         description="Ancient Greek and later Roman port city on the Ionian coast."),
    dict(id="CS-005", name="Forbidden City", country="China", region="Beijing Municipality",
         description="Former Chinese imperial palace complex."),
    dict(id="CS-006", name="Kyoto Imperial Palace", country="Japan", region="Kansai Region",
         description="Former residence of the Japanese Imperial family."),
    dict(id="CS-007", name="Nara", country="Japan", region="Kansai Region",
         description="Japan's first permanent capital, home to early Buddhist temples."),
    dict(id="CS-008", name="Teotihuacan", country="Mexico", region="State of Mexico",
         description="Pre-Aztec Mesoamerican city famed for its pyramids."),
    dict(id="CS-009", name="Machu Picchu", country="Peru", region="Cusco Region",
         description="15th-century Inca citadel set high in the Andes."),
    dict(id="CS-010", name="Benin City", country="Nigeria", region="Edo State",
         description="Historic capital of the Kingdom of Benin, renowned for bronze casting."),
    dict(id="CS-011", name="Angkor", country="Cambodia", region="Siem Reap Province",
         description="Khmer Empire capital and temple complex."),
    dict(id="CS-012", name="Great Zimbabwe", country="Zimbabwe", region="Masvingo Province",
         description="Medieval stone city complex of the Kingdom of Zimbabwe."),
]

# ---------------------------------------------------------------------------
# 3. ARTISTS  (many artifacts deliberately have NO artistRef -- see notes)
# ---------------------------------------------------------------------------
artists = [
    dict(id="ARTIST-001", name="Lorenzo Bellandi", birthYear=1470, deathYear=1538, nationality="Italian",
         biography="Florentine painter known for religious altarpieces and portraiture during the height of the Renaissance."),
    dict(id="ARTIST-002", name="Isabetta Contarini", birthYear=1488, deathYear=1550, nationality="Italian",
         biography="Venetian painter noted for portraits of noblewomen, rare among documented women artists of her era."),
    dict(id="ARTIST-003", name="Willem van der Beek", birthYear=1596, deathYear=1661, nationality="Dutch",
         biography="Baroque painter working in Amsterdam, specializing in still life and interior scenes."),
    dict(id="ARTIST-004", name="Henri Cazalis", birthYear=1768, deathYear=1825, nationality="French",
         biography="Neoclassical painter and sculptor associated with the French Academy."),
    dict(id="ARTIST-005", name="Marguerite Dufresne", birthYear=1841, deathYear=1912, nationality="French",
         biography="Impressionist painter known for outdoor scenes of the Seine valley."),
    dict(id="ARTIST-006", name="Etienne Vasseur", birthYear=1855, deathYear=1901, nationality="French",
         biography="Impressionist painter and printmaker."),
    dict(id="ARTIST-007", name="Giulia Moretti", birthYear=1610, deathYear=1675, nationality="Italian",
         biography="Baroque sculptor active in Rome, known for marble portrait busts."),
    dict(id="ARTIST-008", name="Pieter Aalsmeer", birthYear=1600, deathYear=1667, nationality="Dutch",
         biography="Baroque painter, contemporary of van der Beek, active in the Amsterdam guild."),
    dict(id="ARTIST-009", name="Zhang Wei", birthYear=682, deathYear=756, nationality="Chinese",
         biography="Tang-dynasty court painter credited with several surviving silk paintings."),
    dict(id="ARTIST-010", name="Li Rong", birthYear=705, deathYear=770, nationality="Chinese",
         biography="Tang-dynasty ceramic master associated with the imperial kilns."),
    dict(id="ARTIST-011", name="Fujiwara no Michika", birthYear=None, deathYear=None, nationality="Japanese",
         biography="Heian-period court painter; exact dates not recorded in surviving sources."),
    dict(id="ARTIST-012", name="Hasegawa Tokan", birthYear=1610, deathYear=1674, nationality="Japanese",
         biography="Edo-period lacquer artist known for maki-e technique."),
    dict(id="ARTIST-013", name="Kobori Naoyuki", birthYear=1789, deathYear=1858, nationality="Japanese",
         biography="Edo-period ceramicist associated with the Kyoto kilns."),
    dict(id="ARTIST-014", name="Osaretin Iyare", birthYear=None, deathYear=None, nationality="Edo (Nigerian)",
         biography="Benin court bronze-caster; individual attribution is rare as most works were produced collectively within royal guilds."),
    dict(id="ARTIST-015", name="Adesuwa Igbinovia", birthYear=None, deathYear=None, nationality="Edo (Nigerian)",
         biography="Ivory carver attributed by museum records to the Benin royal workshops."),
    dict(id="ARTIST-016", name="Rosalind Fairweather", birthYear=1862, deathYear=1938, nationality="British",
         biography="Pioneering documentary photographer known for urban street scenes."),
    dict(id="ARTIST-017", name="Kenji Amano", birthYear=1878, deathYear=1945, nationality="Japanese",
         biography="Early 20th-century portrait and landscape photographer."),
    dict(id="ARTIST-018", name="Thomas Whitfield", birthYear=1870, deathYear=1951, nationality="American",
         biography="Photographer known for architectural and industrial subjects."),
    dict(id="ARTIST-019", name="Consuelo Herrera", birthYear=1902, deathYear=1978, nationality="Spanish",
         biography="Textile designer and weaver active in Madrid's decorative arts workshops."),
    dict(id="ARTIST-020", name="Amara Diallo", birthYear=None, deathYear=None, nationality="Malian",
         biography="Master weaver credited by regional oral history with several surviving textile pieces."),
    dict(id="ARTIST-021", name="Brother Anselm of Cluny", birthYear=None, deathYear=None, nationality="French",
         biography="Monastic scribe and illuminator; exact dates unrecorded."),
    dict(id="ARTIST-022", name="Ibn al-Katib", birthYear=None, deathYear=None, nationality="Andalusian",
         biography="Calligrapher active in the manuscript workshops of Al-Andalus."),
    dict(id="ARTIST-023", name="Sister Beatrix of Tyrol", birthYear=None, deathYear=None, nationality="Austrian",
         biography="Manuscript illuminator associated with an Alpine convent scriptorium."),
    dict(id="ARTIST-024", name="Marcus Alderton", birthYear=1925, deathYear=2004, nationality="British",
         biography="Modern goldsmith and jeweler known for mid-century decorative commissions."),
    dict(id="ARTIST-025", name="Kallias of Corinth", birthYear=-420, deathYear=-350, nationality="Greek",
         biography="Sculptor active in Corinth, known through an inscribed signature on surviving works."),
]

# ---------------------------------------------------------------------------
# 4. CURATORS
# ---------------------------------------------------------------------------
curators = [
    dict(id="CUR-001", name="Margaret Sinclair", department="Paintings & Sculpture",
         email="m.sinclair@museum.org", hireDate="2015-03-02"),
    dict(id="CUR-002", name="Rania Haddad", department="Antiquities & Archaeology",
         email="r.haddad@museum.org", hireDate="2011-08-14"),
    dict(id="CUR-003", name="Wei Chen", department="Asian Art",
         email="w.chen@museum.org", hireDate="2018-01-22"),
    dict(id="CUR-004", name="Isabel Duarte", department="Textiles & Costume",
         email="i.duarte@museum.org", hireDate="2019-09-10"),
    dict(id="CUR-005", name="Nathaniel Brooks", department="Photography & Modern Art",
         email="n.brooks@museum.org", hireDate="2020-06-01"),
    dict(id="CUR-006", name="Adaeze Nwosu", department="Decorative Arts",
         email="a.nwosu@museum.org", hireDate="2013-11-27"),
]

# ---------------------------------------------------------------------------
# 5. COLLECTIONS
# ---------------------------------------------------------------------------
collections = [
    dict(id="COL-001", name="European Old Masters", curatorRef="CUR-001",
         theme="European painting and sculpture, 15th-19th century",
         description="Core holdings of Renaissance, Baroque, Neoclassical and Impressionist works."),
    dict(id="COL-002", name="Ancient Egyptian Antiquities", curatorRef="CUR-002",
         theme="Funerary and ceremonial objects from Dynastic Egypt", description=None),
    dict(id="COL-003", name="Classical Greek & Roman Antiquities", curatorRef="CUR-002",
         theme="Sculpture, ceramics and jewelry from the Greco-Roman world", description=None),
    dict(id="COL-004", name="Chinese Art & Ceramics", curatorRef="CUR-003",
         theme="Ceramics and paintings from Imperial China",
         description="Focused primarily on Tang-dynasty court and kiln production."),
    dict(id="COL-005", name="Japanese Art & Artifacts", curatorRef="CUR-003",
         theme="Decorative arts of the Heian and Edo periods", description=None),
    dict(id="COL-006", name="Pre-Columbian Art", curatorRef="CUR-002",
         theme="Artifacts from Mesoamerican and Andean civilizations",
         description="Includes material associated with Teotihuacan and the Inca Empire."),
    dict(id="COL-007", name="African Art & Artifacts", curatorRef="CUR-006",
         theme="Bronze, ivory, and stonework from West and Southern Africa", description=None),
    dict(id="COL-008", name="Textiles & Costume Heritage", curatorRef="CUR-004",
         theme="Woven and embroidered textiles from multiple cultures", description=None),
    dict(id="COL-009", name="Manuscripts & Rare Books", curatorRef="CUR-006",
         theme="Illuminated manuscripts and historical documents",
         description="Spans monastic European scriptoria and Andalusian calligraphic traditions."),
    dict(id="COL-010", name="Modern Photography Collection", curatorRef="CUR-005",
         theme="Photographic works from the late 19th and 20th centuries", description=None),
    dict(id="COL-011", name="Decorative Arts & Jewelry", curatorRef="CUR-006",
         theme="Jewelry and small decorative objects across periods", description=None),
]

# ---------------------------------------------------------------------------
# 6. ARTIFACTS (83 records total, grouped by acquisition theme)
# ---------------------------------------------------------------------------
TYPE_PAINTING, TYPE_SCULPTURE, TYPE_CERAMIC, TYPE_TEXTILE = "Painting", "Sculpture", "Ceramic", "Textile"
TYPE_MANUSCRIPT, TYPE_PHOTO, TYPE_JEWELRY, TYPE_OTHER = "Manuscript", "Photograph", "Jewelry", "Other"

artifacts = []

# --- Group 1: European Old Masters (15) -----------------------------------
group1 = [
    ("Portrait of a Florentine Merchant", TYPE_PAINTING, 1498, "ARTIST-001"),
    ("Madonna of the Orchard", TYPE_PAINTING, 1505, "ARTIST-001"),
    ("Portrait of Contessa Alvise", TYPE_PAINTING, 1522, "ARTIST-002"),
    ("Still Life with Lemons and Pewter", TYPE_PAINTING, 1631, "ARTIST-003"),
    ("Interior with a Woman Reading", TYPE_PAINTING, 1648, "ARTIST-003"),
    ("Allegory of Autumn", TYPE_PAINTING, 1655, "ARTIST-008"),
    ("Bust of a Roman Senator (after the Antique)", TYPE_SCULPTURE, 1798, "ARTIST-004"),
    ("Study for the Monument to Reason", TYPE_SCULPTURE, 1805, "ARTIST-004"),
    ("Morning on the Seine at Argenteuil", TYPE_PAINTING, 1875, "ARTIST-005"),
    ("Poplars in Late Summer Light", TYPE_PAINTING, 1882, "ARTIST-005"),
    ("The Boulevard at Dusk", TYPE_PAINTING, 1889, "ARTIST-006"),
    ("Portrait Bust of Cardinal Farnetti", TYPE_SCULPTURE, 1652, "ARTIST-007"),
    ("Unattributed Flemish Landscape", TYPE_PAINTING, 1610, None),
    ("Studio Copy after a Venetian Altarpiece", TYPE_PAINTING, 1540, None),
    ("Fragment of a Marble Relief, Workshop of Rome", TYPE_SCULPTURE, 1660, None),
]
conditions_g1 = ["Good","Excellent","Good","Fair","Good","Fair","Good","Excellent",
                 "Excellent","Excellent","Good","Fair","Poor","Fair","Fair"]
for i, (name, typ, year, art) in enumerate(group1):
    artifacts.append(dict(
        id=f"OBJ-{len(artifacts)+1:04d}", name=name, type=typ, creationYear=year,
        condition=conditions_g1[i],
        description=None, acquisitionDate=None,
        artistRef=art, periodRef=("HP-007" if year < 1600 else "HP-008" if year < 1760 else
                                    "HP-009" if year < 1830 else "HP-010"),
        siteRef=None, collectionRef="COL-001",
    ))

# --- Group 2: Ancient Egyptian Antiquities (8) -----------------------------
group2 = [
    ("Canopic Jar of Nebamun", TYPE_CERAMIC, "Fair"),
    ("Funerary Mask Fragment", TYPE_OTHER, "Poor"),
    ("Faience Shabti Figure", TYPE_CERAMIC, "Good"),
    ("Gold Amulet in the Form of a Scarab", TYPE_JEWELRY, "Excellent"),
    ("Painted Wooden Sarcophagus Panel", TYPE_OTHER, "Critical"),
    ("Papyrus Fragment, Book of the Dead", TYPE_MANUSCRIPT, "Poor"),
    ("Limestone Offering Stela", TYPE_SCULPTURE, "Fair"),
    ("Alabaster Canopic Chest", TYPE_OTHER, "Good"),
]
for name, typ, cond in group2:
    artifacts.append(dict(
        id=f"OBJ-{len(artifacts)+1:04d}", name=name, type=typ, creationYear=-1300,
        condition=cond, description=None, acquisitionDate=None,
        artistRef=None, periodRef="HP-001", siteRef="CS-001", collectionRef="COL-002",
    ))

# --- Group 3: Classical Greek & Roman Antiquities (10) ---------------------
group3 = [
    ("Red-Figure Amphora Depicting Athletes", TYPE_CERAMIC, -450, "HP-002", "CS-003", None, "Good"),
    ("Marble Head of a Youth", TYPE_SCULPTURE, -380, "HP-002", "CS-003", "ARTIST-025", "Fair"),
    ("Bronze Hydria with Palmette Handle", TYPE_OTHER, -420, "HP-002", "CS-004", None, "Good"),
    ("Terracotta Votive Figurine", TYPE_CERAMIC, -400, "HP-002", "CS-003", None, "Fair"),
    ("Gold Wreath, Funerary Offering", TYPE_JEWELRY, -350, "HP-002", "CS-004", None, "Excellent"),
    ("Mosaic Fragment from a Villa Floor", TYPE_OTHER, 120, "HP-003", "CS-002", None, "Poor"),
    ("Marble Portrait Bust of a Roman Matron", TYPE_SCULPTURE, 90, "HP-003", "CS-002", None, "Good"),
    ("Bronze Oil Lamp with Theatrical Mask Motif", TYPE_OTHER, 150, "HP-003", "CS-002", None, "Excellent"),
    ("Glass Cinerary Urn", TYPE_OTHER, 60, "HP-003", "CS-002", None, "Fair"),
    ("Fresco Fragment, Garden Scene", TYPE_OTHER, 70, "HP-003", "CS-002", None, "Critical"),
]
for name, typ, year, per, site, art, cond in group3:
    artifacts.append(dict(
        id=f"OBJ-{len(artifacts)+1:04d}", name=name, type=typ, creationYear=year,
        condition=cond, description=None, acquisitionDate=None,
        artistRef=art, periodRef=per, siteRef=site, collectionRef="COL-003",
    ))

# --- Group 4a: Chinese Art & Ceramics (7) -----------------------------------
group4a = [
    ("Sancai-Glazed Tomb Horse", TYPE_CERAMIC, 720, "ARTIST-010", "Good"),
    ("Silk Handscroll, Court Ladies at Leisure", TYPE_PAINTING, 745, "ARTIST-009", "Fair"),
    ("Celadon Ewer with Lotus Motif", TYPE_CERAMIC, 780, None, "Excellent"),
    ("White Porcelain Bowl, Xing Kiln", TYPE_CERAMIC, 700, None, "Excellent"),
    ("Painted Guardian Figure (Lokapala)", TYPE_SCULPTURE, 730, None, "Good"),
    ("Bronze Mirror with Grapevine Design", TYPE_OTHER, 690, None, "Good"),
    ("Fragmentary Wall Painting, Court Scene", TYPE_PAINTING, 810, None, "Poor"),
]
for name, typ, year, art, cond in group4a:
    artifacts.append(dict(
        id=f"OBJ-{len(artifacts)+1:04d}", name=name, type=typ, creationYear=year,
        condition=cond, description=None, acquisitionDate=None,
        artistRef=art, periodRef="HP-004", siteRef="CS-005", collectionRef="COL-004",
    ))

# --- Group 4b: Japanese Art & Artifacts (5) ---------------------------------
group4b = [
    ("Illustrated Handscroll, Court Poetry", TYPE_MANUSCRIPT, 1120, "HP-005", "CS-006", "ARTIST-011", "Fair"),
    ("Lacquered Writing Box (Maki-e)", TYPE_OTHER, 1650, "HP-006", "CS-006", "ARTIST-012", "Excellent"),
    ("Raku Tea Bowl", TYPE_CERAMIC, 1820, "HP-006", "CS-007", "ARTIST-013", "Good"),
    ("Screen Painting, Autumn Grasses", TYPE_PAINTING, 1680, "HP-006", "CS-006", None, "Good"),
    ("Silk Kosode with Chrysanthemum Pattern", TYPE_TEXTILE, 1790, "HP-006", "CS-007", None, "Fair"),
]
for name, typ, year, per, site, art, cond in group4b:
    artifacts.append(dict(
        id=f"OBJ-{len(artifacts)+1:04d}", name=name, type=typ, creationYear=year,
        condition=cond, description=None, acquisitionDate=None,
        artistRef=art, periodRef=per, siteRef=site, collectionRef="COL-005",
    ))

# --- Group 5: Pre-Columbian Art (8) -----------------------------------------
group5 = [
    ("Painted Tripod Vessel, Feathered Serpent Motif", TYPE_CERAMIC, 350, "HP-011", "CS-008", "Fair"),
    ("Stone Mask, Funerary Offering", TYPE_SCULPTURE, 400, "HP-011", "CS-008", "Good"),
    ("Obsidian Blade Set", TYPE_OTHER, 300, "HP-011", "CS-008", "Excellent"),
    ("Ceramic Incense Burner, Effigy Form", TYPE_CERAMIC, 450, "HP-011", "CS-008", "Poor"),
    ("Gold Alloy Ceremonial Beaker (Qero)", TYPE_JEWELRY, 1480, "HP-013", "CS-009", "Excellent"),
    ("Woven Tunic Fragment, Andean Highlands", TYPE_TEXTILE, 1490, "HP-013", "CS-009", "Poor"),
    ("Carved Stone Ceremonial Knife (Tumi)", TYPE_OTHER, 1470, "HP-013", "CS-009", "Good"),
    ("Silver Figurine, Miniature Offering", TYPE_JEWELRY, 1500, "HP-013", "CS-009", "Good"),
]
for name, typ, year, per, site, cond in group5:
    artifacts.append(dict(
        id=f"OBJ-{len(artifacts)+1:04d}", name=name, type=typ, creationYear=year,
        condition=cond, description=None, acquisitionDate=None,
        artistRef=None, periodRef=per, siteRef=site, collectionRef="COL-006",
    ))

# --- Group 6: African Art & Artifacts (8: 6 Benin + 2 Great Zimbabwe) ------
group6 = [
    ("Bronze Plaque, Court Ceremony Scene", TYPE_OTHER, 1550, "ARTIST-014", "Good"),
    ("Bronze Commemorative Head of an Oba", TYPE_SCULPTURE, 1600, "ARTIST-014", "Excellent"),
    ("Carved Ivory Hip Mask", TYPE_OTHER, 1550, "ARTIST-015", "Fair"),
    ("Bronze Ceremonial Bell", TYPE_OTHER, 1620, None, "Good"),
    ("Coral-Beaded Regalia Fragment", TYPE_JEWELRY, 1630, None, "Fair"),
    ("Cast Bronze Leopard Figure", TYPE_SCULPTURE, 1580, None, "Good"),
]
for name, typ, year, art, cond in group6:
    artifacts.append(dict(
        id=f"OBJ-{len(artifacts)+1:04d}", name=name, type=typ, creationYear=year,
        condition=cond, description=None, acquisitionDate=None,
        artistRef=art, periodRef="HP-012", siteRef="CS-010", collectionRef="COL-007",
    ))
group6_zim = [
    ("Soapstone Bird Effigy", TYPE_SCULPTURE, "Good"),
    ("Carved Soapstone Bowl Fragment", TYPE_OTHER, "Poor"),
]
for name, typ, cond in group6_zim:
    artifacts.append(dict(
        id=f"OBJ-{len(artifacts)+1:04d}", name=name, type=typ, creationYear=1350,
        condition=cond, description=None, acquisitionDate=None,
        artistRef=None, periodRef=None, siteRef="CS-012", collectionRef="COL-007",
    ))

# --- Group 7: Textiles & Costume Heritage (6) -------------------------------
group7 = [
    ("Embroidered Silk Shawl", TYPE_TEXTILE, 1930, "ARTIST-019", None, "Excellent"),
    ("Woven Cotton Bogolan Cloth", TYPE_TEXTILE, 1960, "ARTIST-020", None, "Good"),
    ("Wool Tapestry Fragment, Floral Border", TYPE_TEXTILE, 1710, None, "HP-014", "Fair"),
    ("Embroidered Ceremonial Vestment", TYPE_TEXTILE, 1580, None, "HP-007", "Fair"),
    ("Printed Cotton Panel, Trade Textile", TYPE_TEXTILE, 1890, None, None, "Good"),
    ("Silk Brocade Fragment", TYPE_TEXTILE, 1650, None, "HP-008", "Poor"),
]
for name, typ, year, art, per, cond in group7:
    artifacts.append(dict(
        id=f"OBJ-{len(artifacts)+1:04d}", name=name, type=typ, creationYear=year,
        condition=cond, description=None, acquisitionDate=None,
        artistRef=art, periodRef=per, siteRef=None, collectionRef="COL-008",
    ))

# --- Group 8: Manuscripts & Rare Books (6) ----------------------------------
group8 = [
    ("Illuminated Psalter Leaf", TYPE_MANUSCRIPT, 1250, "ARTIST-021", "Fair"),
    ("Book of Hours, Marginal Illumination", TYPE_MANUSCRIPT, 1420, None, "Good"),
    ("Andalusian Qur'an Fragment", TYPE_MANUSCRIPT, 1180, "ARTIST-022", "Good"),
    ("Alpine Convent Antiphonal Leaf", TYPE_MANUSCRIPT, 1310, "ARTIST-023", "Fair"),
    ("Monastic Chronicle Fragment", TYPE_MANUSCRIPT, 1050, None, "Poor"),
    ("Charter Document with Wax Seal", TYPE_MANUSCRIPT, 1390, None, "Good"),
]
for name, typ, year, art, cond in group8:
    artifacts.append(dict(
        id=f"OBJ-{len(artifacts)+1:04d}", name=name, type=typ, creationYear=year,
        condition=cond, description=None, acquisitionDate=None,
        artistRef=art, periodRef="HP-014", siteRef=None, collectionRef="COL-009",
    ))

# --- Group 9: Modern Photography (6) ----------------------------------------
group9 = [
    ("Market Street at Dawn", 1901, "ARTIST-016"),
    ("Portrait of a Dockworker", 1908, "ARTIST-016"),
    ("Cherry Blossoms, Kyoto Station", 1922, "ARTIST-017"),
    ("Rice Terraces at Sunset", 1930, "ARTIST-017"),
    ("Steel Mill Interior", 1912, "ARTIST-018"),
    ("The Suspension Bridge", 1919, "ARTIST-018"),
]
conditions_g9 = ["Good","Fair","Excellent","Good","Fair","Good"]
for i, (name, year, art) in enumerate(group9):
    artifacts.append(dict(
        id=f"OBJ-{len(artifacts)+1:04d}", name=name, type=TYPE_PHOTO, creationYear=year,
        condition=conditions_g9[i], description=None, acquisitionDate=None,
        artistRef=art, periodRef="HP-015", siteRef=None, collectionRef="COL-010",
    ))

# --- Group 10: Mixed / Other + Jewelry (4) ----------------------------------
group10 = [
    ("Sandstone Apsara Relief Fragment", TYPE_OTHER, 1150, None, "HP-014", "CS-011", "Fair"),
    ("Gold Filigree Pendant", TYPE_JEWELRY, 1958, "ARTIST-024", None, None, "Excellent"),
    ("Carved Jade Pendant, Unknown Origin", TYPE_JEWELRY, None, None, None, None, "Good"),
    ("Silver and Turquoise Brooch", TYPE_JEWELRY, 1610, None, "HP-008", None, "Good"),
]
for name, typ, year, art, per, site, cond in group10:
    artifacts.append(dict(
        id=f"OBJ-{len(artifacts)+1:04d}", name=name, type=typ, creationYear=year,
        condition=cond, description=None, acquisitionDate=None,
        artistRef=art, periodRef=per, siteRef=site, collectionRef="COL-011",
    ))

assert len(artifacts) == 83, f"Expected 83 artifacts, got {len(artifacts)}"

# Add acquisitionDate to a majority of artifacts (some legitimately missing --
# older museum accessions with no recorded acquisition paperwork)
acq_start = date(1970, 1, 1)
for i, a in enumerate(artifacts):
    if i % 6 != 0:  # ~83% have a recorded acquisition date, ~17% do not
        offset_days = random.randint(0, (date(2023, 12, 31) - acq_start).days)
        a["acquisitionDate"] = (acq_start + timedelta(days=offset_days)).isoformat()

# Add a description to about half the artifacts (rest legitimately blank)
sample_descriptions = {
    3: "Notable for its unusually well-preserved pigment layer.",
    9: "Acquired as part of a bequest; frame is a later, non-original addition.",
    18: "One of the few securely dated pieces in the New Kingdom holdings.",
    41: "Displays tool marks consistent with the imperial Xing kilns.",
    55: "Beadwork pattern consistent with royal regalia fragments held in comparable collections.",
    70: "Marginalia include a scribal note in a secondary hand.",
}
for idx, desc in sample_descriptions.items():
    if idx < len(artifacts):
        artifacts[idx]["description"] = desc

# ---------------------------------------------------------------------------
# 7. EXHIBITIONS (8) -- several artifacts deliberately reused across shows
# ---------------------------------------------------------------------------
exhibitions = [
    dict(id="EXH-001", title="Masters of the Renaissance", startDate="2023-03-01", endDate="2023-08-31",
         location="West Wing, Gallery 1", curatorRef="CUR-001",
         description="Survey of Italian and Northern Renaissance painting and sculpture.",
         featured=["OBJ-0001","OBJ-0002","OBJ-0003","OBJ-0004","OBJ-0005","OBJ-0013","OBJ-0014"]),
    dict(id="EXH-002", title="Light on the Seine: French Impressionism", startDate="2023-05-15", endDate="2023-10-01",
         location="West Wing, Gallery 3", curatorRef="CUR-001", description=None,
         featured=["OBJ-0009","OBJ-0010","OBJ-0011"]),
    dict(id="EXH-003", title="Gifts for the Afterlife: Egyptian Funerary Art", startDate="2023-02-01", endDate="2023-06-30",
         location="East Wing, Gallery 2", curatorRef="CUR-002",
         description="Objects associated with New Kingdom burial practice.",
         featured=["OBJ-0016","OBJ-0017","OBJ-0018","OBJ-0019","OBJ-0020","OBJ-0021","OBJ-0022","OBJ-0023"]),
    dict(id="EXH-004", title="The Classical World", startDate="2023-09-01", endDate="2024-02-28",
         location="East Wing, Gallery 1", curatorRef="CUR-002", description=None,
         featured=["OBJ-0024","OBJ-0025","OBJ-0026","OBJ-0027","OBJ-0028","OBJ-0002"]),
    dict(id="EXH-005", title="Silk and Celadon: Tang Dynasty Splendor", startDate="2023-04-10", endDate="2023-09-10",
         location="North Wing, Gallery 1", curatorRef="CUR-003",
         description="Ceramics, paintings and metalwork from the Tang imperial court.",
         featured=["OBJ-0034","OBJ-0035","OBJ-0036","OBJ-0037","OBJ-0038"]),
    dict(id="EXH-006", title="Kingdoms of Bronze: Court Art of Benin", startDate="2023-06-01", endDate="2023-11-30",
         location="South Wing, Gallery 2", curatorRef="CUR-006",
         description="Cast bronze and carved ivory from the Kingdom of Benin.",
         featured=["OBJ-0057","OBJ-0058","OBJ-0059","OBJ-0060","OBJ-0061","OBJ-0062"]),
    dict(id="EXH-007", title="Early Frames: Photography 1890-1930", startDate="2024-01-15", endDate="2024-06-15",
         location="South Wing, Gallery 4", curatorRef="CUR-005", description=None,
         featured=["OBJ-0074","OBJ-0075","OBJ-0076","OBJ-0077","OBJ-0078","OBJ-0079"]),
    dict(id="EXH-008", title="Cities Under Ash: Roman Pompeii", startDate="2023-10-01", endDate="2024-03-31",
         location="East Wing, Gallery 3", curatorRef="CUR-002",
         description="Everyday and ceremonial objects recovered from the Pompeii excavation.",
         featured=["OBJ-0029","OBJ-0030","OBJ-0031","OBJ-0032","OBJ-0033","OBJ-0024"]),
]

# ---------------------------------------------------------------------------
# 8. LOANS (12) -- references a subset of artifacts; fictional institutions
# ---------------------------------------------------------------------------
fictional_institutions = [
    "Continental Museum of Art, Vienna", "Meridian City Museum of Fine Arts",
    "Northport Museum of Ancient Cultures", "Riverton Cultural Heritage Museum",
    "Grandport National Gallery", "Ashfield Museum of World Art",
    "Old Harbor Antiquities Museum", "Lakeside Museum of Decorative Arts",
    "Falkenridge Municipal Museum", "Sundale Museum of Photography",
]
loans = [
    dict(id="LOAN-0001", artifactRef="OBJ-0009", institution=fictional_institutions[0],
         start="2024-02-01", end="2024-08-01", status="Active", insuranceValue="450000.00"),
    dict(id="LOAN-0002", artifactRef="OBJ-0002", institution=fictional_institutions[1],
         start="2023-11-01", end="2024-04-01", status="Returned", insuranceValue="620000.00"),
    dict(id="LOAN-0003", artifactRef="OBJ-0025", institution=fictional_institutions[2],
         start="2024-01-15", end="2024-07-15", status="Active", insuranceValue="180000.00"),
    dict(id="LOAN-0004", artifactRef="OBJ-0059", institution=fictional_institutions[3],
         start="2023-09-01", end="2024-01-01", status="Returned", insuranceValue="950000.00"),
    dict(id="LOAN-0005", artifactRef="OBJ-0037", institution=fictional_institutions[4],
         start="2024-03-01", end="2024-09-01", status="Pending", insuranceValue="310000.00"),
    dict(id="LOAN-0006", artifactRef="OBJ-0075", institution=fictional_institutions[9],
         start="2024-02-15", end="2024-05-15", status="Active", insuranceValue="75000.00"),
    dict(id="LOAN-0007", artifactRef="OBJ-0016", institution=fictional_institutions[6],
         start="2023-07-01", end="2023-12-01", status="Overdue", insuranceValue="540000.00"),
    dict(id="LOAN-0008", artifactRef="OBJ-0044", institution=fictional_institutions[5],
         start="2024-04-01", end="2024-10-01", status="Pending", insuranceValue="None"),
    dict(id="LOAN-0009", artifactRef="OBJ-0005", institution=fictional_institutions[0],
         start="2023-05-01", end="2023-11-01", status="Returned", insuranceValue="280000.00"),
    dict(id="LOAN-0010", artifactRef="OBJ-0068", institution=fictional_institutions[7],
         start="2024-01-01", end="2024-06-01", status="Cancelled", insuranceValue="None"),
    dict(id="LOAN-0011", artifactRef="OBJ-0030", institution=fictional_institutions[8],
         start="2024-05-01", end="2024-11-01", status="Pending", insuranceValue="410000.00"),
    dict(id="LOAN-0012", artifactRef="OBJ-0012", institution=fictional_institutions[1],
         start="2023-08-15", end="2024-02-15", status="Returned", insuranceValue="365000.00"),
]

# ---------------------------------------------------------------------------
# 9. RESTORATION PROJECTS (14) -- exactly one of curatorRef / external name
# ---------------------------------------------------------------------------
restorations = [
    dict(id="RES-0001", artifactRef="OBJ-0020", start="2023-01-10", end="2023-06-20",
         status="Completed", cost="18500.00", curatorRef="CUR-002", external=None,
         description="Stabilization of painted wood panel and pigment consolidation."),
    dict(id="RES-0002", artifactRef="OBJ-0033", start="2023-11-01", end=None,
         status="InProgress", cost="42000.00", curatorRef=None, external="Verrelli Conservation Studio",
         description="Fresco fragment mounting and surface cleaning."),
    dict(id="RES-0003", artifactRef="OBJ-0022", start="2024-02-01", end=None,
         status="Planned", cost=None, curatorRef="CUR-002", external=None, description=None),
    dict(id="RES-0004", artifactRef="OBJ-0017", start="2022-09-01", end="2023-03-15",
         status="Completed", cost="9800.00", curatorRef=None, external="Northbridge Textile & Paper Lab",
         description="Fragment consolidation and archival rehousing."),
    dict(id="RES-0005", artifactRef="OBJ-0064", start="2023-06-01", end="2023-09-01",
         status="Completed", cost="5400.00", curatorRef="CUR-004", external=None, description=None),
    dict(id="RES-0006", artifactRef="OBJ-0046", start="2024-01-05", end=None,
         status="InProgress", cost="27500.00", curatorRef=None, external="Chen & Wu Ceramics Restoration",
         description="Reassembly of fragmented ceramic body."),
    dict(id="RES-0007", artifactRef="OBJ-0069", start="2023-10-15", end=None,
         status="OnHold", cost="15000.00", curatorRef="CUR-004", external=None,
         description="Restoration paused pending fiber analysis results."),
    dict(id="RES-0008", artifactRef="OBJ-0027", start="2023-04-01", end="2023-07-01",
         status="Completed", cost="6200.00", curatorRef="CUR-002", external=None, description=None),
    dict(id="RES-0009", artifactRef="OBJ-0072", start="2024-03-01", end=None,
         status="Planned", cost=None, curatorRef=None, external="Alpenhaus Manuscript Conservation",
         description=None),
    dict(id="RES-0010", artifactRef="OBJ-0053", start="2023-02-15", end="2023-05-15",
         status="Completed", cost="11750.00", curatorRef="CUR-006", external=None, description=None),
    dict(id="RES-0011", artifactRef="OBJ-0058", start="2023-12-01", end=None,
         status="InProgress", cost="33000.00", curatorRef="CUR-006", external=None,
         description="Corrosion treatment and structural support of cast bronze head."),
    dict(id="RES-0012", artifactRef="OBJ-0083", start="2024-04-01", end=None,
         status="Planned", cost=None, curatorRef=None, external="Sundale Metalwork Conservators",
         description=None),
    dict(id="RES-0013", artifactRef="OBJ-0006", start="2022-11-01", end="2023-02-01",
         status="Completed", cost="8300.00", curatorRef="CUR-001", external=None, description=None),
    dict(id="RES-0014", artifactRef="OBJ-0080", start="2023-08-01", end="2023-10-01",
         status="Completed", cost="4100.00", curatorRef="CUR-005", external=None,
         description="Print stabilization and re-matting."),
]

# ---------------------------------------------------------------------------
# 10. VISITORS (40) and VISITS (90)
# ---------------------------------------------------------------------------
age_groups = ["Child", "Adult", "Senior"]
ticket_types = ["Standard", "Student", "Senior", "Free", "Group"]

visitors = []
for i in range(1, 41):
    vid = f"VIS-{i:05d}"
    if i % 8 == 0:  # ~12.5% have no recorded age group
        ag = None
    else:
        ag = random.choices(age_groups, weights=[15, 65, 20])[0]
    visitors.append(dict(id=vid, ageGroup=ag))

visit_start = date(2023, 2, 1)
visit_end = date(2024, 6, 15)
exhibition_ids = [e["id"] for e in exhibitions]
visits = []
for i in range(1, 91):
    vid = f"VISIT-{i:06d}"
    visitor = random.choice(visitors)["id"]
    exhibition = random.choice(exhibition_ids)
    offset_days = random.randint(0, (visit_end - visit_start).days)
    vdate = (visit_start + timedelta(days=offset_days)).isoformat()
    ticket = random.choices(ticket_types, weights=[40, 20, 15, 10, 15])[0]
    visits.append(dict(id=vid, visitorRef=visitor, exhibitionRef=exhibition,
                        visitDate=vdate, ticketType=ticket))

# ---------------------------------------------------------------------------
# XML BUILDING
# ---------------------------------------------------------------------------
def sub(parent, tag, text):
    if text is None:
        return
    el = ET.SubElement(parent, tag)
    el.text = str(text)

root = ET.Element("MuseumDatabase")

periods_el = ET.SubElement(root, "HistoricalPeriods")
for p in historical_periods:
    e = ET.SubElement(periods_el, "HistoricalPeriod", id=p["id"])
    sub(e, "name", p["name"]); sub(e, "startYear", p["startYear"]); sub(e, "endYear", p["endYear"])
    sub(e, "description", p["description"])

sites_el = ET.SubElement(root, "CulturalSites")
for s in cultural_sites:
    e = ET.SubElement(sites_el, "CulturalSite", id=s["id"])
    sub(e, "name", s["name"]); sub(e, "country", s["country"]); sub(e, "region", s["region"])
    sub(e, "description", s["description"])

artists_el = ET.SubElement(root, "Artists")
for a in artists:
    e = ET.SubElement(artists_el, "Artist", id=a["id"])
    sub(e, "name", a["name"]); sub(e, "birthYear", a["birthYear"]); sub(e, "deathYear", a["deathYear"])
    sub(e, "nationality", a["nationality"]); sub(e, "biography", a["biography"])

curators_el = ET.SubElement(root, "Curators")
for c in curators:
    e = ET.SubElement(curators_el, "Curator", id=c["id"])
    sub(e, "name", c["name"]); sub(e, "department", c["department"])
    sub(e, "email", c["email"]); sub(e, "hireDate", c["hireDate"])

collections_el = ET.SubElement(root, "Collections")
for c in collections:
    e = ET.SubElement(collections_el, "Collection", id=c["id"], curatorRef=c["curatorRef"])
    sub(e, "name", c["name"]); sub(e, "theme", c["theme"]); sub(e, "description", c["description"])

artifacts_el = ET.SubElement(root, "Artifacts")
for a in artifacts:
    attrs = {"id": a["id"]}
    if a["artistRef"]: attrs["artistRef"] = a["artistRef"]
    if a["periodRef"]: attrs["periodRef"] = a["periodRef"]
    if a["siteRef"]: attrs["siteRef"] = a["siteRef"]
    if a["collectionRef"]: attrs["collectionRef"] = a["collectionRef"]
    e = ET.SubElement(artifacts_el, "Artifact", **attrs)
    sub(e, "name", a["name"]); sub(e, "type", a["type"]); sub(e, "creationYear", a["creationYear"])
    sub(e, "condition", a["condition"]); sub(e, "description", a["description"])
    sub(e, "acquisitionDate", a["acquisitionDate"])

exhibitions_el = ET.SubElement(root, "Exhibitions")
for ex in exhibitions:
    e = ET.SubElement(exhibitions_el, "Exhibition", id=ex["id"], curatorRef=ex["curatorRef"])
    sub(e, "title", ex["title"]); sub(e, "startDate", ex["startDate"]); sub(e, "endDate", ex["endDate"])
    sub(e, "location", ex["location"]); sub(e, "description", ex["description"])
    for obj_id in ex["featured"]:
        ET.SubElement(e, "FeaturedArtifact", artifactRef=obj_id)

loans_el = ET.SubElement(root, "Loans")
for l in loans:
    e = ET.SubElement(loans_el, "Loan", id=l["id"], artifactRef=l["artifactRef"])
    sub(e, "borrowingInstitution", l["institution"]); sub(e, "loanStartDate", l["start"])
    sub(e, "loanEndDate", l["end"]); sub(e, "status", l["status"])
    sub(e, "insuranceValue", None if l["insuranceValue"] == "None" else l["insuranceValue"])

res_el = ET.SubElement(root, "RestorationProjects")
for r in restorations:
    attrs = {"id": r["id"], "artifactRef": r["artifactRef"]}
    if r["curatorRef"]: attrs["curatorRef"] = r["curatorRef"]
    if r["external"]: attrs["externalRestorerName"] = r["external"]
    e = ET.SubElement(res_el, "RestorationProject", **attrs)
    sub(e, "startDate", r["start"]); sub(e, "endDate", r["end"]); sub(e, "status", r["status"])
    sub(e, "cost", r["cost"]); sub(e, "description", r["description"])

visitors_el = ET.SubElement(root, "Visitors")
for v in visitors:
    e = ET.SubElement(visitors_el, "Visitor", id=v["id"])
    sub(e, "ageGroup", v["ageGroup"])

visits_el = ET.SubElement(root, "Visits")
for v in visits:
    e = ET.SubElement(visits_el, "Visit", id=v["id"], visitorRef=v["visitorRef"], exhibitionRef=v["exhibitionRef"])
    sub(e, "visitDate", v["visitDate"]); sub(e, "ticketType", v["ticketType"])

# Pretty print
rough = ET.tostring(root, encoding="utf-8")
pretty = minidom.parseString(rough).toprettyxml(indent="  ")
# strip blank lines minidom introduces
pretty = "\n".join(line for line in pretty.split("\n") if line.strip())

header = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    "<!--\n"
    "  ===========================================================\n"
    "  SYNTHETIC / FICTIONAL DATASET. FOR DEVELOPMENT AND TESTING.\n"
    "  ===========================================================\n"
    "  This file contains INVENTED data created to test the museum\n"
    "  XSD schema. It does NOT represent a real museum collection,\n"
    "  external research dataset, or public database. Artist names,\n"
    "  institution names, and cataloguing details are fictional.\n"
    "  Generated by generate_dataset.py with random.seed(42).\n"
    "-->\n"
)
# Replace the xml declaration line minidom produced with our header+comment
lines = pretty.split("\n")
assert lines[0].startswith("<?xml")
final_xml = header + "\n".join(lines[1:]) + "\n"

with open("museum_dataset_synthetic.xml", "w", encoding="utf-8") as f:
    f.write(final_xml)

print(f"Wrote museum_dataset_synthetic.xml")
print(f"Artifacts: {len(artifacts)}")
print(f"HistoricalPeriods: {len(historical_periods)}  CulturalSites: {len(cultural_sites)}")
print(f"Artists: {len(artists)}  Curators: {len(curators)}  Collections: {len(collections)}")
print(f"Exhibitions: {len(exhibitions)}  Loans: {len(loans)}  RestorationProjects: {len(restorations)}")
print(f"Visitors: {len(visitors)}  Visits: {len(visits)}")
