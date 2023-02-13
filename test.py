filepath = r'~/PyCharmProjects/Battery Project/Data/Aggregate'
filepath += r"/Test.xlsx"
print(filepath)

print(len(['SOUTH AFRICA', 'Africa', 'Southern Africa', '2036', '1000', '1036', '256', '1004', '154', '2', '1', '1', '400', '86', '55', '7', '70', '0', '37', '26', '17', '265', '35', '40', '21', '7', '104', '52', '1', '1', '22', '26', '63', '23', '19', '24', '16', '142', '33', '7', '46', '15', '38', '0', '18', '2', '61', '4', '6', '13', '44', '3', '8', '276', '49', '29', '17', '97', '1', '16', '28', '6', '33', '132', '18', '36', '0', '5', '33', '9', '12', '0']))

print(str("﻿Country of Citizenship".encode('ascii', 'ignore')))

def timestamped_sevis_urls(get_stem=False):
    ts_urls = []
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
              "november",
              "december"]
    years = [2014 + i for i in range(8)]
    stem = "" if get_stem else "-stem"
    for month in months:
        for year in years:
            ts = f'{month}-{year}'
            url = f'https://studyinthestates.dhs.gov/sevis-data-mapping-tool/{month}-{year}{stem}-sevis-data-mapping-tool-data'

            ts_urls.append((url, ts))

    return ts_urls

# def download_data(url, filepath):
#     try:
#         page = requests.get(url)
#     except ConnectionError:
#         print(f'Invalid URL: "{url}"')
#         pass
#
#     soup = BeautifulSoup(page.text, 'lxml')
#     tables = soup.find_all('table')
#     if len(tables) != 1:
#         raise Exception("More than one table per page found:", f"{url}")
#     table = tables[0]
#     headers = []
#
#     for i in table.find('tr').find_all():
#         title = i.text
#         headers.append(title)
#
#     # print(headers)
#     mydata = pd.DataFrame(columns=headers)
#     for j in table.find_all('tr')[1:]:
#         row_data = j.find_all()
#         row = [i.text for i in row_data]
#         length = len(mydata)
#         print(row)
#         # mydata.loc[length] = row
#         # mydata = pd.concat([mydata, )
#
#     mydata.to_excel(filepath, index=False)