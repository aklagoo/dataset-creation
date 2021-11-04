from lib import download, extract, pipeline, utils, config
import os
import glob


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


def process_downloaded(limit=-1):
    print("Fetching unique WARC")
    # Get all existing CSVs and WARCs
    warc_paths = list(glob.glob(config.SEGMENT_DIR + '/*'))
    csv_paths = list(glob.glob(config.CSV_DIR_SAMPLES))

    # Find CSVs that do not exist
    warc_names = set([os.path.split(x)[1].split('.')[0] for x in warc_paths])
    csv_names = set([os.path.split(x)[1].split('.')[0] for x in csv_paths])
    unique = list(warc_names.difference(csv_names))[0]

    # Select and process the first unique WARC.
    warc_path = [x for x in warc_paths if unique in x][0]
    segment_ids = download.get_urls()
    segment_id = [x[0] for x in segment_ids if unique in x[1]][0]

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
    process_downloaded()
