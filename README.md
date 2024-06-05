# Password Manager

Welcome to the Password Manager project! This application allows users to create and manage password vaults securely. It includes features such as creating a new vault, signing into an existing vault, adding password records, and retrieving stored passwords. The application uses Flask for the backend and Bootstrap for a responsive UI. Additionally, each user session gets a unique background color for a personalized experience.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [API Endpoints](#api-endpoints)
- [Customization](#customization)
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Create Vault**: Users can create a new password vault with a master password.
- **Sign In**: Users can sign into an existing vault using the vault name and master password.
- **Add Record**: Users can add new password records to their vault.
- **Retrieve Password**: Users can retrieve stored passwords by specifying the record name.
- **Dynamic Background Color**: Each user session gets a unique background color.

## Installation

### Prerequisites

- Python 3.10+
- Flask
- Bootstrap (included via CDN)
- Cryptography package

### Steps

1. Clone the repository:

    ```sh
    git clone https://github.com/srinivassivaratri/password-manager.git
    cd password-manager
    ```

2. Create a virtual environment:

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Run the application:

    ```sh
    python app.py
    ```

5. Open your browser and navigate to `http://localhost:5000` to use the application.

## Usage

1. **Home Page**: The home page allows you to create a new vault or sign into an existing vault.

2. **Create Vault**:
    - Click on "Create Vault".
    - Enter a vault name, master password, and confirm the password.
    - Click "Create Vault" to create the vault.

3. **Sign In**:
    - Click on "Sign In".
    - Enter the vault name and master password.
    - Click "Sign In" to access your vault.

4. **Vault Dashboard**:
    - Once signed in, you will see the vault dashboard.
    - Click on "Add Record" to add a new password record.
    - Enter the record name, username, and password, then click "Add Record".
    - To retrieve a password, click "Show Password" next to the desired record.

## File Structure

The project is organized into the following structure:


### File Descriptions

- **static/styles.css**: Contains the custom CSS styles for the application.
- **templates/base.html**: The base template that other templates extend from.
- **templates/index.html**: The homepage template.
- **templates/create_vault.html**: Template for creating a new vault.
- **templates/sign_in.html**: Template for signing into an existing vault.
- **templates/vault_dashboard.html**: Dashboard template to view and manage password records.
- **templates/add_record.html**: Template for adding a new password record.
- **app.py**: The main application file that sets up the Flask server and routes.
- **vault.py**: Contains the functions to handle vault operations (create, read, update, delete).
- **requirements.txt**: Lists the Python dependencies required for the project.
- **.replit**: Configuration file for running the project on Replit.
- **README.md**: This file, providing an overview of the project.

## API Endpoints

- `GET /`: Home page.
- `GET /create_vault`: Form to create a new vault.
- `POST /create_vault`: Create a new vault.
- `GET /sign_in`: Form to sign into an existing vault.
- `POST /sign_in`: Sign into a vault.
- `GET /vault_dashboard`: Dashboard to view and manage password records.
- `GET /add_record`: Form to add a new password record.
- `POST /add_record`: Add a new password record.
- `POST /retrieve_password`: Retrieve a password record.

## Customization

### Changing the Background Color Logic

If you want to customize how background colors are generated or applied, modify the `generate_random_color` function in `app.py` and the `base.html` template:

```python
def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))
```


In base.html`:
```
<style>
    body {
        background-color: {{ session['bg_color'] }};
    }
</style>
```

Updating Styles:
To update the styles, edit styles.css in the static folder.

    Security Considerations
    Encryption: Ensure all sensitive data is encrypted using robust algorithms.
    HTTPS: Use HTTPS to secure data transmission.
    Input Validation: Validate all user inputs to prevent injection attacks.
    Session Management: Implement secure session management practices.

Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure your code follows best practices and includes necessary tests.

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

### Save the File

1. **After pasting the content**, save the file by clicking the save icon or pressing `Ctrl+S`.

### Commit and Push the README.md File

1. **Open the Shell tab**.

2. **Add the new README.md file to Git**:

    ```sh
    git add README.md
    ```

3. **Commit the new file**:

    ```sh
    git commit -m "Add README.md"
    ```

4. **Push the commit to GitHub**:

    ```sh
    git push -u origin main
    ```

By following these steps, you will have successfully created and pushed the `README.md` file to your GitHub repository from Replit. If you encounter any issues or need further assistance, please let me know!
