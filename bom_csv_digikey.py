#
# Example python script to generate a BOM from a KiCad generic netlist
#
# Example: Sorted and Grouped CSV BOM
#

"""
    @package
    Generate a CSV BOM for use with Digikey distributor.
    Components are sorted by ref and grouped by value with same footprint
    Fields are (if exist).
    DK Part numbers are copied from the "DK PN#" field, if exists.
    It is possible to hide components from the BOM by setting the 
    "DK BOM" field to "0" or "false".

    Output fields:
    'Reference', 'MPN #', 'Description', 'Value', 'DK Part #', 'Quantity', 'Footprint'

    Command line:
    python "pathToFile/bom_csv_digikey.py" "%I" "%O" "<subfolder>/<filename>.csv"
"""
import kicad_netlist_reader
import csv
import sys

net = kicad_netlist_reader.netlist(sys.argv[1])

outFile = sys.argv[2].rpartition('/')[0] + '/' + sys.argv[3]

with open(outFile, 'w') as f:
    out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)
    out.writerow(['Reference', 'MPN #', 'Description', 'Value', 'DK Part #', 'Quantity', 'Footprint'])

    for group in net.groupComponents():
        refs = []
        dk_pn = []

        for component in group:
            if component.getField('DK BOM') in ['0', 'false', 'False', 'FALSE']:
                continue
            if component.getField('Populated') in ['0', 'false', 'False', 'FALSE']:
                continue
            refs.append(component.getRef())
            dk_pn.append(component.getField("DK PN#"))
            c = component

        if(len(dk_pn) == 0):
            continue

        result = dk_pn.count(dk_pn[0]) == len(dk_pn)

        if dk_pn[0] == "":
            continue

        if(not result):
            del refs[:]
            for component in group:
                dk_pn_sample = component.getField("DK PN#")
                if dk_pn_sample == "":
                    continue
                else:
                    refs.append(component.getRef())
            # print(refs + "don't have the same DK PN #")
            # print("Error in DK PN#")
            # exit(1)

        if len(refs) == 0:
            continue

        # Fill in the component groups common data
        out.writerow([
            ",".join(refs),
            c.getField("MPN#"),
            c.getField("Description"),
            c.getValue(),
            dk_pn[0],
            len(refs),
            c.getFootprint().split(':')[1]
        ])

    f.close()
