# UMInizer

Utility to transform UMI's in Illumina fastq headers to UMI in separate tags. Outputs a new (interleaved) fastq file.
This tool was built to parse output from Illumina bcl-convert where the "OverrideCycles" option was used.

## Installation

```
pip install git+https://github.com/CenterForMedicalGeneticsGhent/UMInizer.git

```

or

```bash
python setup.py install

```

## Usage

```bash
UMInizer fastq_R1.fastq.gz fastq_R2.fastq.gz | bgzip -c > interleaved.fastq.gz
```
