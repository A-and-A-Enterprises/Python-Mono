import requests

def main():
    print("Hello from pip-project-1")
    response = requests.get("https://github.com")
    print(f"Status: {response.status_code}")

if __name__ == "__main__":
    main()
