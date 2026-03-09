"""
Simple test script - Just run this!

Basic end-to-end API testing.
"""
import requests
import json

print("=" * 60)
print("TESTING TRADE OPPORTUNITIES API")
print("=" * 60)

# Test 1: Check if server is running
print("\n1. Checking if server is running...")
try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    if response.status_code == 200:
        print("✅ Server is running!")
    else:
        print("❌ Server problem!")
        exit()
except:
    print("❌ Server not running! Start it first.")
    print("   Run: uvicorn main:app --reload")
    exit()

# Test 2: Analyze a sector
print("\n2. Analyzing pharmaceuticals sector...")
print("   (This will take 5-10 seconds...)")

headers = {
    "X-API-Key": "my_secure_api_key_12345"
}

try:
    response = requests.get(
        "http://localhost:8000/api/v1/analyze/pharmaceuticals",
        headers=headers,
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ SUCCESS! Got the report!")
        print(f"   Sector: {data['sector']}")
        print(f"   Sources found: {data['metadata']['sources_found']}")
        print(f"   Analysis time: {data['metadata']['analysis_time']}s")
        print(f"   Requests remaining: {data['requests_remaining']}")
        
        # Save report
        filename = "pharmaceuticals_report.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data['report'])
        
        print(f"\n📄 Full report saved to: {filename}")
        print("\n📋 Report Preview (first 800 characters):")
        print("-" * 60)
        print(data['report'][:800])
        print("...")
        print("-" * 60)
        
    elif response.status_code == 401:
        print("\n❌ Authentication failed!")
        print("   The API key might be wrong in the code.")
        
    elif response.status_code == 429:
        print("\n❌ Rate limit exceeded!")
        print("   You've made too many requests. Wait 1 hour.")
        
    else:
        print(f"\n❌ Error {response.status_code}")
        print(response.text)
        
except requests.exceptions.Timeout:
    print("\n❌ Request timed out (took too long)")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")

print("\n" + "=" * 60)
print("DONE!")
print("=" * 60)

