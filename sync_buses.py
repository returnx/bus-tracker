import openpyxl
import json
import os

def sync_buses():
    excel_path = 'GPRS - 26-27.xlsx'
    if not os.path.exists(excel_path):
        print(f"File not found: {excel_path}")
        return

    wb = openpyxl.load_workbook(excel_path, data_only=True)
    result = []

    for sheetname in wb.sheetnames:
        ws = wb[sheetname]
        is_kg = 'KG' in sheetname.upper()
        section_id = 'kg' if is_kg else '1to12'
        section_title = 'KG Block' if is_kg else 'Grades 1 to 12'
        section_badge = 'KG Block' if is_kg else 'Grades 1-12'

        buses = []
        for r in range(2, ws.max_row + 1):
            sl = ws.cell(r, 1).value
            veh = ws.cell(r, 2).value
            route = ws.cell(r, 3).value
            link = ws.cell(r, 4).value
            if not (veh or route or link):
                continue

            # Format route
            if isinstance(route, float) and route.is_integer():
                route_str = str(int(route))
            elif route is not None:
                route_str = str(route).strip()
            else:
                route_str = 'N/A'

            veh_str = str(veh).strip() if veh is not None else 'N/A'
            link_str = str(link).strip() if link is not None else ''
            hash_val = link_str.rstrip('/').split('/')[-1] if link_str else ''

            if isinstance(sl, float) and sl.is_integer():
                sl_val = int(sl)
            else:
                sl_val = sl if sl is not None else len(buses) + 1

            buses.append({
                'sl': sl_val,
                'vehicle': veh_str,
                'route': route_str,
                'link': link_str,
                'hash': hash_val,
                'section': section_id,
                'sectionTitle': section_title
            })

        result.append({
            'id': section_id,
            'title': section_title,
            'sheetName': sheetname,
            'badge': section_badge,
            'count': len(buses),
            'buses': buses
        })

    print(f"Processed {len(result)} sheets:")
    for s in result:
        print(f" - {s['title']} ({s['sheetName']}): {s['count']} buses")

    with open('buses.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    print("Saved buses.json")

    with open('buses-data.js', 'w', encoding='utf-8') as f:
        f.write('// Auto-generated bus dataset from GPRS - 26-27.xlsx\n')
        f.write('const BUS_DATA = ' + json.dumps(result, indent=2) + ';\n')
        f.write('if (typeof module !== "undefined" && module.exports) { module.exports = BUS_DATA; }\n')
    print("Saved buses-data.js")

if __name__ == '__main__':
    sync_buses()

