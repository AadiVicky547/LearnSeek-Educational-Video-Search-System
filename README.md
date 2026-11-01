# LearnSeek – Educational Video Search Engine

LearnSeek is a beginner-friendly Information Retrieval mini-project for finding educational YouTube videos. The planned system combines keyword search and meaning-based search, then shows users the final ranked videos with relevance percentages.

> **Project status:** Phase 1 is implemented: live YouTube search and a basic Streamlit interface. Retrieval ranking, query caching, and the initial local dataset are later phases.

## Planned capabilities

- Prepare an initial local collection of 200 educational videos across 9 subject categories.
- Collect video metadata with the YouTube Data API.
- Fetch 10 fresh videos for a new live search query; reuse results for the same query for 10 minutes.
- Search the prepared local dataset even when YouTube's API is unavailable.
- Combine TF-IDF keyword retrieval with Sentence Transformers semantic retrieval.
- Present final search results and relevance percentages in a Streamlit interface.
- Use Python, Pandas, and Scikit-learn for the project’s data and retrieval work.

## Project structure

```text
LearnSeek_IRproject/
├── .env.example              # Names and explanations for settings; values are placeholders
├── .gitignore                # Files and local data that Git should not track
├── DATASET_INFO.md           # Dataset plan, fields, categories, and collection notes
├── PROJECT_DOCUMENTATION.md  # Proposed architecture and retrieval methodology
├── README.md                 # Project overview, setup direction, and folder/file guide
├── requirements.txt          # Python dependencies, grouped by purpose
├── assets/                   # Optional diagrams and other project presentation assets
├── dataset/                  # Locally stored source and prepared video metadata
├── models/                   # Local model artifacts or retrieval index artifacts, if needed
├── src/
│   ├── app.py                # Streamlit homepage and live search results
│   ├── youtube_service.py    # YouTube API connection, metadata mapping, and safe errors
│   └── __init__.py           # Marks src as a Python package
└── tests/
    └── test_youtube_service.py # Offline unit tests for the YouTube search module
```

### Folder and file purposes

- `dataset/`: Holds the initial video collection and prepared local data files. Keeping a local copy allows dataset search when the YouTube API is down or unavailable.
- `src/`: Contains the Streamlit interface and YouTube API search module. Retrieval, caching, and local dataset modules are planned for later phases.
- `assets/`: Holds project diagrams, screenshots, and other supporting visual materials.
- `models/`: Holds downloaded Sentence Transformers model files or saved retrieval artifacts when the implementation needs them. Model files are not included now.
- `tests/`: Contains offline unit tests for the Phase 1 YouTube search module. Further retrieval and dataset checks can be added in later phases.
- `README.md`: The project’s starting point and structure guide.
- `requirements.txt`: A categorized list of Python dependencies for the app and planned retrieval work.
- `.env.example`: A safe template showing configuration names. It contains no real key; copy it to `.env` and add your own key locally when ready.
- `.gitignore`: Helps keep credentials, virtual environments, caches, and generated/local data out of Git.
- `PROJECT_DOCUMENTATION.md`: Explains the proposed architecture and retrieval process.
- `DATASET_INFO.md`: Describes the planned dataset schema and collection approach.

## Run LearnSeek

Use the existing virtual environment and run these commands from the project root in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run src/app.py
```

The app reads `YOUTUBE_API_KEY` from the project-root `.env` file. Keep that file private and do not commit it. Search results come from YouTube Data API v3; the app does not show placeholder videos. The first search uses YouTube API quota.

## Current status

- [x] Project structure and planning documents
- [ ] Collect and prepare the initial 200-video dataset
- [x] Implement the Phase 1 live-search interface and YouTube API connection
- [ ] Implement TF-IDF and semantic retrieval, caching, and the initial local dataset
- [ ] Add checks and validate the finished application
