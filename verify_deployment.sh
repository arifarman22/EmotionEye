#!/bin/bash

echo "🔍 Verifying EmotionEye deployment..."

# Check if containers are running
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Containers are not running. Please run deploy.sh first."
    exit 1
fi

# Run deployment tests
echo "🧪 Running API tests..."
python test_deployment.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment verification completed successfully!"
    echo "🌐 Your EmotionEye application is ready at:"
    echo "   Frontend: http://localhost"
    echo "   Backend:  http://localhost:5000"
    echo ""
    echo "📋 Useful commands:"
    echo "   View logs:     docker-compose logs -f"
    echo "   Stop service:  docker-compose down"
    echo "   Restart:       docker-compose restart"
else
    echo "❌ Deployment verification failed!"
    echo "📋 Troubleshooting:"
    echo "   Check logs:    docker-compose logs"
    echo "   Restart:       docker-compose restart"
    exit 1
fi