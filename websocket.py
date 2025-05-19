# import asyncio
# import websockets
# import json
# from datetime import datetime
# from flask import Flask
# from database.database import db
# from main import create_app
# from  model.chat import Chat , ChatHistory  # Ensure models are imported
# from model.athlete import Athlete
# from model.coach import Coach

# connected_clients = {}

# app = create_app()
# app.app_context().push()

# async def handle_connection(websocket):
#     data = await websocket.recv()
#     user = json.loads(data)
#     connected_clients[user['id']] = websocket
#     print(f"{user['role']} {user['name']} connected")

#     try:
#         while True:
#             data = await websocket.recv()
#             msg_data = json.loads(data)

#             if msg_data["type"] == "chat":
#                 sender = msg_data["sender"]
#                 receiver = msg_data["to"]
#                 message_text = msg_data["message"]

#                 # Save to DB
#                 new_chat = Chat(
#                     athlete_id=sender["id"] if sender["role"] == "athlete" else receiver["id"],
#                     coach_id=sender["id"] if sender["role"] == "coach" else receiver["id"],
#                     message=message_text,
#                     timestamp=datetime.utcnow()
#                 )
#                 db.session.add(new_chat)
#                 db.session.commit()

            
#                 history = ChatHistory(chat_id=new_chat.id)
#                 db.session.add(history)
#                 db.session.commit()

#                 # Send to recipient
#                 recipient_ws = connected_clients.get(receiver["id"])
#                 if recipient_ws:
#                     await recipient_ws.send(json.dumps({
#                         "type": "chat",
#                         "from": sender,
#                         "message": message_text,
#                         "timestamp": new_chat.timestamp.isoformat()
#                     }))

#             elif msg_data["type"] == "typing":
#                 recipient_ws = connected_clients.get(msg_data["to"]["id"])
#                 if recipient_ws:
#                     await recipient_ws.send(json.dumps({
#                         "type": "typing",
#                         "from": msg_data["sender"]
#                     }))

#     except websockets.exceptions.ConnectionClosed:
#         print(f"{user['name']} disconnected.")
#         del connected_clients[user['id']]

# async def main():
#     async with websockets.serve(handle_connection, "localhost", 8785):
#         print("WebSocket server running at ws://localhost:8785")
#         await asyncio.Future()

# if __name__ == "__main__":
#     asyncio.run(main())
# --------------------------------------------------------------------------------------------------------------------------------------
# import asyncio
# import websockets
# import json
# from datetime import datetime
# from flask import Flask
# from database.database import db
# from main import create_app
# from model.chat import Chat, ChatHistory
# from model.athlete import Athlete
# from model.coach import Coach

# connected_clients = {}

# app = create_app()
# app.app_context().push()

# async def handle_connection(websocket):
#     try:
#         # Receive initial user identification message
#         data = await websocket.recv()
#         print("Initial connection message:", data)

#         user = json.loads(data)
#         user_id = user.get("id")
#         user_role = user.get("role")
#         user_name = user.get("name")

#         if not user_id or not user_role or not user_name:
#             await websocket.send(json.dumps({"error": "Missing id, role, or name"}))
#             return

#         connected_clients[user_id] = websocket
#         print(f"{user_role} {user_name} connected")

#         while True:
#             try:
#                 data = await websocket.recv()
#                 print("Message received:", data)

#                 msg_data = json.loads(data)

#                 msg_type = msg_data.get("type")
#                 if not msg_type:
#                     await websocket.send(json.dumps({"error": "Missing message type"}))
#                     continue

#                 if msg_type == "chat":
#                     sender = msg_data.get("sender")
#                     receiver = msg_data.get("to")
#                     message_text = msg_data.get("message")

#                     if not sender or not receiver or not message_text:
#                         await websocket.send(json.dumps({"error": "Incomplete chat message"}))
#                         continue

#                     # Save to DB
#                     new_chat = Chat(
#                         athlete_id=sender["id"] if sender["role"] == "athlete" else receiver["id"],
#                         coach_id=sender["id"] if sender["role"] == "coach" else receiver["id"],
#                         message=message_text,
#                         timestamp=datetime.utcnow()
#                     )
#                     db.session.add(new_chat)
#                     db.session.commit()

#                     history = ChatHistory(chat_id=new_chat.id)
#                     db.session.add(history)
#                     db.session.commit()

