"""
Example script demonstrating how to use the Trade Opportunities API.
"""
import requests
import json
from datetime import datetime


# Configuration
API_KEY = "my_secure_api_key_12345"  # Change this to your actual API key
BASE_URL = "http://localhost:8000"
HEADERS = {"X-API-Key": API_KEY}


def check_health():
    """Check if the API is healthy"""
    print("🏥 Checking API health...")
    response = requests.get(f"{BASE_URL}/health")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API is {data['status']}")
        print(f"   Version: {data['version']}")
        return True
    else:
        print(f"❌ API is not responding: {response.status_code}")
        return False


def get_session_info():
    """Get current session information"""
    print("\n📊 Getting session info...")
    response = requests.get(f"{BASE_URL}/api/v1/session", headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Session ID: {data['session_id'][:16]}...")
        print(f"   Requests Made: {data['requests_made']}")
        print(f"   Requests Remaining: {data['requests_remaining']}")
        return True
    else:
        print(f"❌ Failed to get session info: {response.status_code}")
        print(f"   {response.text}")
        return False


def analyze_sector(sector_name):
    """Analyze a specific sector"""
    print(f"\n🔍 Analyzing {sector_name} sector...")
    response = requests.get(
        f"{BASE_URL}/api/v1/analyze/{sector_name}",
        headers=HEADERS
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Analysis complete!")
        print(f"   Sector: {data['sector']}")
        print(f"   Sources Found: {data['metadata']['sources_found']}")
        print(f"   Analysis Time: {data['metadata']['analysis_time']}s")
        print(f"   Requests Remaining: {data['requests_remaining']}")
        
        # Save report to file
        filename = f"{sector_name.replace(' ', '_')}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data['report'])
        
        print(f"\n📄 Report saved to: {filename}")
        print(f"\n📋 Report Preview (first 500 characters):")
        print("-" * 80)
        print(data['report'][:500] + "...")
        print("-" * 80)
        
        return True
        
    elif response.status_code == 401:
        print(f"❌ Authentication failed: Invalid API key")
        print(f"   Make sure your API_KEY matches the one in .env file")
        return False
        
    elif response.status_code == 429:
        print(f"❌ Rate limit exceeded")
        data = response.json()
        print(f"   {data['detail']}")
        return False
        
    else:
        print(f"❌ Failed to analyze sector: {response.status_code}")
        print(f"   {response.text}")
        return False


def main():
    """Main function"""
    print("=" * 80)
    print("Trade Opportunities API - Example Client")
    print("=" * 80)
    
    # Check health
    if not check_health():
        print("\n⚠️  Make sure the API is running:")
        print("   python main.py")
        print("   or")
        print("   uvicorn main:app --reload")
        return
    
    # Get session info
    get_session_info()
    
    # Analyze sectors
    sectors = ["pharmaceuticals", "technology", "agriculture"]
    
    print(f"\n🚀 Analyzing {len(sectors)} sectors...")
    
    for sector in sectors:
        success = analyze_sector(sector)
        if not success:
            break
        print()
    
    print("\n✨ Done! Check the generated .md files for detailed reports.")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

