from lib import download, extract, filters, utils, config
import os


def process_random():
    # Download a new WARC
    segment_id, warc_path = download.download_rand_new()

    # Extract samples from the warc
    samples = extract.extract(warc_path, segment_id)

    # Run all filters
    for data_filter in filters.filters:
        samples = data_filter(samples)

    # Write to CSV
    csv_name = warc_path.split('/')[-1].split('.')[0] + '.csv'
    csv_path = os.path.join(config.CSV_FILE_SAMPLES, csv_name)
    utils.export_csv(samples, csv_path)


if __name__ == '__main__':
    process_random()
