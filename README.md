# LineBot Universal Recipe

## Overview

Welcome to the LineBot Universal Recipe project, an innovative solution at the intersection of culinary exploration and advanced technology. This platform leverages state-of-the-art machine learning algorithms and meticulous data engineering to revolutionize how users discover and explore recipes. Powered by YOLO (You Only Look Once) technology, it identifies ingredients from images, enhancing the user experience by making recipe discovery both interactive and intuitive.

## Features

- **Ingredient Recognition**: Uses YOLO technology to identify ingredients from user-uploaded images.
- **Automated Web Scraping**: Continuously scrapes the web to curate a comprehensive repository of recipes from top culinary websites.
- **Personalized Recommendations**: Provides recipe suggestions based on user preferences, dietary restrictions, and culinary interests.
- **Interactive Interface**: Integrates with LINE Messaging API to deliver a seamless chatbot experience for users seeking recipe recommendations.

## Environment Setup

To set up the development environment for the LineBot Universal Recipe project, follow these steps:

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/sandy1990418/LineBot-Universal-Recipe.git
    cd LineBot-Universal-Recipe
    ```

2. **Install Dependencies**:
    Ensure you have Python and pip installed. Then, install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set Up YOLO**:
    Download the YOLO model weights and configuration files and place them in the appropriate directory as specified in the project configuration.

4. **Environment Variables**:
    Set up the necessary environment variables for LINE Messaging API and other configurations.

## Usage

To run the application, execute the following command:

```sh
python app.py
