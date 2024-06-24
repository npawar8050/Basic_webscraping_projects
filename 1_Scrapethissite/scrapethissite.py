import requests
# import etree
from lxml import html

# //*[@class="col-md-4 country"]/h3/text()

response = requests.get("https://www.scrapethissite.com/pages/simple/")
print("Status_code: ",response.status_code)

data = response.text
tree = html.fromstring(data)
l1 = tree.xpath('//*[@class="col-md-4 country"]/h3/text()')
# l2 = tree.xpath('//*[@class="country-capital"]/text()')
# l3 = tree.xpath('//*[@class="country-population"]/text()')
# l4 = tree.xpath('//*[@class="country-area"]/text()')
titles = []
for title in l1:
    title = title.replace("\n","").replace("\t","").strip()
    if title == '':
        pass
    else:
        titles.append(title)

keys = tree.xpath('//div[@class="country-info"]/strong/text()')
values = tree.xpath('//div[@class="country-info"]/span/text()')
keys2 = []
for key in keys:
    if key == 'Area (km':
        key = 'Area(sqkm)'
        keys2.append(key)
    elif key == '):':
        pass
    else:
        keys2.append(key)

keys3 = [key.rstrip(':') for key in keys2]
structured_data = []

# Loop through the data in chunks of 4 (since each country's data has 4 fields)
for i in range(0, len(values), 3):
    country_data = {keys3[j]: values[i+j] for j in range(3)}
    country_detail = {titles[i//3]: country_data}
    # country_detail = {titles[k]: country_data for k in range(len(titles))}
    structured_data.append(country_detail)

output_file = "output2.tsv"
with open(output_file, 'w',encoding='utf-8') as file:
    file.write("Country\tCapital\tPopulation\tArea(sqkm)\n")
    for title, capital in zip(titles, structured_data):
        file.write(f"{title}\t{capital}\n")
print(f"Data has been written to {output_file}")