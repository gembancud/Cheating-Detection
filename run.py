from CDApp import app, socketio

if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)
    socketio.run(app=app, host='0.0.0.0', port=5001)