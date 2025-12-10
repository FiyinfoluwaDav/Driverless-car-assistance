# Driverless Car Assistance

A developer-friendly ADAS stack for demonstrating and developing driverless car technologies.

## Project Overview

This project provides a comprehensive Advanced Driver-Assistance System (ADAS) stack that integrates several key computer vision and control functionalities. The system is designed to be a practical tool for researchers, hobbyists, and developers interested in autonomous driving technology.

The core features of the project include:

*   **Lane Segmentation:** The system can accurately identify and segment lane markings on the road, providing crucial information for lane-keeping and navigation.
*   **Object Detection:** Using state-of-the-art object detection models, the system can identify and track various objects such as cars, pedestrians, and traffic signs.
*   **Behavioral Rules:** The project implements simple yet effective behavioral rules. For example, the system can automatically slow down when entering a designated "red zone" or issue warnings when obstacles are detected in the vehicle's path.
*   **Auto-Mode:** An optional auto-mode allows the system to take control and output steering and throttle commands. This feature is compatible with various controllers and simulators, enabling end-to-end testing of the autonomous driving stack.
*   **Modular Design:** The project is designed with a modular architecture, making it easy to extend and customize. Developers can easily add new features or replace existing modules with their own implementations.

The main goal of this project is to provide a platform for understanding and experimenting with the core components of a driverless car's perception and control system. By leveraging computer vision, the system can interpret the surrounding environment and make intelligent driving decisions.

## Getting Started

To get started with the project, you will need to have Python and several other dependencies installed.

### Prerequisites

*   Python 3.8 or higher
*   Pip (Python package installer)

### Installation

1.  Clone the repository to your local machine:
    ```
    git clone https://github.com/FiyinfoluwaDav/Driverless-car-assistance.git
    ```
2.  Navigate to the project directory:
    ```
    cd Driverless-car-assistance
    ```
3.  Install the required dependencies using pip:
    ```
    pip install -r requirements.txt
    ```

## Usage

Once you have installed the dependencies, you can run the main application.

```
python main.py
```

The application will launch, and you will be able to see the output of the computer vision system in real-time. You can also enable the auto-mode to let the system control the vehicle in a compatible simulator.

## Contributing

Contributions to the project are welcome! If you would like to contribute, please follow these guidelines:

1.  Fork the repository and create a new branch for your feature or bug fix.
2.  Make your changes and ensure that the code is well-tested.
3.  Submit a pull request with a clear description of your changes.

We appreciate your help in making this project better!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
