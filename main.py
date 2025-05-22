import os
import json
import base64
import asyncio
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.websockets import WebSocketDisconnect
from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream
from dotenv import load_dotenv
load_dotenv()
# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') # requires OpenAI Realtime API Access
PORT = int(os.getenv('PORT', 5050))

SYSTEM_MESSAGE = (
    "You are a helpful and bubbly AI assistant who loves to chat about "
    "the order that the patient has ordered. Start with asking dob and name to verify and then proceed."
    "Don't say lots of words. Keep it simple."
)

extra_context = {
    "patient_id": 2492302,
    "name": "Rahul Garg",
    "dob": "26/05/1999",
    "summary": [
        {
            "drug": {
                "med_name_id": 405739,
                "med_name": "Miebo (PF)",
                "ndc": "24208037705",
                "label_name": "MIEBO 100% EYE DROP",
                "indication": "indicated for the treatment of the signs and symptoms of dry eye disease (DED)",
                "pronunciation": "My-boh",
                "ndc_type": None
            },
            "order_id": 992063,
            "prescription_id": 1051645,
            "fill_id": 1004417,
            "dispense_days_supply": "30.0000",
            "prescriber_name": "AMANDA EILEEN MCGIVERON ",
            "prescriber_npi": 1295137941,
            "pricing_info": [
                {
                    "offer_id": 7703279,
                    "financial_assistance": None,
                    "coupon_amount": None,
                    "total_price": None,
                    "offer_type": "cash",
                    "status": "unavailable",
                    "pharmacy_type": "consignment",
                    "program": "blink_cash_price",
                    "claim_set_id": None,
                    "drug_info": {
                        "med_name_id": 405739,
                        "med_name": "Miebo (PF)",
                        "ndc": "24208037705",
                        "label_name": "MIEBO 100% EYE DROP",
                        "indication": "indicated for the treatment of the signs and symptoms of dry eye disease (DED)",
                        "pronunciation": "My-boh",
                        "ndc_type": None
                    }
                },
                {
                    "offer_id": 7703280,
                    "financial_assistance": None,
                    "coupon_amount": None,
                    "total_price": None,
                    "offer_type": "cash",
                    "status": "unavailable",
                    "pharmacy_type": "consignment",
                    "program": "blink_cash_price",
                    "claim_set_id": None,
                    "drug_info": {
                        "med_name_id": 405739,
                        "med_name": "Miebo (PF)",
                        "ndc": "24208037705",
                        "label_name": "MIEBO 100% EYE DROP",
                        "indication": "indicated for the treatment of the signs and symptoms of dry eye disease (DED)",
                        "pronunciation": "My-boh",
                        "ndc_type": None
                    }
                },
                {
                    "offer_id": 7703281,
                    "financial_assistance": None,
                    "coupon_amount": 0,
                    "total_price": 20000,
                    "offer_type": "insurance",
                    "status": "verified",
                    "pharmacy_type": None,
                    "program": None,
                    "claim_set_id": 809744,
                    "drug_info": {
                        "med_name_id": 405739,
                        "med_name": "Miebo (PF)",
                        "ndc": "24208037705",
                        "label_name": "MIEBO 100% EYE DROP",
                        "indication": "indicated for the treatment of the signs and symptoms of dry eye disease (DED)",
                        "pronunciation": "My-boh",
                        "ndc_type": None
                    }
                }
            ],
            "shipping_info": {
                "shipping_status": None,
                "shipping_method": "Delivery",
                "shipping_date": None,
                "shipping_address": None,
                "expected_date": None,
                "tracking_number": None,
                "carrier": None,
                "delivered": None,
                "delivery_date": None
            },
            "refill_data": {
                "refills_remaining": 1,
                "refill_number": 0,
                "auto_refill": False,
                "next_refill_date": None,
                "last_refill_date": None,
                "last_refill_cost": None
            },
            "has_filled_in_past": False,
            "purchase_status": False,
            "purchase_date": None,
            "program": "Bausch and Lomb",
            "program_url": "https://docs.google.com/document/d/1PtAYWEYpZUiFyIszyXkySVD8-l2FJd113cssU8Hn67s",
            "status": "onboarding",
            "color_status": "green",
            "script": "Your Prescription Miebo (PF) is ready to be purchased and delivered. For a 30 days supply, your price will be $200.0(insurance). You can check out over the phone now, or we can send a text message containing a secure checkout link to your mobile phone 6468547727..",
            "pharmacy_npi": 1003906942,
            "pharmacy_name": "White Drug",
            "order_status": "ready_to_purchase",
            "followup_reasons": [
                "patient_voice_broadcasting_in_progress"
            ],
            "published_price_info": {
                "offer_id": 7703281,
                "financial_assistance": None,
                "coupon_amount": 0,
                "total_price": 20000,
                "offer_type": "insurance",
                "status": "verified",
                "pharmacy_type": None,
                "program": None,
                "claim_set_id": 809744,
                "drug_info": {
                    "med_name_id": 405739,
                    "med_name": "Miebo (PF)",
                    "ndc": "24208037705",
                    "label_name": "MIEBO 100% EYE DROP",
                    "indication": "indicated for the treatment of the signs and symptoms of dry eye disease (DED)",
                    "pronunciation": "My-boh",
                    "ndc_type": None
                }
            },
            "blink_cash_price_info": {
                "offer_id": 7703279,
                "financial_assistance": None,
                "coupon_amount": None,
                "total_price": None,
                "offer_type": "cash",
                "status": "unavailable",
                "pharmacy_type": "consignment",
                "program": "blink_cash_price",
                "claim_set_id": None,
                "drug_info": {
                    "med_name_id": 405739,
                    "med_name": "Miebo (PF)",
                    "ndc": "24208037705",
                    "label_name": "MIEBO 100% EYE DROP",
                    "indication": "indicated for the treatment of the signs and symptoms of dry eye disease (DED)",
                    "pronunciation": "My-boh",
                    "ndc_type": None
                }
            },
            "on_hold": True,
            "on_hold_reason": "Patient prefers other pharmacy",
            "cell_phone": "6468547727",
            "prior_auth_status": None,
            "eligible_for_one_touch_refill": False,
            "order_eligible_for_one_touch_refill": False,
            "prior_auth": None,
            "use_case_status": "ready_to_purchase",
            "prescription_expiry_date": "2026-05-21"
        }
    ]
}

