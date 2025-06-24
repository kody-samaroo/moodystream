# 🎧 MoodyStream

MoodyStream is a serverless Python app that creates 3 personalized Spotify playlists based on your top artists’ genres — each designed to deliver a distinct mood or vibe.

## 🚀 What It Does

- Analyzes your top 3 artists on Spotify
- Extracts their primary genres
- Searches for tracks within those genres
- Generates 3 public playlists in your Spotify account

## 🧰 Tech Stack

| Tool | Purpose |
|------|---------|
| **AWS Lambda** | Runs the playlist generation logic |
| **Spotify Web API** | Gets user data and creates playlists |
| **Spotipy** | Python wrapper for the Spotify API |
| **Python 3.12** | Core runtime |
| **AWS CLI** | Deployment and configuration |
| **AWS Secrets Manager** | (Coming Soon) Securely store Spotify credentials |
| **API Gateway** | (Planned) HTTP endpoint to trigger playlist creation |

## 📦 Folder Structure

