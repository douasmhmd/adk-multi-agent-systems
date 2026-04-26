# file: live_agent/backend/backend.py
import asyncio
import base64
import json
import os
import sys
from typing import Any, Dict

import websockets
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.adk.agents.run_config import RunConfig
from google.adk.agents.live_request_queue import LiveRequestQueue
from google.genai import types

# Allow imports from agent_math (which lives in basic_agent/)
sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "..", "basic_agent"),
)
from agent_math.agent import create_math_agent

load_dotenv()

MODEL = "gemini-2.5-flash-native-audio-preview-12-2025"
# Create the agent ONCE at startup
root_agent, context = create_math_agent(model=MODEL)


async def start_agent_session(
    root_agent,
    session_id: str,
    app_name: str = "agent_math",
    user_id: str = "user",
    context: Dict[str, Any] = {},
):
    response_modalities = ["AUDIO"]
    voice = "Aoede"
    language_code = "en-US"

    print(
        f"Live Agent Config: [Model: {MODEL}, Voice: {voice}, "
        f"Modalities: {response_modalities}, Language: {language_code}, "
        f"Session: {session_id}]"
    )

    run_config = RunConfig(
        response_modalities=response_modalities,
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfigDict(
                {"prebuilt_voice_config": {"voice_name": voice}}
            ),
            language_code=language_code,
        ),
    )

    runner = InMemoryRunner(app_name=app_name, agent=root_agent)
    session_obj = await runner.session_service.create_session(
        app_name=app_name, user_id=user_id, state=context
    )

    live_request_queue = LiveRequestQueue()
    live_events = runner.run_live(
        session=session_obj,
        live_request_queue=live_request_queue,
        run_config=run_config,
    )

    print(f"Session {session_id} created successfully.")
    return live_events, live_request_queue


async def handle_frontend_messages(client_ws, live_request_queue):
    print("-> Starting frontend-to-agent forwarder.")
    try:
        async for message in client_ws:
            try:
                data = json.loads(message)
                if (
                    "realtimeInput" in data
                    and "mediaChunks" in data["realtimeInput"]
                ):
                    for chunk in data["realtimeInput"]["mediaChunks"]:
                        if chunk.get("mime_type") == "audio/pcm":
                            audio_bytes = base64.b64decode(chunk["data"])
                            audio_blob = types.Blob(
                                data=audio_bytes,
                                mime_type="audio/pcm;rate=16000",
                            )
                            live_request_queue.send_realtime(audio_blob)
            except Exception as e:
                print(f"Error in frontend forwarder: {e}")
    except websockets.exceptions.ConnectionClosed:
        print("-> Frontend WebSocket closed.")


async def handle_agent_responses(client_ws, live_events):
    print("<- Starting agent-to-frontend forwarder.")
    try:
        async for event in live_events:
            if event.interrupted:
                await client_ws.send(
                    json.dumps(
                        {
                            "type": "interrupted",
                            "data": {"message": "Response interrupted"},
                        }
                    )
                )
                continue

            if event.content is None:
                if event.turn_complete:
                    await client_ws.send(
                        json.dumps(
                            {"type": "backend", "data": "turn_complete"}
                        )
                    )
                continue

            inline_data = (
                event.content
                and event.content.parts
                and event.content.parts[0].inline_data
            )

            if inline_data and inline_data.mime_type.startswith("audio/pcm"):
                audio_b64 = base64.b64encode(inline_data.data).decode("utf-8")
                await client_ws.send(
                    json.dumps({"type": "audio", "data": audio_b64})
                )
                continue

            await asyncio.sleep(0)
    except websockets.exceptions.ConnectionClosed:
        print("<- Client closed.")


async def handle_connections(client_ws):
    session_id = id(client_ws)
    print(f"Client connected: {session_id}")

    live_events, live_request_queue = await start_agent_session(
        root_agent=root_agent, session_id=str(session_id), context=context
    )

    try:
        await asyncio.gather(
            handle_frontend_messages(client_ws, live_request_queue),
            handle_agent_responses(client_ws, live_events),
        )
    finally:
        print(f"Client disconnected: {session_id}")


async def main():
    port = int(os.environ.get("PORT", 8081))
    host = "0.0.0.0"
    async with websockets.serve(handle_connections, host, port):
        print(f"ADK Live Agent backend running on ws://{host}:{port}")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())