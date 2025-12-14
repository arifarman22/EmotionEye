import requests
import json

def test_negative_phrases():
    """Test negative phrases that might be misclassified"""
    url = "http://127.0.0.1:5000/analyze"
    
    test_messages = [
        "I am not feeling good right now",
        "I'm not doing well today",
        "I don't feel okay",
        "I'm not happy with this situation",
        "I feel bad about what happened",
        "This is not great news",
        "I'm unhappy with the results",
        "I'm upset about the decision"
    ]
    
    print("Testing negative phrase detection...")
    print("=" * 60)
    
    for message in test_messages:
        data = {"message": message}
        response = requests.post(url, json=data)
        result = response.json()
        
        print(f"Message: {message}")
        print(f"Detected Emotion: {result.get('emotion', 'N/A')}")
        print(f"Confidence: {result.get('confidence', 0) * 100:.1f}%")
        if 'original_classification' in result:
            print(f"Original Classification: {result.get('original_classification', 'N/A')}")
        print(f"Bot Reply: {result.get('reply', 'N/A')}")
        print("-" * 50)

def test_positive_phrases():
    """Test positive phrases to ensure they're still correctly classified"""
    url = "http://127.0.0.1:5000/analyze"
    
    test_messages = [
        "I'm feeling incredibly happy today!",
        "This is wonderful news",
        "I'm so excited about this",
        "I feel great today",
        "Everything is going well",
        "I'm delighted with the outcome"
    ]
    
    print("\nTesting positive phrase detection...")
    print("=" * 60)
    
    for message in test_messages:
        data = {"message": message}
        response = requests.post(url, json=data)
        result = response.json()
        
        print(f"Message: {message}")
        print(f"Detected Emotion: {result.get('emotion', 'N/A')}")
        print(f"Confidence: {result.get('confidence', 0) * 100:.1f}%")
        if 'original_classification' in result:
            print(f"Original Classification: {result.get('original_classification', 'N/A')}")
        print(f"Bot Reply: {result.get('reply', 'N/A')}")
        print("-" * 50)

if __name__ == "__main__":
    print("Testing Emotion Analysis API with improved negative phrase detection...\n")
    test_negative_phrases()
    test_positive_phrases()