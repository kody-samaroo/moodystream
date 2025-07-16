# MoodyStream: Spotify Playlist Generator on AWS Lambda

## Overview

MoodyStream is a cloud-native web application that generates Spotify playlists based on a user’s favorite artists. It demonstrates:

- Serverless architecture with AWS Lambda and API Gateway  
- Spotify OAuth 2.0 Authorization Code Flow  
- Secure credential storage using AWS Secrets Manager  
- Python application packaging for cloud deployment  

---

## Architecture Diagram

![alt text](image.png)
_User → API Gateway → Lambda Function → Spotify API / AWS Secrets Manager_



---

## Technologies & Services Used

- **AWS Lambda**
- **AWS API Gateway**
- **AWS Secrets Manager**
- **IAM (Role-Based Access Control)**
- **Python 3.12**
- **Flask**
- **Spotipy**
- **Mangum**

---

## Features

- Authenticate via Spotify using OAuth 2.0  
- Generate playlists using:  
  - Top tracks from user’s favorite artists  
  - As well as less popular tracks from those same artists  
- Store credentials securely in AWS Secrets Manager  
- Serverless

---

## Setup Instructions

### Local


Clone the repository:
```bash
git clone https://github.com/your-username/moodystream.git
cd moodystream
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Copy secrets into `.ENV` file:
```env
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
SCOPE=user-top-read playlist-modify-public
```

Run application:
```
python main.py
```

### Cloud (AWS Lambda)

##### Step 1: Upload Secrets to AWS Secrets Manager
Secret Name: `moodystream/spotify`

Keys:

- `SPOTIPY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET`
- `SPOTIPY_REDIRECT_URI`

##### Step 2: Package and Deploy

Install Python packages locally:
```
pip install -r requirements.txt -t ./package
```

Package your app:
```
cd package
zip -r9 ../lambda_function.zip .
```

Upload `lambda_function.zip` via the AWS Console or AWS CLI.

##### Step 3: Configure API Gateway

- Create an HTTP API with a {proxy+} route
- Attach Lambda integration
- Deploy and use the public API Gateway URL


### Security Considerations

- OAuth credentials stored in AWS Secrets Manager
- IAM roles restricted with least privilege
- No long-term user data storage
