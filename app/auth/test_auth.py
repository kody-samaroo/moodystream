# moodystream/auth/test_auth.py

from spotify_auth import get_auth_url, get_token_from_code

print("Go to the following URL and authorize:")
print(get_auth_url())

auth_code = input("Paste the redirect code here: ")
token_data = get_token_from_code(auth_code)

print("\nAccess token:", token_data["access_token"])
print("Refresh token:", token_data.get("refresh_token"))
