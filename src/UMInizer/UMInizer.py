#!/usr/bin/env python

import click
import logging
import gzip


def umi_transform(fastq):
    """
    Parse fastq header and move UMI sequence to the appropriate tag
    """
    for line in fastq:
        if line.startswith("@"):
            header = line.strip()
            read_name, index = header.split()
            read_name = read_name.split(":")
            if len(read_name) == 8:
                umi = f"RX:Z:{read_name[7]}"
                read_name.pop()
                yield f"{':'.join(read_name)} {index}\t{umi}"
            else:
                yield header
        else:
            yield line


def interleave(fh1, fh2):
    """
    Interleave paired end reads
    """
    while True:
        line = fh1.readline()
        if line.strip() == "":
            break
        yield (line.strip())

        for i in range(3):
            yield (fh1.readline().strip())

        for i in range(4):
            yield (fh2.readline().strip())


@click.command()
@click.version_option()
@click.option(
    "--loglevel",
    default="INFO",
    type=click.Choice(
        ["INFO", "WARNING", "DEBUG", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    help="Set logging level",
)
@click.argument("fastq1", required=True)
@click.argument("fastq2", default=None, required=False)
def uminizer(fastq1, fastq2, loglevel="INFO"):
    """
    Utility to transform UMI's in Illumina fastq headers to UMI in separate tags. Outputs a new (interleaved) fastq file.
    This tool was built to parse output from Illumina bclconvert where the "OverrideCycles" option was used.
    """

    # configure logging
    logging.basicConfig(
        format="[%(levelname)s - %(asctime)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=getattr(logging, loglevel, None),
    )
    logging.debug(f"Set loglevel to {loglevel}")

    # check if fastq2 is provided
    if fastq2:
        # open fastq files
        logging.info(f"Opening fastq files: {fastq1} and {fastq2}")
        with gzip.open(fastq1, "rt") as fh1, gzip.open(fastq2, "rt") as fh2:
            # interleave fastq files
            logging.info("Interleaving fastq files")
            interleaved = interleave(fh1, fh2)
            [print(line.strip()) for line in umi_transform(interleaved)]
    else:
        logging.info("Opening fastq file: {fastq1}")
        with gzip.open(fastq1, "rt") as fh:
            [print(line.strip()) for line in umi_transform(fh)]


if __name__ == "__main__":
    uminizer()
