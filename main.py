from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from bs4 import BeautifulSoup
import csv

app = FastAPI()

def generate_busan_district_data():
    f = open('/Users/Python/i/i.csv', mode='rt', encoding='CP949')
    reader = csv.reader(f, delimiter=',')

    i = {}
    for row in reader:
        count = float(row[3]) if row[3].replace('.', '', 1).isdigit() else 0
        i[row[0].strip()] = count

    f.close()
    return i

def modify_svg():
    i = generate_busan_district_data()

    exclude_ids = [
        "행정구역별(시군구)", "부산광역시", "읍부", "면부", "동부"
    ]
    
    for exclude_id in exclude_ids:
        if exclude_id in i:
            del i[exclude_id]

    svg = open('/Users/Python/i/Busan_districts.svg', 'r').read()

    soup = BeautifulSoup(svg, 'lxml')  
    paths = soup.findAll('path')

    colors = ["#F1EEF6", "#D4B9BA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]

    for p in paths:
        district = p.get('id')

        if district:
            district = district.strip()

            if district == "Buk-gu":
                district = "북구"
            elif district == "Busanjin-gu":
                district = "부산진구"
            elif district == "Dong-gu":
                district = "동구"
            elif district == "Dongnae-gu":
                district = "동래구"
            elif district == "Gangseo-gu":
                district = "강서구"
            elif district == "Geumjeong-gu":
                district = "금정구"
            elif district == "Haeundae-gu":
                district = "해운대구"
            elif district == "Jung-gu":
                district = "중구"
            elif district == "Nam-gu":
                district = "남구"
            elif district == "Saha-gu":
                district = "사하구"
            elif district == "Sasang-gu":
                district = "사상구"
            elif district == "Seo-gu":
                district = "서구"
            elif district == "Suyeong-gu":
                district = "수영구"
            elif district == "Yeongdo-gu":
                district = "영도구"
            elif district == "Yeonje-gu":
                district = "연제구"
            elif district == "Gijang-gun":
                district = "기장군"

            if district in i:
                count = i[district]
                if count > 1200:
                    color = colors[5]
                elif count > 1000:
                    color = colors[4]
                elif count > 800:
                    color = colors[3]
                elif count > 500:
                    color = colors[2]
                elif count > 0:
                    color = colors[1]
                else:
                    color = colors[0]
                p['style'] = f"fill:{color};"

    return str(soup)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    modified_svg = modify_svg()
    return modified_svg
