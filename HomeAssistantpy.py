import asyncio
import websockets
import uuid
import mysecrets
import json
class HomeAssistant:

    messageid = 1
    responses = {}
    websocket = None
    conversation_id = ""
    pipeline = None
    new_coversation_every_x_seconds_of_inactivty = -1
    async def connect(self):
        uri = f"ws://{mysecrets.home_assistant_url}/api/websocket"
        self.websocket = await websockets.connect(uri)
        asyncio.create_task(self.listen_for_messages())
        asyncio.create_task(self.generate_conversation_id())
    def setPipeline(self,pipeline):
        self.pipeline = pipeline
    async def getPipelineOptions(self):
        
        j = {
            "id": self.messageid,
            "type": "assist_pipeline/pipeline/list",
        }
        print(f"Sending: {j}")
        self.messageid += 1
        await self.websocket.send(json.dumps(j))

    async def generate_conversation_id(self):
        while self.new_coversation_every_x_seconds_of_inactivty > -1:
            self.conversation_id = str(uuid.uuid4())
            await asyncio.sleep(self.new_coversation_every_x_seconds_of_inactivty)
    async def cleanup(self):
        await self.websocket.close()
        self.messageid = 1
        self.responses.clear()
        await self.reconnect()


    def __init__(self,secondstoresetconvo=-1, on_response_callback = None):
        self.new_coversation_every_x_seconds_of_inactivty = secondstoresetconvo
        self.on_response_callback = on_response_callback
    async def CreateResponse(self, message, discord_message):
        await self.initAssistPipeline(message, discord_message)
    async def initAssistPipeline(self, message,discord_message):

        j = {
            "id": self.messageid,
            "type": "assist_pipeline/run",
            "start_stage": "intent",
            "end_stage": "intent",
            "conversation_id": self.conversation_id,
            "input": {
                "text": message
            }
        }
        if self.pipeline != None:
            j["pipeline"] = self.pipeline
        print(f"Sending: {j}")
        self.responses[self.messageid] = discord_message

    
        await self.websocket.send(json.dumps(j))
        self.messageid += 1
    async def reconnect(self):
        try:
            print("Reconnecting to Home Assistant...")
            await self.connect()
        except Exception as e:
            print(f"Failed to reconnect: {e}")
            await asyncio.sleep(5)  # Wait before trying again
    async def listen_for_messages(self):
        try:
            while True:
                try:
                    message = await self.websocket.recv()
                    await self.HandleWebSocketMessage(message)
                except websockets.exceptions.ConnectionClosed:
                    # Connection is closed, try to reconnect
                    await self.reconnect()
                    break
        except Exception as e:
            print(f"Error in websocket listener: {e}")
            await self.reconnect()
    async def auth(self):
        j = {
                "type": "auth",
                "access_token": mysecrets.home_assistant_token  # Use the proper token variable
            }
        await self.websocket.send(json.dumps(j))

    async def HandleWebSocketMessage(self,bits):
        print(f"Received: {bits}")
        y = json.loads(bits)
        if y["type"] == "auth_required":
            print("Authenticating...")
            await self.auth()
        elif y["type"] == "event":
            if y["event"]["type"] == "intent-end":
               message =  y["event"]["data"]["intent_output"]["response"]["speech"]["plain"]["speech"]
               message_id = y["id"]  # The message_id can be used to match the response
               discord_message = self.responses.get(message_id)
               if discord_message:
                await self.on_response_callback(discord_message, message)
    
                # Convert to JSON string
          
            

