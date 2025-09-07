from web.sockets import socketio
from flask_socketio import join_room


@socketio.on("connect", namespace="/admin")
def handle_admin_connect():
    join_room("admin_room")
    print("Admin connected and joined admin_room")
    # socketio.emit("new_order", {"id": 123}, namespace="/admin", room="admin_room")
