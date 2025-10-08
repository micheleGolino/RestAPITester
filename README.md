# 🧪 REST API Tester

A simple yet powerful **Streamlit** application for testing REST API endpoints with an intuitive user interface.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.35+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🌐 **HTTP Methods**: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
- 🔐 **Authentication**: Bearer Token and Basic Auth
- 📝 **Customizable Body**: Formatted JSON or raw text
- 🔧 **Headers and Query Params**: Interactive editor with dynamic rows
- 📊 **Smart Viewer**: Automatic JSON detection with syntax highlighting
- ⏱️ **Configurable Timeout**: Avoid blocking calls
- 🔒 **SSL Control**: Option to verify/disable SSL certificates
- 💾 **Presets**: Save and reuse recurring configurations
- 📋 **cURL Preview**: Automatically generate equivalent curl command
- ⬇️ **Download Response**: Save response as file
- 🎨 **Wide Mode**: Optimized layout for more space

## 📋 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- (Optional) Docker for containerization

## 🚀 Installation

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd RestAPITester
   ```

2. **Create and activate a virtual environment** (recommended)
   ```bash
   # Windows PowerShell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   
   # Windows CMD
   python -m venv .venv
   .venv\Scripts\activate.bat
   
   # Linux/macOS
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** at the address shown in the terminal (usually `http://localhost:8501`)

### Docker

1. **Build the image**
   ```bash
   docker build -t rest-api-tester:latest .
   ```

2. **Run the container**
   ```bash
   docker run --rm -p 8501:8501 rest-api-tester:latest
   ```

3. **Access the app** at `http://localhost:8501`

### Portainer

1. Push the image to a registry or build locally on the host
2. Create a new stack/service
3. Expose port 8501
4. Start the container

## 📖 Usage

### 1. Basic Configuration

- **HTTP Method**: Select GET, POST, PUT, PATCH, DELETE, HEAD, or OPTIONS
- **URL**: Enter the complete endpoint (e.g., `https://api.example.com/v1/users`)
- **Timeout**: Set timeout in seconds (default: 20s)
- **Verify SSL**: Enable/disable SSL certificate verification

### 2. Query Parameters

In the **Query Params** tab:
- Add dynamic rows with key/value pairs
- Empty rows are automatically ignored
- Parameters are automatically encoded in the URL

### 3. Headers

In the **Headers** tab:
- Define custom HTTP headers
- Default header: `Accept: application/json`
- Add Content-Type, User-Agent, etc.

### 4. Body

In the **Body** tab:
- **none**: No body (for GET, DELETE, etc.)
- **json**: Paste valid JSON; `Content-Type: application/json` will be automatically added
- **raw**: Free text without forcing Content-Type

### 5. Authentication

In the **Auth** tab:
- **None**: No authentication
- **Bearer**: Enter token (adds `Authorization: Bearer <token>` header)
- **Basic**: Username and password (uses requests' Basic Auth)

### 6. Presets

In the **sidebar**:
- Save recurring configurations with a name
- Load previously saved presets
- Presets include all parameters (URL, headers, auth, body, etc.)

### 7. Send and Response

After clicking **Send request**:
- **Status Code** and **Elapsed Time** highlighted
- **Final URL** with expanded parameters
- **Response Headers** in expandable JSON format
- **Body** with smart viewer (formatted JSON or text)
- **Download** response as file
- **cURL preview** to replicate the request from terminal

## 🧪 Quick Tests

Try these endpoints to verify functionality:

### GET with Query Params
```
URL: https://httpbin.org/get
Query Params: hello=world
```

### POST with JSON
```
URL: https://httpbin.org/post
Method: POST
Body: {"test": true, "value": 123}
```

### GET with Bearer Auth (GitHub API)
```
URL: https://api.github.com/user
Method: GET
Auth: Bearer <your-github-token>
```

### SSL Test (httpbin)
```
URL: https://httpbin.org/status/200
Verify SSL: true
```

## 📂 Project Structure

```
RestAPITester/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker container
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── LICENSE               # MIT License
└── README.md            # This documentation
```

## 🔧 Dependencies

- **streamlit** (≥1.35.0): Web interface framework
- **requests** (≥2.32.0): HTTP library for Python
- **pydantic** (≥2.8.0): Data validation and models
- **curlify** (≥2.2.1): Convert requests to curl commands

## 🚀 Future Enhancements

Potential features for future versions:

- [ ] **File upload**: multipart/form-data support
- [ ] **OAuth2**: Complete flows for advanced authentication
- [ ] **Environments**: Selection between dev/stage/prod with base URL
- [ ] **Persistence**: Save presets to local file
- [ ] **History**: Log of last N requests
- [ ] **Import cURL**: Parser to paste curl commands
- [ ] **Schema validation**: Validation with OpenAPI/JSON Schema
- [ ] **Test mode**: Assertions on status/headers/body
- [ ] **Bulk requests**: Batch execution of requests
- [ ] **Export/Import**: Share collections (Postman-style)

## 🐛 Troubleshooting

### SSL Errors
- Disable "Verify SSL" only for test/development endpoints
- In production always keep SSL verification enabled

### 415 Unsupported Media Type
- Verify that the `Content-Type` header is correct
- For JSON use the "json" mode in the body

### 401/403 Unauthorized
- Check that the Bearer token or Basic credentials are correct
- Verify user/token permissions on the endpoint

### Invalid JSON
- Use an external JSON validator to verify syntax
- Check commas, brackets, and quotes

### Timeout
- Increase the timeout value for slow endpoints
- Check network connectivity

## 🔐 Security Notes

⚠️ **Important**:
- Do not share tokens or passwords in plain text
- Avoid disabling SSL verification in production
- Do not expose the app publicly with saved credentials
- Presets are stored in session (not persistent)
- Limit container access if deployed on network

## 📄 License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! For improvements or bugs:
1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 💡 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Check the Help section in the app (expandable at the bottom)

---

**Happy testing! 🚀**
