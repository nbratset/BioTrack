![Header](src/assets/full_logo_colors.png)
# BioTrack
> A pipeline for the analysis of patient gut microbiome data with easy-to-read report generation.

[![Version](https://img.shields.io/badge/verison-v0.0.1-red)](http://www.gnu.org/licenses/agpl-3.0)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

One to two paragraph statement about your product and what it does.
- has a sample nextflow alignment script
- we ran this on x samples
- ML to determine: association of patient health to gut biome
- compare your sample to it!
- generate a report based on this


# Installation
**OS X & Linux:**

```sh
git clone https://github.com/nbratset/BioTrack.git
```

**Windows:**

```sh
git clone https://github.com/nbratset/BioTrack.git
```

**Alternative:**
> Download a ZIP of the full repository
![zip](https://i.sstatic.net/89Oxe.png)

# Usage example
## Step 1: Nextflow Pipeline for Patient Sample Alignment
This first step is to take the gut microbiome patient samples and align them. This pipeline will generate a metaphlan output, which is used in later analysis. 

See `Nextflow Alignment Pipeline Python Environment Setup` below to set up your python virtual environment to run this pipeline.






A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

_For more examples and usage, please refer to the [Wiki][wiki]._

# Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.
<!-- 
```sh
make install
npm test
``` -->
## Nextflow Alignment Pipeline Python Environment Setup
### 1. Install [micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html)
This will depend heavily on your system. For our HPC, we used the following command:
```sh
curl micro.mamba.pm/install.sh | bash
```

### 2. Create a nextflow virtual environment (for alignment pipeline)
```sh
micromamba create -n nextflow_env -c bioconda -c conda-forge nextflow
```

```sh
micromamba activate nextflow_env
```

### 3. Install dependancies
```sh
micromamba install -c conda-forge -c bioconda metaphlan=3.1.0
micromamba install -c conda-forge -c bioconda fastqc
micromamba install -c conda-forge -c bioconda fastp
micromamba install -c conda-forge -c bioconda bowtie2
micromamba install -c conda-forge -c bioconda multiqc
```

## Report Generation Python Environment Setup
### 1. Install [micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html)
This will depend heavily on your system. For our HPC, we used the following command:
```sh
curl micro.mamba.pm/install.sh | bash
```

### 2. Create a virtual environment (for report generation)
```sh
micromamba create -n biotrack_report_env python=3.11
```

```sh
micromamba activate biotrack_report_env
```

### 3. Install dependancies
```sh
micromamba install numpy
micromamba install pandas
micromamba install matplotlib
micromamba install plotly
micromamba install dash
micromamba install dash_bootstrap_components
```

# Release History

<!-- * 0.2.1
    * CHANGE: Update docs (module code remains unchanged)
* 0.2.0
    * CHANGE: Remove `setDefaultXYZ()`
    * ADD: Add `init()`
* 0.1.1
    * FIX: Crash when calling `baz()` (Thanks @GenerousContributorName!)
* 0.1.0
    * The first proper release
    * CHANGE: Rename `foo()` to `bar()` -->
* 0.0.1
    * Work in progress

# Data Information and Model Processing
We downloaded 3 studies ([PRJNA945504](https://www.ncbi.nlm.nih.gov/bioproject/?term=PRJNA945504), [PRJNA398089](https://www.ncbi.nlm.nih.gov/bioproject/398089), [PRJNA400072](https://www.ncbi.nlm.nih.gov/bioproject/400072)) of microbiome data totalling to 2,034 samples with our script [`run_download_fastqs.sh`](https://github.com/nbratset/BioTrack/blob/main/scripts/run_download_fastqs.sh).

We used these samples with scikit.learn to train a model to differentiate patients who are healthy, have Ulcerative Colitis, or Crohn's disease. (file path to these processed data?)

# Creators
Arya Gautam – [Linkedin](https://www.linkedin.com/in/arya-gautam-a9a125204/) – [CU Profile](https://www.colorado.edu/certificate/iqbiology/natalie-marie-bratset)

Natalie Bratset – [Linkedin](https://www.linkedin.com/in/nbratset/) – [CU Profile](https://www.colorado.edu/certificate/iqbiology/arya-gautam)

Distributed under the AGPL-3.0 license. See ``LICENSE`` for more information.

This software was developed as part of CU Boulder's Software Engineering for Scientists (CSCI 6118) course.

# Acknowledgements
We would like to thank CU Boulder's IQ Biology Program, BioFrontiers, and the NSF for their support on this project.

We would also like to thank CU Boulder's [Biofrontiers IT Team (BIT)](https://bit.colorado.edu/) for allowing us to use their Fiji Computing Cluster, and for many emails and meetings of troubleshooting.

DISCLAIMER: This project, code, and reports generated do not provide medical advice. The information generated in the report is intended to be reviewed by a medical professional and cannot independently provide medical diagnoses. Always seek the advice of your physician or medical health provider for an official diagnosis and treatment information.


<!-- ## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
<!-- [npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki -->
