<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the repo and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->




# Using deep neural networks to recognize hand gestures to control a mobile robot using a camera.
The purpose of this project was to build a system that allows user to control the Arlo mobile robot using static hand gestures, with use of camera. The project consists of three parts, the first was to develop script that supposed to recognize the gestures controlling the robot. For this purpose author used convolutional neural network, which had to be properly trained. The next step was to create a robot program that had to properly react to application commands. The last step was to handle communication between programs, Bluetooth 4.0 Low Energy standard was used for this purpose. Unfortunately, during the final control test Bluetooth module has been damaged, in this case the author decided to use simple serial communication instead. The main assumptions of the project were to achieve real-time processing system and achieve high accuracy of hand gesture recognition. </br>
Arlo: https://www.parallax.com/product/arlo-robotic-platform-system </br>
Presentation: https://www.youtube.com/watch?v=j6qOpACT1z0 </br>

[![ytlink](https://www.androidpolice.com/wp-content/uploads/2013/02/nexusae0_130.png)](https://www.youtube.com/watch?v=j6qOpACT1z0    "Presentation")

### Built With
This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* [Pytorch](https://pytorch.org/)
* [PyQt](https://python101.readthedocs.io/pl/latest/pyqt/)
* [Parallax](https://www.parallax.com/product/28966)
* [Bleak](https://github.com/hbldh/bleak)
* [PySerial](https://github.com/pyserial/pyserial)
* [OpenCv](https://pypi.org/project/opencv-python/)

### Installation

1. Clone the repo
2. Install python 3
3. Install python dependencies, such as: Pytorch, Bleak, PyQt
4. Run script "mainAplication.py"



<!-- USAGE EXAMPLES -->
## Usage



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



## Author

Sylwester Dawida Poland AGH
2020



