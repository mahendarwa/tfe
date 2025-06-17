# Clean up duplicate update.xml files (keep only Teradata/src/update.xml)
import glob

base_path = "Teradata/src"
for xml_file in glob.glob("**/update*.xml", recursive=True):
    if not xml_file.endswith("Teradata/src/update.xml"):
        print(f"🗑️ Removing outdated update file: {xml_file}")
        os.remove(xml_file)
