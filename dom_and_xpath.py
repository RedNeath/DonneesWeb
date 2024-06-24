import heapq
from lxml import etree
from xml.dom.minidom import Document

class PrioritizedItem:
    def __init__(self, priority, item):
        self.priority = priority
        self.item = item

    def __lt__(self, other):
        return self.priority < other.priority

# Charger le document XML directement depuis le fichier
tree = etree.parse('nantes-logement.xml')

# Utiliser XPath pour trouver toutes les résidences
residences = tree.xpath('/root/residence')

# Filtrer les résidences qui ont la ligne 2 comme arrêt et calculer le nombre d'appartements
filtered_residences = []
for residence in residences:
    tramway_arrets = residence.xpath('infos/tramway/arret[ligne="2"]')
    if tramway_arrets:
        t1b_count = sum(int(t.get('nombre', 1)) for t in residence.xpath('infos/loyer/t1b'))
        t2_count = sum(int(t.get('nombre', 1)) for t in residence.xpath('infos/loyer/t2'))
        t3_count = sum(int(t.get('nombre', 1)) for t in residence.xpath('infos/loyer/t3'))
        total_apartments = t1b_count + t2_count + t3_count
        
        if total_apartments > 0:
            heapq.heappush(filtered_residences, PrioritizedItem(-total_apartments, residence))

# Créer un nouveau document XML
doc = Document()
new_root = doc.createElement('root')
doc.appendChild(new_root)

# Ajouter les résidences triées au nouveau document XML
while filtered_residences:
    prioritized_item = heapq.heappop(filtered_residences)
    count = -prioritized_item.priority  # inverser la négation pour obtenir le vrai nombre
    residence = prioritized_item.item

    res_elem = doc.createElement('residence')
    res_elem.setAttribute('id', residence.get('id'))
    res_elem.setAttribute('title', residence.get('title'))
    if residence.get('short_desc'):
        res_elem.setAttribute('short_desc', residence.get('short_desc'))
    if residence.get('lat'):
        res_elem.setAttribute('lat', residence.get('lat'))
    if residence.get('lon'):
        res_elem.setAttribute('lon', residence.get('lon'))
    if residence.get('zone'):
        res_elem.setAttribute('zone', residence.get('zone'))
    
    # Infos
    infos_elem = doc.createElement('infos')
    res_elem.appendChild(infos_elem)
    
    # Bus
    bus_elem = doc.createElement('bus')
    arrets_bus = residence.xpath('infos/bus/arret')
    for arret in arrets_bus:
        arret_elem = doc.createElement('arret')
        arret_elem.setAttribute('nom', arret.get('nom'))
        lignes = arret.xpath('ligne')
        for ligne in lignes:
            ligne_elem = doc.createElement('ligne')
            ligne_elem.appendChild(doc.createTextNode(ligne.text))
            arret_elem.appendChild(ligne_elem)
        bus_elem.appendChild(arret_elem)
    if arrets_bus:
        infos_elem.appendChild(bus_elem)
    
    # Tramway
    tramway_elem = doc.createElement('tramway')
    arrets_tramway = residence.xpath('infos/tramway/arret')
    for arret in arrets_tramway:
        arret_elem = doc.createElement('arret')
        arret_elem.setAttribute('nom', arret.get('nom'))
        lignes = arret.xpath('ligne')
        for ligne in lignes:
            ligne_elem = doc.createElement('ligne')
            ligne_elem.appendChild(doc.createTextNode(ligne.text))
            arret_elem.appendChild(ligne_elem)
        tramway_elem.appendChild(arret_elem)
    if arrets_tramway:
        infos_elem.appendChild(tramway_elem)
    
    # Loyer
    loyer_elem = doc.createElement('loyer')
    t1b_elements = residence.xpath('infos/loyer/t1b')
    for t1b in t1b_elements:
        t1b_elem = doc.createElement('t1b')
        t1b_elem.setAttribute('superficie', t1b.get('superficie'))
        if t1b.get('nombre'):
            t1b_elem.setAttribute('nombre', t1b.get('nombre'))
        t1b_elem.appendChild(doc.createTextNode(t1b.text))
        loyer_elem.appendChild(t1b_elem)
    
    t2_elements = residence.xpath('infos/loyer/t2')
    for t2 in t2_elements:
        t2_elem = doc.createElement('t2')
        t2_elem.setAttribute('superficie', t2.get('superficie'))
        if t2.get('nombre'):
            t2_elem.setAttribute('nombre', t2.get('nombre'))
        t2_elem.appendChild(doc.createTextNode(t2.text))
        loyer_elem.appendChild(t2_elem)
    
    t3_elements = residence.xpath('infos/loyer/t3')
    for t3 in t3_elements:
        t3_elem = doc.createElement('t3')
        t3_elem.setAttribute('superficie', t3.get('superficie'))
        if t3.get('nombre'):
            t3_elem.setAttribute('nombre', t3.get('nombre'))
        t3_elem.appendChild(doc.createTextNode(t3.text))
        loyer_elem.appendChild(t3_elem)
    
    infos_elem.appendChild(loyer_elem)
    
    # Address
    address_text = residence.xpath('address/text()')
    if address_text:
        address_elem = doc.createElement('address')
        address_elem.appendChild(doc.createTextNode(address_text[0]))
        res_elem.appendChild(address_elem)
    
    # House Services
    house_services_elem = doc.createElement('house_services')
    house_service_elements = residence.xpath('house_services/house_service')
    for service in house_service_elements:
        service_elem = doc.createElement('house_service')
        service_elem.appendChild(doc.createTextNode(service.text))
        house_services_elem.appendChild(service_elem)
    res_elem.appendChild(house_services_elem)
    
    new_root.appendChild(res_elem)

# Sauvegarder le nouveau document XML
with open('dom_and_xpath.xml', 'w', encoding='utf-8') as file:
    file.write(doc.toprettyxml(indent="  "))
