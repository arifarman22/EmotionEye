# EmotionEye 👁️

An AI-powered emotional analysis application that analyzes text emotions and provides relevant Quranic guidance.

## Features

- 🎯 Real-time emotion detection from text
- 📖 Quranic verses and translations based on detected emotions
- 📊 Emotion trend analysis and visualization
- 🌐 Modern web interface with responsive design
- 🔄 Multi-language support (Arabic, English, Bengali)

## Quick Start

### Option 1: Docker Deployment (Recommended)

1. **Prerequisites**
   - Install [Docker](https://www.docker.com/get-started)
   - Install [Docker Compose](https://docs.docker.com/compose/install/)

2. **Deploy**
   ```bash
   # On Linux/Mac
   chmod +x deploy.sh
   ./deploy.sh
   
   # On Windows
   deploy.bat
   ```

3. **Access the Application**
   - Frontend: http://localhost
   - Backend API: http://localhost:5000

### Option 2: Manual Setup

1. **Backend Setup**
   ```bash
   cd backend
   pip install -r ../requirement.txt
   python app.py
   ```

2. **Frontend Setup**
   - Open `Frontend/index.html` in a web browser
   - Or serve with any web server

## API Endpoints

- `GET /` - Health check
- `POST /analyze` - Analyze emotion from text
- `GET /sentiment-trend` - Get emotion statistics

## Project Structure

```
EmotionEye/
├── backend/
│   ├── app.py          # Flask API server
│   └── test.py         # API tests
├── Frontend/
│   ├── index.html      # Main web interface
│   ├── app.js          # Frontend JavaScript
│   └── style.css       # Styling
├── docker-compose.yml  # Docker services
├── Dockerfile          # Container configuration
├── nginx.conf          # Web server config
├── requirement.txt     # Python dependencies
└── deploy.sh/bat       # Deployment scripts
```

## Deployment Options

### Local Development
```bash
python backend/app.py
```

### Docker Container
```bash
docker-compose up --build
```

### Cloud Deployment
The application is ready for deployment on:
- AWS (ECS, EC2, Elastic Beanstalk)
- Google Cloud Platform
- Azure Container Instances
- Heroku
- DigitalOcean App Platform

## Environment Variables

Create a `.env` file for custom configuration:

```env
FLASK_ENV=production
FLASK_DEBUG=False
HOST=0.0.0.0
PORT=5000
MODEL_NAME=bhadresh-savani/distilbert-base-uncased-emotion
```

## Technologies Used

- **Backend**: Flask, Transformers, PyTorch
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **AI Model**: DistilBERT for emotion classification
- **Deployment**: Docker, Nginx, Gunicorn

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please create an issue in the repository.