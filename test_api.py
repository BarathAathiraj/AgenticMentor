#!/usr/bin/env python3
"""
Test the API response to debug projects count issue
"""

import requests
import json

def test_api():
    """Test the API stats endpoint"""
    
    print("🔍 Testing API Response")
    print("=" * 40)
    
    try:
        # Test the stats endpoint
        response = requests.get("http://localhost:3000/api/stats")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Response Status: {response.status_code}")
            print(f"📊 Response Data:")
            print(json.dumps(data, indent=2))
            
            # Check specific fields
            print(f"\n🔍 Analysis:")
            print(f"   Documents: {data.get('documents', 'NOT FOUND')}")
            print(f"   Projects: {data.get('repositories', 'NOT FOUND')}")
            print(f"   Repositories List: {'FOUND' if 'repositories_list' in data else 'NOT FOUND'}")
            
            if 'repositories_list' in data:
                print(f"   Repositories List Length: {len(data['repositories_list'])}")
                for i, repo in enumerate(data['repositories_list'][:3]):
                    print(f"   - {i+1}. {repo}")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is it running on localhost:3000?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api() 