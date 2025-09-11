# Gemini Nano FastAPI - AI Image Editor

A production-ready FastAPI application that uses Google's Gemini AI to edit images based on text prompts. This API provides a simple and powerful way to modify images using natural language descriptions.

## 🚀 Features

- **AI-Powered Image Editing**: Uses Google's Gemini 2.5 Flash Image Preview model for intelligent image modifications
- **Multiple Endpoints**: Flexible API design with multiple endpoints for different use cases
- **Production Ready**: Comprehensive error handling, logging, and CORS support
- **Binary Response**: Efficiently streams edited images as binary data
- **Health Monitoring**: Built-in health check endpoint for monitoring
- **Debug Support**: Debug endpoints for troubleshooting

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API Key
- pip (Python package installer)

## 🛠 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/hariom-hp/gemini-nano-fast-api.git
   cd gemini-nano-fast-api
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   ```
   
   **Note**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🚦 Usage

### Starting the Server

```bash
# Development mode with auto-reload
uvicorn main:app --reload

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Interactive Docs (Swagger)**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📡 API Endpoints

### 1. Health Check
```http
GET /health
```
Returns the API health status.

### 2. Image Editing (Primary)
```http
POST /design/generate
```
**Parameters:**
- `image`: Image file (multipart/form-data)
- `description`: Text prompt describing the desired edit

**Response:** Binary image data (PNG format)

### 3. Alternative Image Editing
```http
POST /edit-image
```
**Parameters:**
- `file`: Image file (multipart/form-data)
- `prompt`: Text prompt describing the desired edit

**Response:** Binary image data (PNG format)

### 4. Debug Endpoint
```http
POST /debug
```
Logs request details for debugging purposes.

### 5. Test JSON Response
```http
POST /test-json
```
Returns a JSON response for testing client implementations.

## 🧪 Example Usage

### cURL Example
```bash
curl -X POST "http://localhost:8000/design/generate" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@your-image.jpg" \
  -F "description=make it look modern and futuristic" \
  --output edited-image.png
```

### Python Example
```python
import requests

url = "http://localhost:8000/design/generate"
files = {"image": open("input-image.jpg", "rb")}
data = {"description": "turn this into a modern minimalist design"}

response = requests.post(url, files=files, data=data)

if response.status_code == 200:
    with open("output-image.png", "wb") as f:
        f.write(response.content)
    print("Image edited successfully!")
```

### Flutter/Dart Example
```dart
import 'package:dio/dio.dart';

final dio = Dio();
final formData = FormData.fromMap({
  'image': await MultipartFile.fromFile('path/to/image.jpg'),
  'description': 'make it colorful and vibrant',
});

final response = await dio.post(
  'http://localhost:8000/design/generate',
  data: formData,
  options: Options(responseType: ResponseType.bytes),
);

// Save the binary response as an image
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Google Gemini API key | Yes |

### Supported Image Formats

- JPEG/JPG
- PNG
- GIF
- BMP
- TIFF
- WebP

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

1. **Environment Variables**: Use secure environment variable management
2. **Rate Limiting**: Implement rate limiting for production use
3. **Authentication**: Add authentication for secure access
4. **Load Balancing**: Use load balancers for high availability
5. **Monitoring**: Implement logging and monitoring solutions

## 🛡 Security

- ✅ API keys are stored securely in environment variables
- ✅ CORS is configured for cross-origin requests
- ✅ Input validation and error handling
- ✅ No sensitive data in logs or responses

## 🔍 Troubleshooting

### Common Issues

1. **"Missing API key" error**
   - Ensure `.env` file exists with valid `GOOGLE_API_KEY`
   - Check that the API key has proper permissions

2. **"AI did not return image data" error**
   - Try different prompts
   - Check if the Gemini model is available
   - Verify your API quota

3. **Connection errors**
   - Check internet connectivity
   - Verify firewall settings
   - Ensure the server is running

### Debug Mode

Enable debug logging by modifying the logging level in `main.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📁 Project Structure

```
gemini-nano-fast-api/
├── main.py              # FastAPI application and endpoints
├── services.py          # Gemini AI integration logic
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (not in repo)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google AI for the Gemini API
- FastAPI for the excellent web framework
- The Python community for amazing libraries

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/hariom-hp/gemini-nano-fast-api/issues) page
2. Create a new issue with detailed information
3. Include error logs and system information

---

**Made with ❤️ using Google Gemini AI and FastAPI**
