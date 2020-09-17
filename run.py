from CDApp import app,socketio
import eventlet
import eventlet.wsgi
# eventlet.monkey_patch()

if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)
    socketio.run(app=app, host='0.0.0.0', port=8000, debug=True)
