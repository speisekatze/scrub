from scrubadubdub import config, scrub

conf = config.config('config/config.yaml')

scrubber = scrub.Scrub(conf)
clean = scrubber.scrub("Olf Maurer mag keine PII, darum lässt er Peter alle entfernen! Herrn Müller gefällt das.")
print(clean)

# Tests
test_data = [
    {
        "text": "Die A.B.C. Corp. gab heute in Berlin bekannt, dass die Universität von Berlin neue Forschung im Bereich AeroStream startet.",
        "entities": [
            (4, 15, "ORG"),     # A.B.C. Corp. (Abkürzungen/Punkte)
            (26, 32, "LOC"),    # Berlin (Einfacher Ort)
            (48, 70, "ORG"),    # Universität von Berlin (Verschachtelte Entität: ORG + LOC)
            (85, 94, "MISC")    # AeroStream (Produkt/Projekt)
        ]
    },
    {
        "text": "Dr. Elena Schmidt sprach mit Schmidt über das Projekt Schloss.",
        "entities": [
            (4, 16, "PER"),     # Dr. Elena Schmidt (Titel + Name)
            (30, 36, "PER"),    # Schmidt (Name ohne Titel - Kontext-Test)
            (52, 58, "MISC")    # Schloss (Ambiguität: Ist es ein Gebäude oder ein Projektname?)
        ]
    },
    {
        "text": "Während der Konferenz im Hotel Adlon Kempinski sah Rose, dass die Rosen im Garten verwelkten.",
        "entities": [
            (31, 52, "FAC"),    # Hotel Adlon Kempinski (Facility/Location)
            (57, 61, "PER"),    # Rose (Person - Ambiguität: Name vs. Pflanze)
        ]
    },
    {
        "text": "Die Global Express AG nutzt Cloud-Systeme wie Azure oder AWS.",
        "entities": [
            (4, 21, "ORG"),     # Global Express AG (Standard ORG)
            (43, 48, "MISC"),   # Azure (Produkt/Service)
            (53, 56, "MISC")    # AWS (Abkürzung/Service)
        ]
    },
    {
        "text": "Dr. Elena Schmidt sprach mit Rose über das Projekt Schloss."
    },
    {
        "text": "HELADEF1WEM"
}
]

for test in test_data:
    check = scrubber.scrub(test['text'])
    print(check)
