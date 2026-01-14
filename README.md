# Lyrical Lab

A comprehensive web application for songwriters and musicians to create, analyze, and manage lyrics. This tool provides features like syllable counting, rhyme detection, and song saving, with plans to evolve into a full SaaS platform.

## Features

- **Syllable Counter**: Analyze lyrics for syllable count per line.
- **Song Saving**: Store and manage your songs with metadata (title, artist, album, mood, genre).
- **User Authentication**: Secure login and session management.
- **Responsive UI**: Built with Svelte for a modern, fast user experience.

## Tech Stack

- **Frontend**: SvelteKit
- **Backend**: FastAPI (Python)
- **Database**: SQLAlchemy with ORM
- **Authentication**: OAuth2 with JWT tokens
- **Deployment**: Ready for cloud hosting (e.g., Vercel for frontend, Railway/Heroku for backend)

## Installation

### Prerequisites
- Node.js (for frontend)
- Python 3.8+ (for backend)
- Git

### Backend Setup
1. Navigate to the backend directory:
   ```
   cd lyrical-lab-backend
   ```
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up the database (assuming SQLite for development):
   ```
   alembic upgrade head
   ```
5. Run the server:
   ```
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd my-app
   ```
2. Install dependencies:
   ```
   npm install
   ```
3. Run the development server:
   ```
   npm run dev
   ```
   The app will be available at `http://localhost:5173`.

## Usage

1. Register/Login to access the tools.
2. Use the syllable counter to analyze your lyrics.
3. Save songs with metadata for future reference.
4. Explore additional features as they are added.

## API Endpoints

- `POST /api/lyric-tools/syllable-counter`: Count syllables in provided text.
- `POST /api/lyric-tools/save-song`: Save a song with metadata.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

1. Fork the repo.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -m 'Add feature'`.
4. Push to branch: `git push origin feature-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

- Advanced rhyme and meter analysis.
- Collaboration features for songwriting teams.
- Integration with music production tools.
- Monetization features for SaaS launch.