import requests

def test_search():
    print("Testing gateway global search api...")
    try:
        res = requests.get('https://e836eae639457939-103-210-91-37.serveousercontent.com/api/search/?q=Laptop')
        data = res.json()
        
        print(f"Status: {res.status_code}")
        print(f"Results Count: {len(data.get('results', []))}")
        
        # If services are not running, it gracefully returns [] due to our except blocks
        assert res.status_code == 200, "Should return 200 OK"
        assert 'results' in data, "Should have results key"
        
        print("API test successful!")
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == '__main__':
    test_search()