VOICE = 'alloy'
LOG_EVENT_TYPES = [
    'response.content.done', 'rate_limits.updated', 'response.done',
    'input_audio_buffer.committed', 'input_audio_buffer.speech_stopped',
    'input_audio_buffer.speech_started', 'session.created'
]
app = FastAPI()
if not OPENAI_API_KEY:
    raise ValueError('Missing the OpenAI API key. Please set it in the .env file.')

@app.get("/", response_class=JSONResponse)
async def index_page():
    return {"message": "Twilio Media Stream Server is running!"}
@app.api_route("/incoming-call", methods=["GET", "POST"])
async def handle_incoming_call(request: Request):
    """Handle incoming call and return TwiML response to connect to Media Stream."""
    response = VoiceResponse()
    # <Say> punctuation to improve text-to-speech flow
    response.say("Please wait while we connect your call to the A. I. voice assistant")
    response.pause(length=1)
    response.say("O.K. you can start talking!")
    host = request.url.hostname
    connect = Connect()
    connect.stream(url=f'wss://{host}/media-stream')
    response.append(connect)
    return HTMLResponse(content=str(response), media_type="application/xml")

import aiohttp

@app.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):
    """Handle WebSocket connections between Twilio and OpenAI using aiohttp."""
    print("Client connected")
    await websocket.accept()

    OPENAI_API_URL = 'wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01'
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Beta": "realtime=v1"
    }

    stream_sid = None

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(OPENAI_API_URL, headers=headers) as openai_ws:

            await send_session_update_aiohttp(openai_ws)

            async def receive_from_twilio():
                nonlocal stream_sid
                try:
                    while True:
                        message = await websocket.receive_text()
                        data = json.loads(message)

                        if data['event'] == 'media' and not openai_ws.closed:
                            audio_append = {
                                "type": "input_audio_buffer.append",
                                "audio": data['media']['payload']
                            }
                            await openai_ws.send_str(json.dumps(audio_append))

                        elif data['event'] == 'start':
                            stream_sid = data['start']['streamSid']
                            print(f"Incoming stream started: {stream_sid}")

                except WebSocketDisconnect:
                    print("Client disconnected.")
                    if not openai_ws.closed:
                        await openai_ws.close()

            async def send_to_twilio():
                nonlocal stream_sid
                try:
                    async for msg in openai_ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            response = json.loads(msg.data)

                            if response['type'] in LOG_EVENT_TYPES:
                                print(f"Received event: {response['type']}", response)

                            if response['type'] == 'session.updated':
                                print("Session updated successfully:", response)

                            if response['type'] == 'response.audio.delta' and response.get('delta'):
                                try:
                                    audio_payload = base64.b64encode(base64.b64decode(response['delta'])).decode('utf-8')
                                    audio_delta = {
                                        "event": "media",
                                        "streamSid": stream_sid,
                                        "media": {
                                            "payload": audio_payload
                                        }
                                    }
                                    await websocket.send_json(audio_delta)
                                except Exception as e:
                                    print(f"Error processing audio data: {e}")

                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            print(f"OpenAI WebSocket error: {openai_ws.exception()}")
                            break

                except Exception as e:
                    print(f"Error in send_to_twilio: {e}")

            await asyncio.gather(receive_from_twilio(), send_to_twilio())

async def send_session_update_aiohttp(openai_ws):
    session_update = {
        "type": "session.update",
        "session": {
            "turn_detection": {"type": "server_vad"},
            "input_audio_format": "g711_ulaw",
            "output_audio_format": "g711_ulaw",
            "voice": VOICE,
            "instructions": SYSTEM_MESSAGE + str(extra_context),
            "modalities": ["text", "audio"],
            "temperature": 0.8,
        }
    }
    print('Sending session update:', json.dumps(session_update))
    await openai_ws.send_str(json.dumps(session_update))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)