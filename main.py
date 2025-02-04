from server import app, initDB


def main():
    app.run(debug=True,host="0.0.0.0",port=5001)
if __name__ == "__main__":
    initDB()
    main()