# 📊 Trade Opportunities API

> **AI-Powered Market Sector Analysis for Indian Markets**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-green.svg)](https://fastapi.tiangolo.com/)
[![Gemini AI](https://img.shields.io/badge/Gemini-2.5--flash-orange.svg)](https://ai.google.dev/)
[![Status](https://img.shields.io/badge/Status-✅_Operational-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-ready REST API that provides comprehensive market analysis reports for Indian business sectors using **Google Gemini AI** and real-time web data. Built with FastAPI, featuring authentication, rate limiting, and professional markdown report generation.

---

## 🎯 Quick Demo

**Live API Documentation:** `http://localhost:8000/docs` (after running locally)

**Test Credentials:**
```
API Key: my_secure_api_key_12345
```

**Try it in 30 seconds:**
1. Open API docs at http://localhost:8000/docs
2. Click 🔓 "Authorize" button (top right)
3. Enter API key: `my_secure_api_key_12345`
4. Click "Authorize" → "Close"
5. Find **GET /api/v1/analyze/{sector}**
6. Click "Try it out"
7. Enter sector: `agriculture` or `technology` or `pharmaceuticals`
8. Click "Execute" and wait 30-45 seconds
9. Get 2000+ word AI-analyzed report! 📄

---

## ✨ Features

### 🤖 AI-Powered Analysis
- **Google Gemini 2.5 Flash** integration for intelligent market analysis
- Sophisticated prompt engineering for structured outputs
- Generates comprehensive 2000+ word reports in 30-45 seconds

### 📊 Comprehensive Reports
- Executive summary with market overview
- Key trends and market drivers
- Trade opportunities with risk assessment
- Investment outlook (short/medium/long term)
- Strategic recommendations
- Professional markdown formatting with emojis

### 🔒 Production-Ready Security
- API key authentication
- Rate limiting (10 requests per hour, configurable)
- Input validation and sanitization
- Session management
- CORS configuration

### 📈 Real-Time Data
- Aggregates latest market news from DuckDuckGo
- Analyzes current trends and developments
- Sources cited in every report

### 🚀 High Performance
- Async/await operations (non-blocking)
- Handles concurrent requests
- Auto-generated OpenAPI documentation
- Comprehensive error handling
- **Fast**: Built with FastAPI for high performance
- **Free Tier**: All integrations use free-tier services

## Tech Stack 🛠️

- **Backend**: FastAPI
- **AI**: Google Gemini API (Free tier)
- **Data**: DuckDuckGo Search API (Free)
- **Storage**: In-memory (No database required)
- **Authentication**: API Key-based
- **Rate Limiting**: Custom middleware

## Quick Start 🏃‍♂️

### 1. Clone and Setup

```bash
cd fastapi
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Get your Gemini API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_actual_gemini_api_key

# Generate a random API key for authentication
API_KEY=your_secure_api_key_here

# Rate limiting (10 requests per hour)
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_PERIOD=3600
```

### 5. Run the Server

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

## API Documentation 📚

### Interactive API Docs

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoint

#### Analyze Sector

```
GET /api/v1/analyze/{sector}
```

**Headers:**
```
X-API-Key: your_api_key_here
```

**Parameters:**
- `sector` (path): Sector name (e.g., pharmaceuticals, technology, agriculture)

**Example Request:**

```bash
curl -X GET "http://localhost:8000/api/v1/analyze/pharmaceuticals" \
  -H "X-API-Key: your_api_key_here"
```

**Example Response:**

```json
{
  "status": "success",
  "sector": "pharmaceuticals",
  "timestamp": "2026-01-15T10:30:00Z",
  "report": "# Market Analysis Report: Pharmaceuticals\n\n## Executive Summary\n...",
  "session_id": "abc123...",
  "requests_remaining": 9
}
```

### Other Endpoints

#### Health Check
```
GET /health
```

#### Get Session Info
```
GET /api/v1/session
Headers: X-API-Key: your_api_key_here
```

## How to Get Gemini API Key 🔑

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your `.env` file

**Note**: The free tier includes:
- 60 requests per minute
- 1,500 requests per day
- Plenty for development and testing!

## Usage Examples 💡

### Python Example

```python
import requests

API_KEY = "your_api_key_here"
BASE_URL = "http://localhost:8000"

headers = {"X-API-Key": API_KEY}

# Analyze a sector
response = requests.get(
    f"{BASE_URL}/api/v1/analyze/technology",
    headers=headers
)

data = response.json()
print(data['report'])

# Save to file
with open('technology_report.md', 'w', encoding='utf-8') as f:
    f.write(data['report'])
```

### JavaScript Example

```javascript
const API_KEY = 'your_api_key_here';
const BASE_URL = 'http://localhost:8000';

async function analyzeSector(sector) {
  const response = await fetch(
    `${BASE_URL}/api/v1/analyze/${sector}`,
    {
      headers: {
        'X-API-Key': API_KEY
      }
    }
  );
  
  const data = await response.json();
  return data;
}

analyzeSector('agriculture').then(data => {
  console.log(data.report);
});
```

## Available Sectors 🏢

The API supports analysis for any sector. Common examples:

- **Pharmaceuticals**: Drug manufacturing, healthcare
- **Technology**: IT services, software, hardware
- **Agriculture**: Farming, agritech, food processing
- **Automotive**: Vehicle manufacturing, EV sector
- **Banking**: Financial services, fintech
- **Textiles**: Garments, fabrics
- **Renewable Energy**: Solar, wind, green tech
- **E-commerce**: Online retail, logistics
- **Real Estate**: Construction, infrastructure
- **Telecommunications**: Telecom services, 5G

## Security Features 🔒

1. **API Key Authentication**: All requests require valid API key
2. **Rate Limiting**: 10 requests per hour per API key (configurable)
3. **Input Validation**: Sanitizes sector names and validates input
4. **Session Tracking**: Monitors usage per session
5. **Error Handling**: Graceful degradation on failures

## Rate Limiting ⏱️

- **Default**: 10 requests per hour
- **Configurable**: Edit `RATE_LIMIT_REQUESTS` and `RATE_LIMIT_PERIOD` in `.env`
- **Reset**: Automatically resets after the time period

## Error Handling 🚨

The API returns structured error responses:

```json
{
  "detail": "Rate limit exceeded. Try again in 3540 seconds.",
  "status": "error"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid sector name)
- `401`: Unauthorized (missing/invalid API key)
- `429`: Too Many Requests (rate limit exceeded)
- `500`: Internal Server Error

## Project Structure 📁

```
fastapi/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── auth/
│   ├── __init__.py
│   └── middleware.py      # Authentication middleware
├── services/
│   ├── __init__.py
│   ├── search_service.py  # Web search integration
│   ├── ai_service.py      # Gemini AI integration
│   └── analysis_service.py # Market analysis logic
├── utils/
│   ├── __init__.py
│   ├── rate_limiter.py    # Rate limiting logic
│   └── validators.py      # Input validation
├── models/
│   ├── __init__.py
│   └── schemas.py         # Pydantic models
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Development 👨‍💻

### Running Tests

```bash
# Install test dependencies
pip install pytest httpx

# Run tests (if implemented)
pytest
```

### Debug Mode

Set `DEBUG=True` in `.env` for detailed logging:

```env
DEBUG=True
```

## Troubleshooting 🔧

### Issue: "Invalid API Key"

**Solution**: Ensure your Gemini API key is correctly set in `.env`

### Issue: "Rate limit exceeded"

**Solution**: Wait for the rate limit to reset or increase limits in `.env`

### Issue: "No search results found"

**Solution**: Try a different sector name or check internet connection

### Issue: "Module not found"

**Solution**: Ensure virtual environment is activated and dependencies installed:
```bash
pip install -r requirements.txt
```

## Production Deployment 🚀

### Using Docker (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production

- Set `DEBUG=False`
- Use strong `SECRET_KEY` and `API_KEY`
- Configure appropriate rate limits
- Use HTTPS in production
- Set up proper logging

## API Response Format 📋

### Success Response

```json
{
  "status": "success",
  "sector": "pharmaceuticals",
  "timestamp": "2026-01-15T10:30:00Z",
  "report": "# Market Analysis Report...",
  "session_id": "unique_session_id",
  "requests_remaining": 9,
  "metadata": {
    "sources_found": 5,
    "analysis_time": 3.2
  }
}
```

### Error Response

```json
{
  "status": "error",
  "detail": "Error message here",
  "sector": "invalid_sector",
  "timestamp": "2026-01-15T10:30:00Z"
}
```

## Contributing 🤝

This is a take-home assignment project. Feel free to extend and improve:

1. Add database support (PostgreSQL, MongoDB)
2. Implement JWT authentication
3. Add caching layer (Redis)
4. Create frontend dashboard
5. Add more AI models
6. Implement webhook notifications

---

## 📝 License

This project is licensed under the **MIT License** - free to use, modify, and distribute.

---

## 👤 Author & Contact

**Developer:** [Your Name]
- 📧 Email: your.email@example.com
- 💼 LinkedIn: [linkedin.com/in/your-profile](https://linkedin.com/in/your-profile)
- 🐙 GitHub: [@your-username](https://github.com/your-username)
- 🌐 Portfolio: [your-portfolio.com](https://your-portfolio.com)

---

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework
- **Google Gemini** - Powerful AI language model  
- **DuckDuckGo** - Privacy-focused search
- **Pydantic** - Data validation made easy

---

## 💼 For Recruiters

### Project Highlights
✅ **Production-ready** REST API with comprehensive error handling  
✅ **AI Integration** with Google Gemini 2.5 Flash  
✅ **Security** features: Authentication, rate limiting, input validation  
✅ **Async operations** for optimal performance  
✅ **Clean architecture** with separation of concerns  
✅ **Full documentation** including OpenAPI/Swagger  
✅ **Deployment ready** with Docker and cloud platform support  

### Technical Skills Demonstrated
- Backend API development (FastAPI)
- AI/ML integration
- Authentication & authorization
- Rate limiting & security
- Async/await programming
- Data validation (Pydantic)
- Error handling & logging
- API documentation
- Git version control

### Quick Demo for Interview
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Add environment variables
4. Run: `uvicorn main:app --reload`
5. Open: http://localhost:8000/docs
6. Test with provided API key

**Estimated setup time:** 5 minutes

See [RECRUITER_SUMMARY.md](RECRUITER_SUMMARY.md) for detailed project overview.

---

## �‍💻 About the Developer

**Nazeef Ahmed**
- 📧 **Email:** nazeefahmed17@gmail.com
- 💼 **LinkedIn:** [Nazeef Ahmed](https://www.linkedin.com/public-profile/settings?trk=d_flagship3_profile_self_view_public_profile)
- 🐙 **GitHub:** [Nazeefahmed2023](https://github.com/Nazeefahmed2023)
- 🌐 **Portfolio:** [profile34.vercel.app](https://profile34.vercel.app/)

---

## 📞 Support & Questions

### Need Help?
- 📖 **Documentation:** Check `/docs` folder for guides
- 🔧 **API Docs:** http://localhost:8000/docs
- 🐛 **Issues:** Report on GitHub
- 📧 **Email:** nazeefahmed17@gmail.com

### Want to Connect?
I'm happy to discuss this project or collaborate!  
📧 nazeefahmed17@gmail.com  
💼 [LinkedIn Profile](https://www.linkedin.com/public-profile/settings?trk=d_flagship3_profile_self_view_public_profile)

---

## ⭐ Star This Project!

If you find this useful, please give it a ⭐ on GitHub!

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/Nazeefahmed2023/trade-opportunities-api)
![GitHub forks](https://img.shields.io/github/forks/Nazeefahmed2023/trade-opportunities-api)
![GitHub issues](https://img.shields.io/github/issues/Nazeefahmed2023/trade-opportunities-api)
![GitHub license](https://img.shields.io/github/license/Nazeefahmed2023/trade-opportunities-api)

---

**Built with ❤️ using FastAPI and Google Gemini AI**

**Status:** ✅ Production Ready | 🚀 Actively Maintained | 📈 Open for Contributions

---

*Last Updated: January 15, 2026 | Version 1.0.0*
