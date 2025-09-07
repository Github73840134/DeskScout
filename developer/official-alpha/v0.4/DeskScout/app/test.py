from requests_oauthlib import OAuth2Session

client_id = "f0XG4DL7Q2NCDLKiiOBhvCI4ktGvrzSR"
client_secret = "KvcWEZC4zIKwO3Vc"
authorization_base_url = "https://api.dexcom.com/v2/oauth2/login"
token_url = "https://example.com/oauth2/token"

# Step 1: Redirect user to authorization URL
github = OAuth2Session(client_id)
authorization_url, state = github.authorization_url(authorization_base_url)

print(f"Please visit this URL to authorize: {authorization_url}")

# After the user authorizes, they will be redirected to your redirect URI
redirect_response = input("Paste the full redirect URL here:")

# Step 2: Fetch the access token
token = github.fetch_token(
    token_url,
    client_secret=client_secret,
    authorization_response=redirect_response,
)

# Now you can make requests using the access token
resource_url = "https://api.example.com/resource"
response = github.get(resource_url)
print(response.content)