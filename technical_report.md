# Nexus Learn - Technical Report

## Overview
Nexus Learn is a modular, CLI-based e-learning system designed to provide a lightweight yet powerful platform for academic management. It facilitates interactions between Students, Teachers, and Administrators through a secure terminal interface, allowing for efficient management of users and educational content without the overhead of a web server or heavy database.

## Architecture & Technology Stack
The application follows a modular monolith architecture, ensuring high cohesion and low coupling between logical units:

### Core Framework
- **Language**: Python 3.10+ utilizing standard libraries for maximum portability.
- **Modularity**: Logic is divided into specialized modules (`admin.py`, `responsable.py`, `utilisateur.py`, `authentification.py`) to manage role-specific functionalities independently.
- **UI System**: A custom `ui.py` module handles terminal formatting, utilizing ANSI color codes for a modern, high-contrast visual experience.

### Data Management
- **Persistence Layer**: Data is persisted in a local `nexus_db.json` file.
- **Storage Strategy**: Uses nested dictionaries within the application memory, which are serialized/deserialized via the `json` module. 
- **Integrity**: Automatic data loading on startup and atomic saving on modification ensures state consistency.

## Key Technical Capabilities

### 1. Multi-Role Navigation System
The portal implements dynamic routing based on authenticated roles:
- **Administrator**: Global visibility of the user base and account lifecycle management (deletion).
- **Teacher (Responsable)**: Full CRUD ownership over courses, allowing instructors to manage their own curriculum.
- **Student (Utilisateur)**: Read-only access to a centralized course catalog.

### 2. Secure Authentication Workflow
The system implements a robust login mechanism with:
- **Attempt Limiting**: A maximum of three failed attempts before returning to the main menu.
- **Dynamic ID Generation**: Automatic generation of unique identifiers for new users and courses.
- **Role-Based Menus**: Execution flows are strictly isolated per role, preventing unauthorized access to administrative functions.

### 3. Interactive UX in Terminal
Despite being a CLI application, Nexus Learn prioritizes user experience through:
- **Visual Feedback**: Success/Failure messages marked with distinct colors (Green/Red).
- **Loading Simulations**: `ui.loading()` functions to provide temporal feedback for processing tasks.
- **Input Sanitization**: Basic stripping and validation of user inputs to prevent runtime crashes.

## Future Scalability
The modular nature of Nexus Learn allows for several expansion paths:
- **SQL Integration**: Swapping the `data.py` logic to use SQLite or PostgreSQL for better concurrent access handling.
- **Web API Layer**: Wrapping the core logic in a FastAPI or Flask app to serve as a backend for a modern frontend.
- **Enrollment Logic**: Adding many-to-many relationships between students and courses to track progress and grades.
