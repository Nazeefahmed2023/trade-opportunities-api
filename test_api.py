"""Test API endpoints with authentication."""
import requests
import json

print("Testing Trade Opportunities API with new Gemini key...")
print("=" * 60)

try:
    headers = {"X-API-Key": "my_secure_api_key_12345"}
    print("\n🔄 Making request to analyze technology sector...")
    print("⏳ This will take 10-20 seconds...\n")
    
    response = requests.get(
        "http://localhost:8000/api/v1/analyze/agriculture",
        headers=headers,
        timeout=120
    )
    
    print(f"✅ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Sector: {data['sector']}")
        print(f"✅ Sources Found: {data['metadata']['sources_found']}")
        print(f"✅ Analysis Time: {data['metadata']['analysis_time']}")
        print(f"\n📄 Report Preview (first 500 characters):")
        print("=" * 60)
        print(data['report'][:500])
        print("...")
        print("=" * 60)
        
        # Save full report
        with open('technology_report.md', 'w', encoding='utf-8') as f:
            f.write(data['report'])
        print(f"\n✅ Full report saved to technology_report.md")
        print(f"✅ NEW GEMINI API KEY WORKS! 🎉")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to server!")
    print("   Make sure server is running on http://localhost:8000")
except Exception as e:
    print(f"❌ Error: {e}")