#                     # Send to recipient
#                     recipient_ws = connected_clients.get(receiver["id"])
#                     if recipient_ws:
#                         await recipient_ws.send(json.dumps({
#                             "type": "chat",
#                             "from": sender,
#                             "message": message_text,
#                             "timestamp": new_chat.timestamp.isoformat()
#                         }))

#                 elif msg_type == "typing":
#                     recipient_ws = connected_clients.get(msg_data.get("to", {}).get("id"))
#                     if recipient_ws:
#                         await recipient_ws.send(json.dumps({
#                             "type": "typing",
#                             "from": msg_data["sender"]
#                         }))

#             except json.JSONDecodeError:
#                 await websocket.send(json.dumps({"error": "Invalid JSON message"}))
#             except Exception as inner_exc:
#                 print("Error processing message:", inner_exc)

#     except websockets.exceptions.ConnectionClosed:
#         print(f"{user_name if 'user_name' in locals() else 'A user'} disconnected.")
#     except Exception as outer_exc:
#         print("Connection error:", outer_exc)
#     finally:
#         if 'user_id' in locals() and user_id in connected_clients:
#             del connected_clients[user_id]

# async def main():
#     async with websockets.serve(handle_connection, "localhost", 8785):
#         print("WebSocket server running at ws://localhost:8785")
#         await asyncio.Future()

# if __name__ == "__main__":
#     asyncio.run(main())
# ---------------------------------------------------------------------------------------------------------------------------------


# import asyncio
# import websockets
# import json
# from datetime import datetime
# from flask import Flask
# from database.database import db
# from main import create_app
# from model.chat import Chat, ChatHistory

# connected_clients = {}         # user_id -> websocket
# offline_messages = {}          # user_id -> list of messages

# app = create_app()
# app.app_context().push()

# async def handle_connection(websocket):
#     try:
#         # Initial user connection handshake
#         data = await websocket.recv()
#         print("Initial connection data:", data)

#         user = json.loads(data)
#         user_id = user.get("id")
#         user_role = user.get("role")
#         user_name = user.get("name")

#         if not user_id or not user_role or not user_name:
#             await websocket.send(json.dumps({"error": "Missing id, role, or name"}))
#             return

#         connected_clients[user_id] = websocket
#         print(f"{user_role} {user_name} connected.")
#         print(f"Connected clients: {list(connected_clients.keys())}")

#         # Send any stored offline messages
#         if user_id in offline_messages:
#             for msg in offline_messages[user_id]:
#                 await websocket.send(json.dumps(msg))
#             del offline_messages[user_id]  # Clear after sending

#         while True:
#             try:
#                 data = await websocket.recv()
#                 print("Received message:", data)

#                 msg_data = json.loads(data)
#                 msg_type = msg_data.get("type")

#                 if not msg_type:
#                     await websocket.send(json.dumps({"error": "Missing message type"}))
#                     continue

#                 if msg_type == "chat":
#                     sender = msg_data.get("sender")
#                     receiver = msg_data.get("to")
#                     message_text = msg_data.get("message")

#                     if not sender or not receiver or not message_text:
#                         await websocket.send(json.dumps({"error": "Incomplete chat message"}))
#                         continue

#                     # Save message to DB
#                     new_chat = Chat(
#                         athlete_id=sender["id"] if sender["role"] == "athlete" else receiver["id"],
#                         coach_id=sender["id"] if sender["role"] == "coach" else receiver["id"],
#                         message=message_text,
#                         timestamp=datetime.utcnow()
#                     )
#                     db.session.add(new_chat)
#                     db.session.commit()

#                     history = ChatHistory(chat_id=new_chat.id)
#                     db.session.add(history)
#                     db.session.commit()

#                     response_payload = {
#                         "type": "chat",
#                         "from": sender,
#                         "message": message_text,
#                         "timestamp": new_chat.timestamp.isoformat()
#                     }

#                     recipient_ws = connected_clients.get(receiver["id"])
#                     if recipient_ws:
#                         await recipient_ws.send(json.dumps(response_payload))
#                     else:
#                         print(f"User {receiver['name']} is offline. Storing message.")
#                         if receiver["id"] not in offline_messages:
#                             offline_messages[receiver["id"]] = []
#                         offline_messages[receiver["id"]].append(response_payload)

#                 elif msg_type == "typing":
#                     recipient_ws = connected_clients.get(msg_data.get("to", {}).get("id"))
#                     if recipient_ws:
#                         await recipient_ws.send(json.dumps({
#                             "type": "typing",
#                             "from": msg_data["sender"]
#                         }))

