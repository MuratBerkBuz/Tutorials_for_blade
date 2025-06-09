
import os
# Get the absolute path to the folder where the .py file is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to that folder
os.chdir(script_dir)
print("Current working directory:", os.getcwd())

from lxml import etree

# Load the XML file
tree = etree.parse("cpacs.xml")
root = tree.getroot()

print(f"Root element tag: {root.tag}")

# Accessing direct children
for child in root:
    print(f"  Child tag: {child.tag}, Attributes: {child.attrib}")
    
# CPACS uses namespaces — we need to handle that
ns = {"cpacs": "http://www.dlr.de/cpacs/3.3"}

# Find the wing area
area = root.find(".//cpacs:wing/cpacs:area", namespaces=ns)
span = root.find(".//cpacs:wing/cpacs:span", namespaces=ns)
print("Wing area:", area.text, "\nspan :", span.text)

area.text = "50.0"  # Modify the area
span.text = "20.0"  # Modify the span
# Save the modified XML back to a file
tree.write("cpacs_modified.xml", pretty_print=True, xml_declaration=True, encoding= "UTF-8")
print("Wing area:", area.text, "\nspan :", span.text)
#for rectangular wing
chord = float(area.text) / float(span.text)
print("Wing chord:%.2f" % chord)

wings = root.find(".//cpacs:wings", namespaces=ns)
# Remove existing Wing2 (if exists)
for wing in wings.findall("cpacs:wing", namespaces=ns):
    if wing.attrib.get("uid") == "Wing2":
        wings.remove(wing)

new_wing = etree.Element("{http://www.dlr.de/cpacs/3.3}wing", uid="Wing2")
name = etree.SubElement(new_wing,"{http://www.dlr.de/cpacs/3.3}name")
name.text = "Second Wing"
area = etree.SubElement(new_wing, "{http://www.dlr.de/cpacs/3.3}area")
area.text = "30.0"
span = etree.SubElement(new_wing, "{http://www.dlr.de/cpacs/3.3}span")
span.text = "25.0"

wings.append(new_wing)
tree.write("cpacs_modified.xml", pretty_print=True, xml_declaration=True, encoding="UTF-8")


# End