![Header](assets/full_logo_colors.png)
# BioTrack
> A pipeline for the analysis of patient gut microbiome data with easy-to-read report generation.
<!-- <img style="float: right;" src="assets/logo_b_background.png"> -->

[![Version](https://img.shields.io/badge/verison-v0.0.1-red)](http://www.gnu.org/licenses/agpl-3.0)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

One to two paragraph statement about your product and what it does.
- has a sample nextflow alignment script
- we ran this on x samples
- ML to determine: association of patient health to gut biome
- compare your sample to it!
- generate a report based on this

# Installation
WIP
<!-- OS X & Linux:

```sh
npm install my-crazy-module --save
```

Windows:

```sh
edit autoexec.bat
``` -->


# Usage example

A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

_For more examples and usage, please refer to the [Wiki][wiki]._

# Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.
<!-- 
```sh
make install
npm test
``` -->


## Python Environment Setup (For Nextflow Alignment Pipeline)
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

# Creators
Arya Gautam – [Linkedin](https://www.linkedin.com/in/arya-gautam-a9a125204/) – YourEmail@example.com

Natalie Bratset – [Linkedin](https://www.linkedin.com/in/nbratset/) – YourEmail@example.com

Distributed under the AGPL-3.0 license. See ``LICENSE`` for more information.

This software was developed as part of CU Boulder's Software Engineering for Scientists (CSCI 6118) course.

# Acknowledgements
We would like to thank CU Boulder's IQ Biology Program, BioFrontiers, and the NSF fortheir support on this project.

We would also like to thank CU Boulder's [Biofrontiers IT Team (BIT)](https://bit.colorado.edu/) for allowing us to use their Fiji Computing Cluster, and for many emails and meetings of troubleshooting.


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