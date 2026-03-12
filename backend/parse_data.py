import xml.etree.ElementTree as ET
import json
from database.db_config import get_db_connection

def parse_and_insert_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    xml_file = '../official-cpe-dictionary_v2.xml'
    
    print(f"Processing {xml_file}...")
    
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    ns = {
        'cpe': 'http://cpe.mitre.org/dictionary/2.0',
        'cpe-23': 'http://scap.nist.gov/schema/cpe-extension/2.3'
    }
    
    count = 0
    for cpe_item in root.findall('cpe:cpe-item', ns):
        cpe_22_uri = cpe_item.get('name')
        
        title_elem = cpe_item.find('cpe:title', ns)
        cpe_title = title_elem.text if title_elem is not None else None
        
        cpe_23_elem = cpe_item.find('cpe-23:cpe23-item', ns)
        cpe_23_uri = cpe_23_elem.get('name') if cpe_23_elem is not None else None
        
        refs = cpe_item.findall('cpe:references/cpe:reference', ns)
        reference_links = json.dumps([ref.get('href') for ref in refs]) if refs else None
        
        deprecation_elem = cpe_item.find('cpe-23:deprecation', ns)
        cpe_22_deprecation_date = deprecation_elem.get('date') if deprecation_elem is not None else None
        cpe_23_deprecation_date = cpe_22_deprecation_date
        
        sql = """INSERT INTO cpes 
                 (cpe_title, cpe_22_uri, cpe_23_uri, reference_links, 
                  cpe_22_deprecation_date, cpe_23_deprecation_date)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        
        cursor.execute(sql, (cpe_title, cpe_22_uri, cpe_23_uri, 
                            reference_links, cpe_22_deprecation_date, 
                            cpe_23_deprecation_date))
        
        count += 1
        if count % 1000 == 0:
            conn.commit()
            print(f"Processed {count} items...")
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Data import completed! Total items: {count}")

if __name__ == '__main__':
    parse_and_insert_data()
