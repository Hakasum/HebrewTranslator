"""
Test script to verify English and Spanish to Hebrew translations
"""
import requests
import json
import time

# API endpoint
BASE_URL = "http://localhost:5005"

def test_translation(text, source, target):
    """Test a single translation"""
    print(f"\n{'='*60}")
    print(f"Testing: {source} -> {target}")
    print(f"Input: {text}")
    print('-'*60)
    
    payload = {
        "text": text,
        "source": source,
        "target": target
    }
    
    print(f"Request payload:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(f"{BASE_URL}/translate", json=payload)
        print(f"\nResponse status: {response.status_code}")
        
        result = response.json()
        print(f"Response body:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if response.status_code == 200:
            translation = result.get('translation', '')
            print(f"\n✓ Translation successful!")
            print(f"  Output: {translation}")
            return True
        else:
            print(f"\n✗ Translation failed!")
            return False
            
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("Hebrew Translator API - Test Suite")
    print("="*60)
    
    # First check if API is healthy
    print("\n[1] Checking API health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✓ API is healthy!")
            print(json.dumps(response.json(), indent=2))
        else:
            print("✗ API health check failed!")
            return
    except Exception as e:
        print(f"✗ Cannot connect to API: {e}")
        print(f"Make sure the server is running on {BASE_URL}")
        return
    
    # Test cases
    test_cases = [
        # English to Hebrew
        {
            "text": "Hello world",
            "source": "en",
            "target": "he",
            "name": "English to Hebrew - Simple"
        },
        {
            "text": "Good morning, how are you?",
            "source": "en",
            "target": "he",
            "name": "English to Hebrew - Sentence"
        },
        {
            "text": "The weather is beautiful today.",
            "source": "en",
            "target": "he",
            "name": "English to Hebrew - Complex"
        },
        # Spanish to Hebrew
        {
            "text": "Hola mundo",
            "source": "es",
            "target": "he",
            "name": "Spanish to Hebrew - Simple"
        },
        {
            "text": "Buenos días, ¿cómo estás?",
            "source": "es",
            "target": "he",
            "name": "Spanish to Hebrew - Sentence"
        },
        {
            "text": "El clima está hermoso hoy.",
            "source": "es",
            "target": "he",
            "name": "Spanish to Hebrew - Complex"
        },
    ]
    
    print("\n" + "="*60)
    print("[2] Running translation tests...")
    print("="*60)
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n\n[Test {i}/{len(test_cases)}] {test_case['name']}")
        success = test_translation(
            test_case['text'],
            test_case['source'],
            test_case['target']
        )
        results.append({
            "name": test_case['name'],
            "success": success
        })
        time.sleep(0.5)  # Small delay between requests
    
    # Summary
    print("\n\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(1 for r in results if r['success'])
    total = len(results)
    
    for i, result in enumerate(results, 1):
        status = "✓ PASS" if result['success'] else "✗ FAIL"
        print(f"{i}. {status} - {result['name']}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

if __name__ == "__main__":
    main()

