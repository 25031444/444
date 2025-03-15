from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from . import main

@main.route('/', methods=['GET'])  # 只允许 GET 方法
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')