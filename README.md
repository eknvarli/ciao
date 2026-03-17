# 🎧 Ciao Music API

Ciao is a high-performance, asynchronous music streaming backend built with FastAPI, designed for modern mobile applications.

It leverages an open-source YouTube Music wrapper for structured metadata retrieval and yt-dlp for efficient, low-latency audio streaming.

## ⚡ Features

- 🔍 Global music search
- 🎵 Track metadata (title, artist, thumbnails)
- 📡 Direct audio stream extraction (m4a/webm)
- 📂 User playlist management
- 🔐 JWT-based authentication
- ⚡ Fully asynchronous FastAPI architecture

## 📡 API Overview

### Auth
- POST `/api/v1/auth/register`
- POST `/api/v1/auth/login`

### Music
- GET `/api/v1/search`
- GET `/api/v1/tracks/{video_id}`
- GET `/api/v1/streams/{video_id}`

### Playlists
- POST `/api/v1/playlists/`
- GET `/api/v1/playlists/`
- GET `/api/v1/playlists/{playlist_id}`
- POST `/api/v1/playlists/{playlist_id}/tracks`