<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the repo and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->





<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- 
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
-->




<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/gembancud/Cheating-Detection">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Live Exam Cheating Detection</h3>

  <p align="center">
    A Cheating Detection System using OpenPose Pose Estimation and XGBoost
    <br />
    <a href="https://github.com/gembancud/Cheating-Detection"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/gembancud/Cheating-Detection">View Demo</a>
    ·
    <a href="https://github.com/gembancud/Cheating-Detection/issues">Report Bug</a>
    ·
    <a href="https://github.com/gembancud/Cheating-Detection/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

# This Project is currently in development

There are many great README templates available on GitHub, however, I didn't find one that really suit my needs so I created this enhanced one. I want to create a README template so amazing that it'll be the last one you ever need.

Here's why:
* Your time should be focused on creating something amazing. A project that solves a problem and helps others
* You shouldn't be doing the same tasks over and over like creating a README from scratch
* You should element DRY principles to the rest of your life :smile:

Of course, no one template will serve all projects since your needs may be different. So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue.

A list of commonly used resources that I find helpful are listed in the acknowledgements.

### Built With
This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [XGBoost](https://xgboost.readthedocs.io/en/latest/)




<!-- GETTING STARTED -->
## Getting Started
To get a local copy up and running follow these simple example steps.

### Prerequisites

- **Requirements** for the default configuration (you might need more resources with a greater `--net_resolution` and/or `scale_number` or less resources by reducing the net resolution and/or using the MPI and MPI_4 models):
    - CUDA (Nvidia GPU) version:
        - NVIDIA graphics card with at least 1.6 GB available (the `nvidia-smi` command checks the available GPU memory in Ubuntu).
        - At least 2.5 GB of free RAM memory for BODY_25 model or 2 GB for COCO model (assuming cuDNN installed).
        - Highly recommended: cuDNN.
    - OpenCL (AMD GPU) version:
        - Vega series graphics card
        - At least 2 GB of free RAM memory.
    - CPU-only (no GPU) version:
        - Around 8GB of free RAM memory.
    - Highly recommended: a CPU with at least 8 cores.
- **Dependencies**:
    - OpenCV (all 2.X and 3.X versions are compatible).

### Installation

1. Clone the repo
```sh
git clone https://github.com/gembancud/Cheating-Detection.git
```
2. Install Python packages
```sh
pip install -r requirements.txt
```
3. Download [Compiled OpenPose Models](https://drive.google.com/file/d/1OmsF-PqlyDessAruHpESvOnC89eAl4Vz/view?usp=sharing) and move to:
```sh
Cheating-Detection/CheatDetection/
```



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/gembancud/Cheating-Detection/issues) for a list of proposed features (and known issues).

Author's personal [documentation](https://github.com/othneildrew/Best-README-Template/blob/master/README.md) hosted on Google Sheets



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Gil Emmanuel Bancud - [@iamuPnP](https://www.facebook.com/iamuPnP) - gembancud@gmail.com

Project Link: [https://github.com/gembancud/Cheating-Detection](https://github.com/gembancud/Cheating-Detection)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
* [XGBoost](https://github.com/dmlc/xgboost)
* [Flask](https://github.com/pallets/flask)
* [Corey Shafer](https://www.youtube.com/user/schafer5)
* [Miguel Grinberg](https://blog.miguelgrinberg.com/index)
* [Best README Template](https://github.com/othneildrew/Best-README-Template/blob/master/README.md)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=flat-square
[contributors-url]: https://github.com/gembancud/Cheating-Detection/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=flat-square
[forks-url]: https://github.com/gembancud/Cheating-Detection/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=flat-square
[stars-url]: https://github.com/gembancud/Cheating-Detection/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=flat-square
[issues-url]: https://github.com/gembancud/Cheating-Detection/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/gembancud/Cheating-Detection/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/gil-emmanuel-bancud-140502104/
[product-screenshot]: images/screenshot.png
