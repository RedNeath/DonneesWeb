import xml.sax
import xml.sax.handler

class SaxHandler(xml.sax.handler.ContentHandler):
    def __init__(self, output_file):
        self.output_file = output_file
        self.current_element = ""
        self.current_attributes = {}
        self.current_content = ""

    def startDocument(self):
        self.output_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        self.output_file.write('<!DOCTYPE root [\n')
        self.output_file.write('<!ELEMENT root (residence+)>\n')
        self.output_file.write('<!ELEMENT residence (infos, address?, house_services)>\n')
        self.output_file.write('<!ELEMENT infos (bus?, tramway?, loyer)>\n')
        self.output_file.write('<!ELEMENT address (#PCDATA)>\n')
        self.output_file.write('<!ELEMENT house_services (house_service+)>\n')
        self.output_file.write('<!ELEMENT bus (arret+)>\n')
        self.output_file.write('<!ELEMENT tramway (arret+)>\n')
        self.output_file.write('<!ELEMENT loyer ((t1b|t2|t3)+)>\n')
        self.output_file.write('<!ELEMENT arret (ligne+)>\n')
        self.output_file.write('<!ELEMENT t1b (#PCDATA)>\n')
        self.output_file.write('<!ELEMENT t2 (#PCDATA)>\n')
        self.output_file.write('<!ELEMENT t3 (#PCDATA)>\n')
        self.output_file.write('<!ELEMENT ligne (#PCDATA)>\n')
        self.output_file.write('<!ELEMENT house_service (#PCDATA)>\n')
        self.output_file.write('<!ATTLIST residence id CDATA #REQUIRED>\n')
        self.output_file.write('<!ATTLIST residence title CDATA #REQUIRED>\n')
        self.output_file.write('<!ATTLIST residence short_desc CDATA #IMPLIED>\n')
        self.output_file.write('<!ATTLIST residence lat CDATA #IMPLIED>\n')
        self.output_file.write('<!ATTLIST residence lon CDATA #IMPLIED>\n')
        self.output_file.write('<!ATTLIST residence zone CDATA #IMPLIED>\n')
        self.output_file.write('<!ATTLIST arret nom CDATA #REQUIRED>\n')
        self.output_file.write('<!ATTLIST t1b superficie CDATA #REQUIRED>\n')
        self.output_file.write('<!ATTLIST t1b nombre CDATA #IMPLIED>\n')
        self.output_file.write('<!ATTLIST t2 superficie CDATA #REQUIRED>\n')
        self.output_file.write('<!ATTLIST t2 nombre CDATA #IMPLIED>\n')
        self.output_file.write('<!ATTLIST t3 superficie CDATA #REQUIRED>\n')
        self.output_file.write('<!ATTLIST t3 nombre CDATA #IMPLIED>\n')
        self.output_file.write(']>\n')
        self.output_file.write('<root>\n')

    def startElement(self, name, attrs):
        if name == "residence":
            self.output_file.write('\t<residence id="{}" title="{}"'.format(attrs.getValue("id"), attrs.getValue("title")))
            if attrs.getValue("short_desc"):
                self.output_file.write(' short_desc="{}"'.format(attrs.getValue("short_desc")))
            if attrs.getValue("lat"):
                self.output_file.write(' lat="{}"'.format(attrs.getValue("lat")))
            if attrs.getValue("lon"):
                self.output_file.write(' lon="{}"'.format(attrs.getValue("lon")))
            if attrs.getValue("zone"):
                self.output_file.write(' zone="{}"'.format(attrs.getValue("zone")))
            self.output_file.write(">\n")
        elif name == "infos":
            self.output_file.write("\t\t<infos>\n")
        elif name == "address":
            self.output_file.write("\t\t<address>")
        elif name == "house_services":
            self.output_file.write("\t\t<house_services>\n")
        elif name == "house_service":
            self.output_file.write("\t\t\t<house_service>")
        elif name == "bus" or name == "tramway" or name == "loyer":
            self.output_file.write("\t\t\t<{}>\n".format(name))
        elif name == "arret":
            self.output_file.write('\t\t\t\t<arret nom="{}">\n'.format(attrs.getValue("nom")))
        elif name == "ligne":
            self.output_file.write("\t\t\t\t\t<ligne>")
        elif name == "t1b" or name == "t2" or name == "t3":
            self.output_file.write("\t\t\t\t<{} superficie=\"{}\"".format(name, attrs.getValue("superficie")))
            if attrs.getValue("nombre"):
                self.output_file.write(' nombre="{}"'.format(attrs.getValue("nombre")))
            self.output_file.write(">")
        self.current_content = ""
        self.current_element = name

    def endElement(self, name):
        if name == "residence":
            self.output_file.write("\t</residence>\n")
        elif name == "infos" or name == "house_services":
            self.output_file.write("\t\t</{}>\n".format(name))
        elif name == "address":
            self.output_file.write("{}</address>\n".format(self.current_content))
        elif name == "house_service":
            self.output_file.write("{}</house_service>\n".format(self.current_content))
        elif name == "bus" or name == "tramway" or name == "loyer":
            self.output_file.write("\t\t\t</{}>\n".format(name))
        elif name == "arret":
            self.output_file.write("\t\t\t\t</arret>\n")
        elif name == "ligne":
            self.output_file.write("{}</ligne>\n".format(self.current_content))
        elif name == "t1b" or name == "t2" or name == "t3":
            self.output_file.write("{}</{}>\n".format(self.current_content, name))
        self.current_element = ""
        self.current_content = ""

    def characters(self, content):
        if self.current_element == "address" or self.current_element == "house_service" or self.current_element == "ligne":
            self.current_content += content


if __name__ == "__main__":
    import sys
    from xml.sax.handler import feature_external_ges
    from xml.sax import make_parser

    if len(sys.argv) != 3:
        print("Usage: python sax_handler.py input.xml output.xml")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    parser = make_parser()
    parser.setFeature(feature_external_ges, 0)

    file = open(output_file, "w")
    handler = SaxHandler(file)
    parser.setContentHandler(handler)

    parser.parse(input_file)
    file.write("</root>\n")
    file.close()

