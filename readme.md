
# Parking Management System

## Overview

This Parking Management System is developed by users with the following IDs: 112103034 & 112103026.

## Requirements

- Flask
- Flask-SQLAlchemy
- Flask-Mail
- ReportLab

## Getting Started

1. Install the required packages:

   ```bash
   pip install Flask Flask-SQLAlchemy Flask-Mail ReportLab
   ```

2. Configure the `config.json` file with the necessary parameters.

3. Run the application:

   ```bash
   python main.py
   ```

4. Open a web browser and navigate to [http://localhost:5000/](http://localhost:5000/) to access the application.

## Features

- **Contact Form:** Users can submit inquiries or messages via the contact form.
- **Vehicle Entry:** Add vehicles to the parking lot, specifying details such as vehicle number, owner name, and entry time.
- **Vehicle Removal:** Remove vehicles from the parking lot, calculating the bill based on the duration of stay and vehicle type.
- **Dashboard:** Access the admin dashboard after logging in with the provided credentials.
- **Parked Vehicles:** View details of currently parked vehicles.

## Usage

1. Visit [http://localhost:5000/](http://localhost:5000/) to access the home page.
2. Use the navigation menu to explore different sections of the application.
3. Admins can log in to the dashboard using the provided credentials.
4. Add vehicles, remove vehicles, and view parked vehicles accordingly.

## Configuration

- The application uses a `config.json` file for configuration parameters such as database URI, mail server details, etc.

## Contributing

Contributions are welcome! Follow these steps:

1. Fork the project.
2. Create a new branch for your feature: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request.

## Acknowledgments

- The project uses Flask, Flask-SQLAlchemy, Flask-Mail, and ReportLab.


