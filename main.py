import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import xlsxwriter


# months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
#               "november",
#               "december"]
# years = [2014 + i for i in range(8)]

months = ["may", "september"]

years = [2022]


def sevis_url(month, year, get_stem=False):
    stem = "-stem" if get_stem else ""
    return f'https://studyinthestates.dhs.gov/sevis-data-mapping-tool/{month}-{year}{stem}-sevis-data-mapping-tool-data'


def table_to_dataframe(table):
    headers = []
    for element in table.find('tr').find_all():
        utf8_header = element.text.encode('ascii', 'ignore').decode("utf-8").strip()
        processed_header = utf8_header.replace("# of Active Students", "active_students")
        headers.append(processed_header)

    data = pd.DataFrame(columns=headers)
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all()
        row = [i.text for i in row_data]
        length = len(data)
        try:
            data.loc[length] = row
        except ValueError:
            print("Invalid row:", row)

    return data


def get_tables(url):
    try:
        page = requests.get(url)
    except ConnectionError:
        print(f'Invalid URL: "{url}"')
        return None

    soup = BeautifulSoup(page.text, 'lxml')
    return soup.find_all('table')


# https://studyinthestates.dhs.gov/sevis-data-mapping-tool/december-2015-stem-sevis-data-mapping-tool-data

# filepath = r'~/PyCharmProjects/Battery Project/Data/Test.xlsx'

def download_sevis_agg(folder_path):
    writer = pd.ExcelWriter(folder_path + r"/All Countries.xlsx")
    china_rows = pd.DataFrame(columns=["Report Date"])

    for year in years:
        for month in months:
            url = sevis_url(month, year)

            # url = "https://studyinthestates.dhs.gov/sevis-data-mapping-tool/december-2018-sevis-data-mapping-tool-data"
            tables = get_tables(url)
            if len(tables) == 0:
                continue
            if len(tables) > 1:
                raise Exception("More than one table per page found:", f"{url}")

            print(f"processing url: {url}")
            df = table_to_dataframe(tables[0])
            country_header = "Country of Citizenship" if "Country of Citizenship" in df.columns else "CoC"

            date = f"{month[0].upper()}{month[1:]} {year}"
            china_row = df.loc[df[country_header] == "CHINA"]
            temp_china_df = pd.DataFrame(china_row)
            temp_china_df.insert(0, "Report Date", date)
            china_rows = pd.concat([china_rows, china_row])

            df.to_excel(writer, sheet_name=f"{date}", index=False)
            print(f"Processed {url}")

    writer.save()
    china_rows.to_excel(folder_path + r"/China.xlsx", index=False)



def download_sevis_stem(folder_path):
    all_writer = pd.ExcelWriter(folder_path + r"/All Countries.xlsx")
    china_writer = pd.ExcelWriter(folder_path + r"/China.xlsx")


    for year in years:
        for month in months:
            url = sevis_url(month, year, True)

            # url = "https://studyinthestates.dhs.gov/sevis-data-mapping-tool/december-2018-sevis-data-mapping-tool-data"
            tables = get_tables(url)
            if len(tables) == 0:
                continue
            if len(tables) > 1:
                raise Exception("More than one table per page found:", f"{url}")

            print(f"processing url: {url}")
            all_data = table_to_dataframe(tables[0])
            country_header = "Country of Citizenship" if "Country of Citizenship" in all_data.columns else "CoC"

            date = f"{month[0].upper()}{month[1:]} {year}"
            china_data = all_data.loc[all_data[country_header] == "CHINA"]


            all_data.to_excel(all_writer, sheet_name=f"{date}", index=False)
            china_data.to_excel(china_writer, sheet_name=f"{date}", index=False)
            print(f"Processed {url}")

    all_writer.save()
    china_writer.save()


def main():
    # path_agg = r"~/PyCharmProjects/Battery Project/SEVIS Data/Aggregate"
    # download_sevis_agg(path_agg)

    path_stem = r"~/PyCharmProjects/Battery Project/SEVIS Data/STEM"
    download_sevis_stem(path_stem)

if __name__ == "__main__":
    main()

    # url = "https://studyinthestates.dhs.gov/sevis-data-mapping-tool/december-2015-stem-sevis-data-mapping-tool-data"
    # url = "https://studyinthestates.dhs.gov/sevis-data-mapping-tool/april-2014-sevis-data-mapping-tool-data"
