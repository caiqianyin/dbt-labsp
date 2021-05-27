import codecs
import csv
import re


def generator_wrapper(reader):
    to_return = {}

    for row in reader:
        for key, value in row.items():
            formatted_key = key

            # remove non-word, non-whitespace characters
            formatted_key = re.sub(r"[^\w\s]", '', formatted_key)

            # replace whitespace with underscores
            formatted_key = re.sub(r"\s+", '_', formatted_key)

            to_return[formatted_key.lower()] = value

        yield to_return


def get_row_iterator(file_handle):
    # we use a protected member of the s3 object, _raw_stream, here to create
    # a generator for data from the s3 file.
    # pylint: disable=protected-access
    file_stream = codecs.iterdecode(
        file_handle._raw_stream, encoding='utf-8')

    reader = csv.DictReader(file_stream)

    return generator_wrapper(reader)
