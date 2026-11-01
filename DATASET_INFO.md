# LearnSeek – Dataset Information

## Dataset plan

The initial LearnSeek collection is planned to contain **200 educational YouTube videos** across **9 subject categories**. Video metadata will be collected with the YouTube Data API and stored locally in `dataset/`. The local prepared dataset is the source for offline search when the API is unavailable.

The category names below are a practical starting proposal and can be refined before collection:

1. Mathematics
2. Physics
3. Chemistry
4. Biology
5. Computer Science
6. Engineering
7. History
8. Geography
9. Language and Literature

A balanced distribution would be approximately 22 videos per category, with the remaining 2 assigned to categories that have suitable results (for example, 23 in two categories and 22 in the other seven). This is a target, not a claim that records have already been collected.

## Live query collection

For each new/different live search query, LearnSeek is planned to request 10 fresh videos. Results for the same normalized query should be reused for 10 minutes. This short-lived query cache is distinct from the durable prepared dataset: the initial 200-video collection remains locally searchable even if the YouTube API is unavailable.

## Proposed record fields

| Field | Purpose |
| --- | --- |
| `video_id` | Stable YouTube video identifier; use it to detect duplicates. |
| `title` | Video title and an important searchable field. |
| `description` | Video description and searchable context. |
| `channel_title` | Name of the publishing channel. |
| `category` | One of the project’s 9 subject categories. |
| `published_at` | Publication date/time returned by the API, when available. |
| `video_url` | Link to the video. |
| `thumbnail_url` | Optional thumbnail link, if retained. |
| `source_query` | Query used to discover the record, when applicable. |
| `collected_at` | Time the metadata was collected. |

The final file format and exact field names will be settled during implementation. Avoid storing fields that are not needed for search, display, or project evaluation.

## Preparation and quality guidelines

- Remove duplicate records using `video_id`.
- Check that each record has a usable ID, title, category, and video URL.
- Assign each record to exactly one of the 9 categories.
- Treat missing descriptions as empty text during indexing rather than failing the entire dataset load.
- Keep text encoding consistent (UTF-8 is recommended).
- Record collection time and discovery query where useful for understanding provenance.
- Review that the final prepared collection reaches the target of 200 videos and has category counts recorded.
- Keep the dataset local and searchable without a live API request.

## Suggested local organization

```text
dataset/
├── raw/        # Optional unmodified API response exports
└── processed/  # Clean, deduplicated records used by local search
```

These subfolders are suggestions only and have not been created. The requested `dataset/` folder is currently empty. No videos or API responses have been collected yet.

## API and credential note

The YouTube Data API is the planned metadata source. Its key must be supplied privately through a local `.env` file based on `.env.example`. Never put a real key in this document, the example template, source control, or a public dataset export.
