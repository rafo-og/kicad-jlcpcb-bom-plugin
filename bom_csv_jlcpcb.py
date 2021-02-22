#
# Example python script to generate a BOM from a KiCad generic netlist
#
# Example: Sorted and Grouped CSV BOM
#

"""
    @package
    Generate a CSV BOM for use with JLC distributor.
    Components are sorted by ref and grouped by value with same footprint
    Fields are (if exist).
    LCSC Part numbers are copied from the "LCSC PN#" field, if exists.
    It is possible to hide components from the BOM by setting the 
    "JLCPCB BOM" field to "0" or "false".

    Output fields:
    'Reference', 'MPN #', 'Description', 'Value', 'LCSC Part #', 'Quantity', 'Footprint'

    Command line:
    python "pathToFile/bom_csv_jlcpcb.py" "%I" "%O" "<subfolder>/<filename>.csv"
"""
import kicad_netlist_reader
import csv
import sys

net = kicad_netlist_reader.netlist(sys.argv[1])

outFile = sys.argv[2].rpartition('/')[0] + '/' + sys.argv[3]

with open(outFile, 'w') as f:
    out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)
    out.writerow(['Reference', 'MPN #', 'Description', 'Value', 'LCSC Part #', 'Quantity', 'Footprint'])

    for group in net.groupComponents():
        refs = []
        lcsc_pn = []

        for component in group:
            if component.getField('JLCPCB BOM') in ['0', 'false', 'False', 'FALSE']:
                continue
            if component.getField('Populated') in ['0', 'false', 'False', 'FALSE']:
                continue
            refs.append(component.getRef())
            # refs += component.getRef() + ","
            lcsc_pn.append(component.getField("LCSC PN#"))
            c = component

        if(len(lcsc_pn) == 0):
            continue
            
        result = lcsc_pn.count(lcsc_pn[0]) == len(lcsc_pn)

        if lcsc_pn[0] == "":
            continue

        if(not result):
            print(refs + "don't have the same LCSC PN #")
            print("Error in LCSC PN#")
            exit(1)

        if len(refs) == 0:
            continue

        # Fill in the component groups common data
        out.writerow([
            ",".join(refs),
            # refs,
            c.getField("MPN#"),
            c.getField("Description"),
            c.getValue(),
            lcsc_pn[0],
            len(refs),
            c.getFootprint().split(':')[1]
        ])

    f.close()