#             except json.JSONDecodeError:
#                 await websocket.send(json.dumps({"error": "Invalid JSON"}))
#             except Exception as err:
#                 print("Error during message processing:", err)

#     except websockets.exceptions.ConnectionClosed:
#         print(f"{user_name if 'user_name' in locals() else 'A user'} disconnected.")
#     except Exception as outer_exc:
#         print("Connection error:", outer_exc)
#     finally:
#         if 'user_id' in locals() and user_id in connected_clients:
#             del connected_clients[user_id]
#         print(f"Connected clients after disconnection: {list(connected_clients.keys())}")

# async def main():
#     async with websockets.serve(handle_connection, "localhost", 8785):
#         print("WebSocket server running at ws://localhost:8785")
#         await asyncio.Future()  # Keep running

# if __name__ == "__main__":
#     asyncio.run(main())

# ====================================================================================================
import asyncio
import websockets
import json
from datetime import datetime
from flask import Flask
from database.database import db
from main import create_app
from model.chat import Chat, ChatHistory

connected_clients = {}         # user_id -> websocket
offline_messages = {}          # user_id -> list of messages

app = create_app()
app.app_context().push()

async def handle_connection(websocket):
    try:
        # Initial user connection handshake
        data = await websocket.recv()
        print("Initial connection data:", data)

        user = json.loads(data)
        user_id = user.get("id")
        user_role = user.get("role")

        if not user_id or not user_role:
            await websocket.send(json.dumps({"error": "Missing id or role"}))
            return

        user_name = f"{user_role.capitalize()}-{user_id}"
        connected_clients[user_id] = websocket
        print(f"{user_role} {user_name} connected.")
        print(f"Connected clients: {list(connected_clients.keys())}")

        # Send any stored offline messages
        if user_id in offline_messages:
            for msg in offline_messages[user_id]:
                await websocket.send(json.dumps(msg))
            del offline_messages[user_id]  # Clear after sending

        # Message receive loop
        while True:
            try:
                data = await websocket.recv()
                print("Received message:", data)

                msg_data = json.loads(data)
                msg_type = msg_data.get("type")

                if not msg_type:
                    await websocket.send(json.dumps({"error": "Missing message type"}))
                    continue

                # === Handle Chat Message ===
                if msg_type == "chat":
                    sender = msg_data.get("sender")
                    receiver = msg_data.get("to")
                    message_text = msg_data.get("message")

                    if not sender or not receiver or not message_text:
                        await websocket.send(json.dumps({"error": "Incomplete chat message"}))
                        continue

                    # Save message to DB
                    new_chat = Chat(
                        athlete_id=sender["id"] if sender["role"] == "athlete" else receiver["id"],
                        coach_id=sender["id"] if sender["role"] == "coach" else receiver["id"],
                        message=message_text,
                        timestamp=datetime.utcnow()
                    )
                    db.session.add(new_chat)
                    db.session.commit()

                    history = ChatHistory(chat_id=new_chat.id)
                    db.session.add(history)
                    db.session.commit()

                    response_payload = {
                        "type": "chat",
                        "from": sender,
                        "message": message_text,
                        "timestamp": new_chat.timestamp.isoformat()
                    }

                    recipient_ws = connected_clients.get(receiver["id"])
                    if recipient_ws:
                        await recipient_ws.send(json.dumps(response_payload))
                    else:
                        print(f"User {receiver['id']} is offline. Storing message.")
                        offline_messages.setdefault(receiver["id"], []).append(response_payload)

                # === Handle Typing Indicator ===
                elif msg_type == "typing":
                    sender = msg_data.get("sender")
                    receiver = msg_data.get("to")
                    if not sender or not receiver:
                        continue

                    recipient_ws = connected_clients.get(receiver["id"])
                    if recipient_ws:
                        await recipient_ws.send(json.dumps({
                            "type": "typing",
                            "from": sender
                        }))

            except json.JSONDecodeError:
                await websocket.send(json.dumps({"error": "Invalid JSON"}))
            except Exception as err:
                print("Error during message processing:", err)

    except websockets.exceptions.ConnectionClosed:
        print(f"{user_name if 'user_name' in locals() else 'A user'} disconnected.")
    except Exception as outer_exc:
        print("Connection error:", outer_exc)
    finally:
        if 'user_id' in locals() and user_id in connected_clients:
            del connected_clients[user_id]
        print(f"Connected clients after disconnection: {list(connected_clients.keys())}")

async def main():
    async with websockets.serve(handle_connection, "localhost", 8785):
        print("WebSocket server running at ws://localhost:8785")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
