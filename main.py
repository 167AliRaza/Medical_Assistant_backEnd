import asyncio
from datetime import datetime, timedelta
import uuid
from fastapi import FastAPI, HTTPException
from openai import AsyncOpenAI
from agents import Agent, ModelSettings, Runner, set_tracing_disabled,OpenAIChatCompletionsModel,function_tool
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from pydantic import BaseModel
from google_sheet import data,worksheet
set_tracing_disabled(True)
class Message(BaseModel):
    message: str


app = FastAPI()
load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

@function_tool
def search_doctor(specialty):
    """Search for a doctor by specialty."""

    # doctors = {
    #     "cardiologist": "Dr. Smith, Cardiologist, Heart Care Clinic",
    #     "dermatologist": "Dr. Johnson, Dermatologist, Skin Health Center",
    #     "neurologist": "Dr. Lee, Neurologist, Brain and Nerve Institute",
    #     "pediatrician": "Dr. Brown, Pediatrician, Children's Health Clinic",
    #     "general practitioner": "Dr. Davis, General Practitioner, Family Health Center"
    # }
    doctors_data = data
    filtered_records = [row for row in doctors_data[1:] if row[1].lower() == specialty.lower()]
    return  filtered_records




@function_tool
def book_appointment(doctor_name):
    """Book an appointment with a doctor.
    arguments:
    doctor_name: str : Name of the doctor to book an appointment with.
    check availability and book the appointment.
    returns: str : Confirmation message.
    """
    
    # Assuming 'Name' is in column index 2 and 'IsBooked' is in column index 6
    try:
        doctor_found = False
        for i, row in enumerate(data[1:], start=2):  # Start=2 because we skip header and sheets are 1-indexed
            if row[2].lower() == doctor_name.lower():
                doctor_found = True
                if row[6].upper() == 'FALSE':  # Check if doctor is available (case insensitive)
                    print(f"Booking appointment...")
                    worksheet.update_cell(i, 7, 'TRUE')  # Column 7 (G) for IsBooked (index 6)
                    row[6] = 'TRUE'  # Update the local data representation
                    return {
                        'status': 'success',
                        'message': f"Doctor {doctor_name} booked successfully!",
                        'doctor_info': row
                    }
                else:  # Doctor found but already booked
                    return {
                        'status': 'error',
                        'message': f"Doctor {doctor_name} is already booked."
                    }
        
        # If we reach here, doctor was not found
        if not doctor_found:
            return {
                'status': 'error',
                'message': f"Doctor {doctor_name} not found."
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f"Error: {str(e)}"
        }


agent = Agent(
    name="Medical Assistant",
    instructions="You are an expert Medical Assistant.help the user to identify possible medical conditions based on their symptoms and sugest appropriate professional Doctor by using the search_doctor function tool. If you are unsure, ask for more information.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[search_doctor, book_appointment],
    # model_settings=ModelSettings(tool_choice="required")

)


history = []


# session_histories: Dict[str, List[Dict[str, str]]] = {}

# def get_session_id() -> str:
#     """Generate a simple session ID - in production, use proper session management"""
#     import uuid
#     return str(uuid.uuid4())

# @app.post("/chat")
# def chat(message: Message, session_id: str = None):
#     """Handle chat messages with the medical assistant"""
#     if not message.message or not message.message.strip():
#         raise HTTPException(status_code=400, detail="Message cannot be empty")
    
#     # Use session-based history or create new session
#     if not session_id:
#         session_id = get_session_id()
    
#     if session_id not in session_histories:
#         session_histories[session_id] = []
    
#     history = session_histories[session_id]
#     query = message.message.strip()
    
#     # Add user message to history
#     history.append({"role": "user", "content": query})
    
#     try:
#         # Run the agent asynchronously
#         result = Runner.run_sync(
#             agent,
#             history,
#         )
        
#         # Add assistant response to history
#         history.append({"role": "assistant", "content": result.final_output})
        
#         # Keep history manageable (last 20 messages)
#         if len(history) > 20:
#             history = history[-20:]
#             session_histories[session_id] = history

#         return {"response": result.final_output}

#     except Exception as e:
#         print(f"Error in chat endpoint: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Welcome to the Medical Assistant API."}


@app.post("/chat")
async def agent_endpoint(message: Message, ):
    query = message.message.strip()
    if not query:
        return {"error": "Query is required"}

    history.append({"role": "user", "content": query})
   
    try:
        result = await Runner.run(agent, history)
        history.append({"role": "assistant", "content": result.final_output})
        return {"response": result.final_output}
    except Exception as e:
        return {"error": str(e)}
