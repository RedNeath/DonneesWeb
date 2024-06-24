import xml.dom.minidom
import heapq

# Parse the XML document
DOMTree = xml.dom.minidom.parse("nantes-logement.xml")
rootNode = DOMTree.documentElement

dictionaryResidence = {}
binaryHeapLogement = []

# Iterate through the residents
for resident in rootNode.childNodes:
    if resident.nodeType != resident.ELEMENT_NODE:
        continue
    
    loyer = resident.getElementsByTagName('infos')[0].getElementsByTagName('loyer')[0]
    nblogement = 0
    
    for type in loyer.childNodes:
        if type.nodeType != type.ELEMENT_NODE:
            continue
        if type.tagName in ('chambre', 'studio', 't1'):
            continue
        nombre = type.getAttribute("nombre")
        if nombre:
            nblogement += int(nombre)
        else:
            nblogement += 1
    
    # Remove specified tags
    for tag in ['chambre', 'studio', 't1']:
        while len(loyer.getElementsByTagName(tag)) > 0:
            loyer.removeChild(loyer.getElementsByTagName(tag)[0])
    
    if len([item for item in loyer.childNodes if item.nodeType == item.ELEMENT_NODE]) <= 0:
        continue
    
    if nblogement not in dictionaryResidence:
        dictionaryResidence[nblogement] = []
        heapq.heappush(binaryHeapLogement, nblogement)
    
    # Append a copy of the resident to the dictionary
    dictionaryResidence[nblogement].append(resident.cloneNode(deep=True))
    
    # Remove services tag if it exists
    if len(resident.getElementsByTagName('services')) > 0:
        services = resident.getElementsByTagName('services')[0]
        resident.removeChild(services)

# Create a new XML document
doc = xml.dom.minidom.Document()
new_root = doc.createElement('root')
doc.appendChild(new_root)

# Append elements from the heap to the new document
while len(binaryHeapLogement) > 0:
    residence = heapq.heappop(binaryHeapLogement)
    for logement in dictionaryResidence[residence]:
        new_root.appendChild(logement)

# Write the new XML document to a file
with open('dom_sans_xpath.xml', 'w', encoding='utf-8') as file:
    file.write(doc.toprettyxml(indent="", newl=''))
