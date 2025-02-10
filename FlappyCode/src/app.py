from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory,
    session,
    redirect,
    url_for,
)
from dotenv import load_dotenv
from flask_cors import CORS
import pyodbc
import logging
from logging_loki import LokiHandler
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import sys

app = Flask(__name__, static_url_path="")

load_dotenv()  

LOGIN_HTML = "login.html"
INTERNAL_SERVER_ERROR_MESSAGE = "Internal server error"

app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "your-secret-key"
#Session(app)
CORS(app)

keyVaultName = os.getenv("KEY_VAULT_NAME")

KVUri = f"https://{keyVaultName}.vault.azure.net"

# Authenticate and create a client for Key Vault
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=KVUri, credential=credential)


def get_secret(secret_name):
    secret = secret_client.get_secret(secret_name)
    return secret.value


AZURE_SQL_SERVER = get_secret("AZURE-SQL-SERVER")
AZURE_SQL_DATABASE = get_secret("AZURE-SQL-DATABASE")
AZURE_SQL_USERNAME = get_secret("AZURE-SQL-USERNAME")
AZURE_SQL_PASSWORD = get_secret("AZURE-SQL-PASSWORD")

connection_string = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER=tcp:{AZURE_SQL_SERVER}.database.windows.net,1433;"
    f"DATABASE={AZURE_SQL_DATABASE};"
    f"UID={AZURE_SQL_USERNAME};"
    f"PWD={AZURE_SQL_PASSWORD};"
    f"TrustServerCertificate=yes;Connection Timeout=30;"
)
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()


def initialize_database():
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
    CREATE TABLE users (
        id INT IDENTITY PRIMARY KEY,
        username NVARCHAR(255) NOT NULL UNIQUE,
        password NVARCHAR(255) NOT NULL
    )
    """)
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='scores' AND xtype='U')
    CREATE TABLE scores (
        id INT IDENTITY PRIMARY KEY,
        username NVARCHAR(255) NOT NULL,
        score FLOAT NOT NULL
    )
    """)
    conn.commit()

initialize_database()


@app.route("/")
def serve_index():
    if "username" not in session:
        return redirect(url_for("login"))
    return send_from_directory("static", "index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            data = request.json
            username = data.get("username")
            password = data.get("password")

            if not username or username.strip() == "":
                return jsonify({"error": "Username is required"}), 400
            if not username.strip().isalpha():
                return jsonify({"error": "Username must contain only letters"}), 400
            
            cursor.execute("SELECT username FROM users WHERE username = ?", username)
            user = cursor.fetchone()
            if not user:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, password)
                conn.commit()
                session["username"] = username
                return jsonify({"message": "Registration successful!"}), 200
            else:
                return jsonify({"message": "Username already exists"}), 200

        except Exception as e:
            app.logger.error(f"Unexpected error during registration: {e}")
            return jsonify({"error": "Internal server error"}), 500
    return send_from_directory("static", login.html)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            data = request.json
            username = data.get("username")
            password = data.get("password")

            cursor.execute("SELECT password FROM users WHERE username = ?", username)
            user = cursor.fetchone()

            if user == None:
                return jsonify({"error": "Username must be registerd"}), 400
            stored_password = user[0]
            if password == stored_password:
                session["username"] = username
                app.logger.info(f"{username} - Login success from Loki.")
                return jsonify({"message": "Login successful!", "redirect_url": "/"}), 200
            else:
                return jsonify({"error": "The password is wrong"}), 400


        except Exception as e:
            app.logger.error(f"Unexpected error during login: {e}")
            return jsonify({"error": INTERNAL_SERVER_ERROR_MESSAGE}), 500

    return send_from_directory("static", "login.html")


@app.route("/logout", methods=["POST"])
def logout():
    try:
        session.clear()
        return send_from_directory("static", LOGIN_HTML)
    except Exception as e:
        app.logger.error(f"Unexpected error during logout: {e}")
        return jsonify({"error": INTERNAL_SERVER_ERROR_MESSAGE}), 500


@app.route("/submit-score", methods=["POST"])
def submit_score():
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.json
        score = data.get("score")
        if not isinstance(score, (int, float)):
            return jsonify({"error": "Invalid data"}), 400
        
        cursor.execute("SELECT score FROM scores WHERE username = ?", session["username"])
        existing_score = cursor.fetchone()

        if existing_score:
            # Update score only if the new score is higher
            if score > existing_score[0]:
                cursor.execute(
                    "UPDATE scores SET score = ? WHERE username = ?",
                    (score, session["username"])
                )
        else:
            # Insert a new record if no existing score is found
            cursor.execute(
                "INSERT INTO scores (username, score) VALUES (?, ?)",
                (session["username"], score)
            )

            # Commit changes to the database
        conn.commit()

        return jsonify({"message": "Score submitted successfully!"}), 200

    except Exception as e:
        app.logger.error(f"Unexpected error during score submission: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    try:
        cursor.execute("SELECT TOP 20 username, score FROM scores ORDER BY score DESC")
        top_scores = cursor.fetchall()

        leaderboard = [{"username": row[0], "score": row[1]} for row in top_scores]

        return jsonify(leaderboard), 200

    except Exception as e:
        app.logger.error(f"Unexpected error while fetching leaderboard: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/health", methods=["GET"])
def health_check():
    try:
        return jsonify({"status": "UP"}), 200
    except Exception as e:
        return jsonify({"status": "DOWN", "error": str(e)}), 500


if __name__ == "__main__":
    try:
        app.run(debug=True, host="0.0.0.0", port=3000)
    except Exception as e:
        app.logger.error(f"Unexpected error during application startup: {e}")

