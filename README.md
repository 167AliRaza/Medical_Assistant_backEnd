
# 🏥 Medical Assistant API

An AI-powered **Medical Assistant** built with **FastAPI**, **OpenAI Agent SDK**, and **Google Sheets** for managing doctor availability.  
This project helps users describe their symptoms, suggests the right specialist doctor, and allows booking appointments if available.

---

## 🚀 Features
- 🤖 Conversational **Medical Assistant** powered by LLMs (Gemini API).
- 🧑‍⚕️ **Doctor Search** by specialty (cardiologist, dermatologist, etc.).
- 📅 **Appointment Booking** integrated with Google Sheets.
- 🔄 Maintains simple **chat history**.
- 🌐 RESTful API endpoints via **FastAPI**.

---

## 📂 Project Structure
```
├── agents/               # Agent definitions & utilities
├── google_sheet.py       # Google Sheets integration
├── main.py               # FastAPI application (entry point)
├── .env                  # Environment variables (API keys)
└── requirements.txt      # Python dependencies
```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/medical-assistant.git
cd medical-assistant
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variables
Create a **.env** file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_SHEET_ID=your_google_sheet_id_here
```

---

## ▶️ Run the Application
Start the FastAPI server:
```bash
uvicorn main:app --reload
```

Access the API:
- Root: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📡 API Endpoints

### **1. Root**
```http
GET /
```
**Response**
```json
{ "message": "Welcome to the Medical Assistant API." }
```

---

### **2. Chat with Assistant**
```http
POST /chat
```
**Request**
```json
{
  "message": "I have chest pain and shortness of breath"
}
```
**Response**
```json
{
  "response": "Based on your symptoms, I recommend consulting a cardiologist. Dr. Smith is available at Heart Care Clinic."
}
```

---

## 🧑‍💻 Tools Used
- **FastAPI** – High-performance Python web framework.
- **OpenAI Agent SDK** – Agent orchestration & LLM-powered reasoning.
- **Google Sheets API** – Manage doctor data & appointment booking.
- **Pydantic** – Data validation.
- **dotenv** – Environment configuration.

---

## 📌 Example Workflow
1. User sends symptoms → `/chat`
2. Agent analyzes symptoms → Suggests appropriate doctor.
3. User confirms → Doctor availability checked in Google Sheets.
4. Appointment booked → Returns confirmation message.

---

## ✅ Future Enhancements
- Add authentication & user session management.
- Improve symptom analysis with structured medical ontologies.
- Store conversation history in MongoDB or PostgreSQL.
- Add multi-language support.

---

## 📝 License
This project is licensed under the MIT License.  
Feel free to use and modify it as needed.
