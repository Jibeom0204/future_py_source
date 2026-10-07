from flask import Flask, render_template,render_template_string, request,make_response,redirect, session,url_for,flash
import pymysql,os;

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123")
DB_NAME = os.getenv("DB_NAME", "test")

def get_connFunc():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4" ,# 전세계 문자(한글 포함)+이모지까지 처리가능
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )