from lib import download, extract, pipeline, utils, config
import os


def process_random(limit=-1):
    # Download a new WARC
    print("Downloading WARC")
    segment_id, warc_path = download.download_rand_new()

    # Extract samples from the warc
    print("Extracting samples")
    samples = extract.extract(warc_path, segment_id, limit=limit)

    # Pass through pipeline
    print("Running pipeline")
    for process in pipeline.pipeline:
        samples = process(samples)

    # Write to CSV
    print("Writing to CSV")
    csv_name = warc_path.split('/')[-1].split('.')[0] + '.csv'
    csv_path = os.path.join(config.CSV_DIR_SAMPLES, csv_name)
    utils.export_csv(samples, csv_path)


if __name__ == '__main__':
    process_random(limit=10000)
