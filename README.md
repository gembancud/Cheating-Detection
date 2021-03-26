<br />
<p align="center">
  <a href="https://github.com/gembancud/Cheating-Detection" />


  <h3 align="center">Live Exam Cheating Detection</h3>

  <p align="center">
    A Cheating Detection System using OpenPose Pose Estimation and XGBoost
    <br />
    <a href="https://youtu.be/1iesgJBp6Qc">View Demo</a>
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

Abstract - Academic cheating is the use of prohibited methods to gain an unlawful advantage during academic tests and examinations. This study proposes the use of cutting-edge
machine learning, particularly deep learning, to utilize pose estimation on examinees to determine if they are cheating. A proctor’s monitoring system was developed alongside the assistive monitoring device using the Nvidia Jetson Nano. A web application was developed to allow the proctor to observe the video feed captured by the device, control the pose estimation and cheating detection features, and review previously stored evidence. The developed system provides real-time capabilities  close to 10 frames per second under the full computational load. Benchmarked on a validated dataset, the system was evaluated with an accuracy of 90%, an f1-score of 89.65%, and an area nder the receiver operating characteristic curve (AUROC) of 0.32%. A demonstrated survey to proctors yields complete greement on the system’s overall effectiveness.

See the complete paper [here!](https://drive.google.com/file/d/1Tb0Qf9gBLiqN-Tclv99ep66OETWkNLQi/view?usp=sharing)

This study has won 1st Runner up in the Ateneo de Davao University Engineering Thesis Awards. See [here!](https://twitter.com/ADDU_SEA/status/1372864898506485766/photo/2)

# This project is no longer under active development but welcomes changes/improvements


### Built With
This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
* [XGBoost](https://xgboost.readthedocs.io/en/latest/)
* [Starlette](https://www.starlette.io/)
* [VidGear](https://abhitronix.github.io/vidgear/)




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
3.
- Download [Compiled OpenPose Models + (Windows)Pyopenpose](https://drive.google.com/file/d/1OmsF-PqlyDessAruHpESvOnC89eAl4Vz/view?usp=sharing) and move to:
- Download [(Linux)Pyopenpose library without CuDnn](https://drive.google.com/file/d/1Ax1EQ9tfd0iKBmUNynaRHffKdKQ0bvSj/view?usp=sharing) and move to:
- Download [(Linux)Pyopenpose library with CuDnn](https://drive.google.com/file/d/1WXsR7AM23nt9AAdxuJe6jT8FpXjsOV85/view?usp=sharing) and move to:
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

Author's personal [documentation](https://docs.google.com/spreadsheets/d/1rPMHePNQsHh3moOTQ3r7VIakKBZ2deZtDosMtV5RZo4/edit?usp=sharing) hosted on Google Sheets



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

[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
* [XGBoost](https://github.com/dmlc/xgboost)
* [Corey Shafer](https://www.youtube.com/user/schafer5)
* [Miguel Grinberg](https://blog.miguelgrinberg.com/index)
* [Abhishek Thakur](https://github.com/abhiTronix)
* [Starlette](https://www.starlette.io/)
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
