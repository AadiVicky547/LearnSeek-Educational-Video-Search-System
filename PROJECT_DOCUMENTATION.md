# LearnSeek – Project Documentation

## 1. Purpose

LearnSeek is a proposed educational video search engine for an Information Retrieval mini-project. It will help a user find relevant YouTube learning videos using both the words in a query and the query’s meaning. This document describes the design; it does not represent implemented behavior.

## 2. Goals and scope

The planned first dataset contains 200 educational videos organized into 9 subject categories. A YouTube Data API collector will support initial data gathering and live searches. For each different live search query, the system will request 10 fresh videos. An identical query will reuse its cached response for 10 minutes. Independently, the prepared local collection must remain searchable when the API cannot be reached.

The interface will use Streamlit. Python, Pandas, and Scikit-learn will support data preparation and retrieval. TF-IDF will provide keyword retrieval, while Sentence Transformers will provide semantic retrieval. A hybrid method will combine them. The interface will show only the final ranked results and relevance percentages, rather than separate retrieval-method scores.

## 3. Proposed architecture

```text
User
  │ search query
  ▼
Streamlit interface (src/)
  │ normalized query
  ▼
Search coordinator (planned in src/)
  ├── Local dataset loader ──► prepared video metadata (dataset/)
  ├── Live query cache ──────► 10-minute query-result entries
  ├── YouTube API collector ─► 10 fresh videos for a cache miss/new query
  └── Hybrid retrieval
       ├── TF-IDF keyword retrieval (Scikit-learn)
       └── Sentence Transformers semantic retrieval
  │ merge, rank, and scale final relevance
  ▼
Final video results with relevance percentages
```

The exact module boundaries and cache storage mechanism will be selected during implementation. The diagram shows responsibilities, not existing source files.

## 4. Data flow

1. The user enters a search query in Streamlit.
2. The search coordinator normalizes the query for matching. The original wording can still be retained for display or API requests.
3. The local prepared dataset is loaded and searched, so it can provide results without a network connection.
4. For live collection, the coordinator checks whether the normalized query has a cached response that is less than 10 minutes old. If so, it reuses those results. Otherwise it requests up to 10 fresh matching videos using the YouTube Data API and stores the response with its retrieval time.
5. Available local and live video records are prepared for retrieval. Duplicate video IDs should be consolidated.
6. The hybrid retriever scores the candidate records, combines the two retrieval signals, sorts the candidates, and prepares a final relevance percentage.
7. Streamlit displays the final results and their relevance percentages. Internal component scores are not shown.

A network/API failure should not prevent local search. If live collection fails, the search should continue against the local collection and communicate API availability in a simple, user-understandable way if needed.

## 5. Retrieval methodology

### 5.1 Text preparation

Use video title, description, and subject category as searchable text, with fields combined or weighted deliberately. Normalize missing text and duplicate records before indexing. Preserve useful metadata such as video ID, title, channel, URL, category, and publication date for the result display.

### 5.2 TF-IDF keyword retrieval

TF-IDF (term frequency–inverse document frequency) represents each video as a weighted vector of terms. Common terms receive less weight, while terms that distinguish a video receive more. Transform the query with the same vectorizer and compare it with video vectors, for example with cosine similarity. This method is useful when query terms overlap with a title or description.

### 5.3 Semantic retrieval

A Sentence Transformers model encodes the query and each candidate’s searchable text as dense vectors. Similarity between these vectors can surface videos that express the same idea with different words. The selected model and its version should be recorded when implementation begins; this planning document does not download or select model files.

### 5.4 Hybrid ranking

Normalize or otherwise put both retrieval scores on a comparable scale, then combine them with a weighted score:

`hybrid_score = alpha × tfidf_score + (1 - alpha) × semantic_score`

Here, `alpha` is a configurable weight between 0 and 1. Its initial value should be chosen and documented during implementation, then adjusted using representative queries and relevance judgments. A larger value gives keyword matching more influence. Candidates are ranked by the combined score, with a deterministic tie-break rule such as video ID.

The final relevance percentage is a presentation value derived from the final ranking scores, for example by scaling the highest result to 100 and the other results proportionally. It is a relative relevance indicator, not a probability that a result is correct. The precise scaling should be finalized alongside the implementation and described in the interface.

## 6. Query caching and live collection

- Cache key: normalized query (case and surrounding whitespace should not create accidental duplicate entries).
- Cache lifetime: 10 minutes from retrieval time.
- Cache value: the query’s live video metadata and fetch timestamp.
- Cache miss or expired entry: request 10 fresh videos for that query and update the entry when successful.
- Different query: perform a fresh live request rather than reusing an unrelated query’s response.
- API unavailable or request fails: retain local dataset search and do not claim live results were refreshed.

The implementation should also handle API quota limits and malformed or empty responses. The API key belongs in a local `.env` file and must never be committed.

## 7. Planned components

| Component | Responsibility |
| --- | --- |
| Streamlit interface | Accept a query and render final video results with relevance percentages. |
| Dataset loader | Read and validate locally stored prepared metadata. |
| YouTube collector | Fetch initial collection records and 10 fresh records for a live query. |
| Query cache | Reuse identical live-query results for 10 minutes. |
| Text preparation | Build consistent searchable text and handle missing fields/duplicates. |
| TF-IDF retriever | Produce keyword-based candidate scores. |
| Semantic retriever | Produce Sentence Transformers similarity scores. |
| Hybrid ranker | Combine scores, order results, and produce display relevance values. |

These are proposed responsibilities. No implementation modules exist yet.

## 8. Privacy, credentials, and local operation

Do not commit API keys or other credentials. Use `.env.example` only as a template and keep the real `.env` local. Keep the prepared dataset on the local machine as planned. The initial project should avoid collecting personal data; video metadata is the intended content.

## 9. Implementation milestones

1. Confirm the dataset fields, category names, and collection process.
2. Collect and validate 200 educational video records in the local dataset.
3. Implement dataset loading, query normalization, and 10-minute live-query caching.
4. Implement TF-IDF and semantic retrieval, then combine and scale the scores.
5. Build the Streamlit interface to show final results and relevance percentages.
6. Add project checks and document observed limitations and setup steps.
