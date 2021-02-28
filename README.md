# KiCad JLCPCB and Digikey BOM Plugin

Export a JLCPCB and Digikey Compatible BOM directly from your KiCad schematic!

## Installation

This script requires **Python 3**.

The script has been tested with KiCad 5.1.9.

1. Copy `bom_csv_jlcpcb.py` and `bom_csv_digikey.py` to your KiCad installation folder under the `bin/scripting/plugins` directory
2. In Eschema (the Schematics editor) go to "Tools" -> "Generate Bill of Materials", press the "+" button 
   at the bottom of the screen, and choose the plugin file you have just copied. When asked for a nickname,
   go with the default, "bom_csv_jlcpcb" and "bom_csv_digikey".

## Usage

Instructions for exporting JLCPCB BOM from KiCad's Eschema:

1. Go to "Tools" -> "Generate Bill of Materials"
2. Choose "bom_csv_jlcpcb" from the "BOM plugins" list on the left
3. Add to command line the subfolder where the BOM is going to be placed and the name ending with .csv. (The subfolder must be created previously)
4. Click on "Generate". The BOM file should be created inside your project's directory, as a CSV file.

Instructions for exporting Digikey BOM from KiCad's Eschema:

1. Go to "Tools" -> "Generate Bill of Materials"
2. Choose "bom_csv_digikey" from the "BOM plugins" list on the left
3. Add to command line the subfolder where the BOM is going to be placed and the name ending with .csv. (The subfolder must be created previously)
4. Click on "Generate". The BOM file should be created inside your project's directory, as a CSV file.

## Custom Fields

You can customize the script's output by adding the following fields to your components:

1. "LCSC PN#" - Add this field to include an LCSC Part number in the generated BOM. e.g.: C2286 for a red LED.
2. "DK PN#" - Add this field to include an Digikey Part number in the generated BOM.
3. "DK BOM" or "JLCPCB BOM" - Set this field to 0 (or "False") to omit the component from the generated BOM.
4. "Populated" - Set this field to 0 (or "False") to omit the component from any generated BOM. It's useful when you have several assembly variants.

Only the components which have the "LCSC PN#" or "DK PN#" not equal to empty string and their flags aren't set to false are added to the related BOM.

## Generating a JLCPCB CPL File

You can use the `kicad_pos_to_cpl.py` script to convert a KiCad Footprint Position (.pos) file into a CPL file
compatible with JLCPCB SMT Assembly service. The `.pos` file can be generated from Pcbnew, by going into 
"File" -> "Fabrication Outputs" -> "Footprint Position (.pos) File..." and choosing the following options:

* Format: CSV
* Units: Millimeters
* Files: Separate files for front and back

Also, make sure to uncheck "Include footprints with SMD pads even if not marked Surface Mount". 

# Credits

This repository is based on [wokwi/kicad-jlcpcb-bom-plugin](https://github.com/wokwi/kicad-jlcpcb-bom-plugin).