from defusedxml.lxml import fromstring
import lxml.etree as ET
import tempfile
from xml.etree import ElementTree
from signxml import XMLSigner, XMLVerifier

# s1 = tempfile.TemporaryFile()
# s2 = tempfile.TemporaryFile()
#
# one_data = open('1.xml').read()
#
#
# et1 = ET.parse('1.xml')
# et2 = ET.parse('signed-crt')
#
# print(et1 == et2)
# print(ET.dump(et1))
XML_TEMPLATE = """<name>{}</name>"""

HTML_TEMPLATE = """{}"""

key = open('domain.key', 'rb').read()
cert = open('domain.crt', 'rb').read()

def verify_and_get_user(xml):
    try:
        to_xml = fromstring(xml)
        XMLVerifier().verify(to_xml, x509_cert=cert).signed_xml
        return to_xml.text
    except:
        return

def sign(name):
    try:
        et = fromstring(XML_TEMPLATE.format(name))
        signed = XMLSigner().sign(et, key=key, cert=cert)
        return HTML_TEMPLATE.format(ET.tostring(signed))
    except:
        return

# signed_root =
# verified_data = XMLVerifier().verify(signed_root, x509_cert=cert).signed_xml
#
# verified_data2 = XMLVerifier().verify(et2, x509_cert=cert).signed_xml
#
# print(ET.tostring(verified_data2))
# open('signed-crt', 'wb').write(ET.tostring(signed_root2))
