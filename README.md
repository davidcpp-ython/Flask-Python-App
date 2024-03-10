# Flask Emergency App


Emergency application designed to showcase basic functionalities of Flask. It utilizes Flask along with Flask extensions such as Flask-Login, Flask-Mail, and Flask-SQLAlchemy.

## Setup

1. **Install Dependencies**: Before running the application, ensure you have Python installed on your system. You can install the required dependencies using pip:

    ```
    pip install flask flask-login flask-mail sqlalchemy
    ```

2. **Environment Variables**:
   - Create a `.env` file in the root directory of the project.
   - Use the template below to define necessary environment variables:

    ```plaintext
    # .env

    # Mail configuration
    MAIL_SERVER=
    MAIL_PORT=
    MAIL_USE_TLS=
    MAIL_USE_SSL=
    MAIL_USERNAME=
    MAIL_PASSWORD=
    MAIL_DEFAULT_SENDER=
    ```

    Replace placeholders (`<...>`) with appropriate values.

3. **Database Setup**: Ensure your database is set up and running. Update the `SQLALCHEMY_DATABASE_URI` and `SECRET_KEY` in the `__init__.py` file with the appropriate database connection string.

4. **Run the Application**: Once dependencies are installed and environment variables are configured, you can run the Flask application:

    ```
    flask run
    ```

    By default, the application will be accessible at `http://localhost:5000`.
