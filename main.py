from scraper import download_sevis_stem
from scraper import download_sevis_agg

def main():
    # Set the paths to where the data should be downloaded
    path_agg = r"~/PyCharmProjects/Battery Project/SEVIS Data/Aggregate"
    download_sevis_agg(path_agg)
    path_stem = r"~/PyCharmProjects/Battery Project/SEVIS Data/STEM"
    download_sevis_stem(path_stem)


if __name__ == "__main__":
    main()