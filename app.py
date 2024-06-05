from flask import Flask, render_template, request, redirect, url_for, session, flash
import vault
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)


def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


@app.route('/')
def index():
    if 'bg_color' not in session:
        session['bg_color'] = generate_random_color()
    return render_template('index.html')


@app.route('/create_vault', methods=['GET', 'POST'])
def create_vault():
    if request.method == 'POST':
        vault_name = request.form['vault_name']
        master_password = request.form['master_password']
        confirm_password = request.form['confirm_password']
        if master_password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for('create_vault'))
        try:
            vault.create_vault(vault_name, master_password)
            session['bg_color'] = generate_random_color(
            )  # Generate new color on vault creation
            flash("Vault created successfully", "success")
            return redirect(url_for('index'))
        except FileExistsError:
            flash("A vault with this name already exists", "danger")
            return redirect(url_for('create_vault'))
    return render_template('create_vault.html')


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        vault_name = request.form['vault_name']
        master_password = request.form['master_password']
        vault_data, key = vault.sign_in(vault_name, master_password)
        if vault_data:
            session['vault_name'] = vault_name
            session['key'] = key
            session['bg_color'] = generate_random_color(
            )  # Generate new color on sign in
            flash("Signed in successfully", "success")
            return redirect(url_for('vault_dashboard'))
        flash("Invalid vault name or password", "danger")
        return redirect(url_for('sign_in'))
    return render_template('sign_in.html')


@app.route('/vault_dashboard')
def vault_dashboard():
    if 'vault_name' not in session:
        flash("Please sign in first", "warning")
        return redirect(url_for('sign_in'))
    vault_name = session['vault_name']
    vault_data = vault.load_vault(vault_name)
    return render_template('vault_dashboard.html',
                           records=vault_data['records'])


@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    if 'vault_name' not in session:
        flash("Please sign in first", "warning")
        return redirect(url_for('sign_in'))
    if request.method == 'POST':
        vault_name = session['vault_name']
        key = session['key']
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        vault_data = vault.load_vault(vault_name)
        vault.create_password_record(vault_data, key, name, username, password)
        flash("Password record added successfully", "success")
        return redirect(url_for('vault_dashboard'))
    return render_template('add_record.html')


@app.route('/retrieve_password', methods=['POST'])
def retrieve_password():
    if 'vault_name' not in session:
        flash("Please sign in first", "warning")
        return redirect(url_for('sign_in'))
    vault_name = session['vault_name']
    key = session['key']
    record_name = request.form['name']
    vault_data = vault.load_vault(vault_name)
    username, password = vault.retrieve_password_record(
        vault_data, key, record_name)
    if username and password:
        return f"Username: {username}<br>Password: {password}"
    flash("Record not found", "danger")
    return redirect(url_for('vault_dashboard'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
