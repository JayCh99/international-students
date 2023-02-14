import requests
from bs4 import BeautifulSoup
import pandas as pd


def sevis_url(month, year, get_stem=False):
    """
    :param month: month of report to parse
    :param year: year of report to parse
    :param get_stem: whether the report is of STEM students
    :return: the url associated with a SEVIS report
    """

    stem = "-stem" if get_stem else ""
    return f'https://studyinthestates.dhs.gov/sevis-data-mapping-tool/{month}-{year}{stem}-sevis-data-mapping-tool-data'


def table_to_dataframe(table):
    """
    :param table: HTML table from online SEVIS dataset
    :return: df equivalent of 'table'
    """
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
    """
    :param url: SEVIS url
    :return: All tables available at 'url'
    """
    try:
        page = requests.get(url)
    except ConnectionError:
        print(f'Invalid URL: "{url}"')
        return None

    soup = BeautifulSoup(page.text, 'lxml')
    return soup.find_all('table')


def download_sevis_agg(folder_path):
    """
    :param folder_path: local folder to download data in
    :return: None;
    """
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
                  "november",
                  "december"]
    years = [2014 + i for i in range(8)]
    writer = pd.ExcelWriter(folder_path + r"/All Countries.xlsx")
    china_rows = pd.DataFrame(columns=["Report Date"])

    for year in years:
        for month in months:
            url = sevis_url(month, year)
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

    months = ["may", "september"]
    years = [2022]

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