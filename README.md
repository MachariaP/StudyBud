# StudyBud

StudyBud is a collaborative learning platform where users can join discussion rooms, explore different topics, and share knowledge. This application provides a space for users to connect, learn, and grow together in a supportive online community.

[GitHub Repository](https://github.com/MachariaP/StudyBud.git)

## Table of Contents

-   [Description](#description)
-   [Features](#features)
-   [Installation](#installation)
-   [Usage](#usage)
-   [License](#license)
-   [Credits](#credits)

## Description

StudyBud enables users to explore rooms dedicated to various subjects, participate in topic-specific discussions, and collaborate with others. Each room allows users to share insights, ask questions, and learn collaboratively, making it a great resource for anyone committed to continuous learning.

## Features

-   **Topic Rooms**: Join specific rooms to discuss or learn about particular topics.
-   **Search Functionality**: Find rooms or topics of interest quickly.
-   **User Profiles**: Each user can create and maintain a profile.
-   **Community Collaboration**: Engage with others on a journey of shared knowledge.

## Installation

1.  **Clone the repository**:
    
    bash
    
    Copy code
    
    `git clone https://github.com/MachariaP/StudyBud.git
    cd StudyBud` 
    
2.  **Set up a virtual environment** (optional but recommended):
    
    bash
    
    Copy code
    
    `python3 -m venv venv
    source venv/bin/activate` 
    
3.  **Install the dependencies**:
    
    bash
    
    Copy code
    
    `pip install -r requirements.txt` 
    
4.  **Set up the Database**:
    
    -   Run migrations to set up the database schema:
        
        bash
        
        Copy code
        
        `python manage.py migrate` 
        
5.  **Create a Superuser**:
    
    bash
    
    Copy code
    
    `python manage.py createsuperuser` 
    
6.  **Run the Development Server**:
    
    bash
    
    Copy code
    
    `python manage.py runserver` 
    
7.  **Access the application**:
    
    -   Open your web browser and go to `http://127.0.0.1:8000`.

## Usage

1.  **Sign up / Log in** to create or access your account.
2.  **Browse Rooms** to find discussions on topics of interest.
3.  **Join or Start Discussions** within a room to share insights or ask questions.
4.  **Create and Manage Topics** that matter to you, facilitating conversations with like-minded individuals.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

This project was inspired by and developed with guidance from **Dennis Ivy**.
