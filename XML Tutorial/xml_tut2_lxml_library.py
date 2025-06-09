from lxml import etree
############################ PARSING XML FILE WITH LXML LIBRARY ############################
import os
# Get the absolute path to the folder where the .py file is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the current working directory to that folder
os.chdir(script_dir)
print("Current working directory:", os.getcwd())
# Load the XML file
tree = etree.parse('aerospace_data.xml')
root = tree.getroot()

print(f"Root element tag: {root.tag}")

############################ Navigating and Accesing through the XML structure ############################

# Using XPath to find specific elements
aircraft_name = root.xpath('/AerospaceData/Aircraft/Name/text()')
if aircraft_name:
    print(f"\nAircraft Name (lxml): {aircraft_name[0]}")

# Find all waypoints in a flight plan
waypoints = root.xpath('//FlightPlan/Route/Waypoint')
print("\nFlight Plan Waypoints:")
for wp in waypoints:
    print(f"  Name: {wp.text}, Lat: {wp.attrib.get('lat')}, Lon: {wp.attrib.get('lon')}")

# Find the thrust of a specific engine
engine_thrust = root.xpath('//Engine[@type="Trent 900"]/Thrust/text()')
if engine_thrust:
    print(f"\nTrent 900 Engine Thrust: {engine_thrust[0]} kN")

############################ Modifying Elements ############################

# Change text of an element
aircraft_name_elem = root.find('Aircraft/Name')
if aircraft_name_elem is not None:
    aircraft_name_elem.text = "Airbus A380-800"

# Change an attribute
aircraft_elem = root.find('Aircraft')
if aircraft_elem is not None:
    aircraft_elem.set('id', 'A380-800')

############################ Add a new element ############################

# Add a new FlightPlan entry
new_flight_plan = etree.SubElement(root, 'FlightPlan', id="FP002")
etree.SubElement(new_flight_plan, 'AircraftRef', id="787")
etree.SubElement(new_flight_plan, 'Origin').text = "KSEA"
etree.SubElement(new_flight_plan, 'Destination').text = "PANC"

############################ delete an element ############################

# Find the element to remove
propulsion_system = root.xpath('//System[@name="Propulsion"]')[0]
if propulsion_system is not None:
    parent_element = propulsion_system.getparent()
    if parent_element is not None:
        parent_element.remove(propulsion_system)

# Save the modified XML back to a file

tree.write('aerospace_data_modified_lxml.xml', encoding='utf-8', xml_declaration=True, pretty_print=True)
# pretty_print=True for nicely formatted output with indentation