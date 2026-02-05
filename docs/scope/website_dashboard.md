b# 1) Web Dashboard Scope

## Dashboard MVP Goals

The dashboard must do three things well:

1. **Re-entry:** allow the user to continue where they left off
2. **Navigation:** make it easy to find and manage projects
3. **Light insight:** provide gentle, non-judgmental writing statistics

Anything beyond this (advanced analytics, prompts, visualizations) is explicitly out of scope for the MVP.

---

## MVP Features

### A) Workspace Hub

* **Continue writing** (last edited song)
* **Recent songs** (last 8–12 items)
* **Pinned songs** (optional, low complexity, high utility)
* **Search**

  * Title search
  * Content substring search
  * NLP-based search is out of scope

---

### B) Quick Stats (Minimal)

Weekly, aggregated metrics only:

* Total writing time
* Number of writing sessions
* Output metric (choose one initially):

  * Words added
  * or lines/bars added

These stats are informational only and should not imply performance evaluation.

---

### C) Draft State and Metadata

Each song exposes:

* Status: `draft | revising | polished | archived`
* Last updated timestamp
* Optional tags (can be deferred)

---

## Explicitly Out of Scope (Phase 2)

The following features must not be implemented as part of the MVP:

* Rhyme density charts or phoneme visualizations
* AI critique summaries shown on the dashboard
* Version diff UI
* NLP-powered internal search UI

---

# 2) UI Structure (Web)

Target framework: **SvelteKit**

### Route

* `/dashboard`

---

## Layout

### Header

* Page title: “Dashboard”
* Global song search bar
* Primary actions:

  * New Song
  * Continue
  for desktop
* Account state indicator:

  * Local-only
  * Online features enabled

---

### Main Column (Primary Content)

**Continue Writing**

* Song title
* Last edited timestamp
* Action: Continue

**Recent Songs**

* Grid or list layout
* Per-item information:

  * Title
  * Status
  * Last updated
* Per-item actions:

  * Pin / unpin
  * Rename
  * Archive

---

### Side Column (Secondary Content)

**This Week**

* Minutes written
* Number of sessions
* Output metric

**Quick Shortcuts**

* Rhyme engine
* Flow alignment
* Synonyms / homophones
* Critique

These shortcuts navigate to existing tools. No heavy computation runs from the dashboard.

---

### Optional Section

**Pinned Songs**

* Visible only if at least one song is pinned

---

# 3) API Routes (FastAPI)

The following routes define the backend contract required for the dashboard.

## Authentication Assumptions

* All routes require `current_user`
* All list endpoints support pagination

---

## A) Songs

### 1) Dashboard Overview

**GET** `/api/dashboard/overview`

Returns:

```json
{
  "continue": {
    "song_id": 123,
    "title": "X",
    "updated_at": "...",
    "status": "draft"
  },
  "recent": [ ... up to 12 items ... ],
  "pinned": [ ... ],
  "stats_week": {
    "minutes": 140,
    "sessions": 5,
    "words_added": 420
  }
}
```

Purpose: load all dashboard data in a single request.

---

### 2) List Songs

**GET** `/api/songs`

Query parameters:

* `q` (search string)
* `status` (optional)
* `pinned` (optional boolean)
* `page`
* `size`

Returns:

```json
{
  "items": [...],
  "page": 1,
  "size": 12,
  "total": 57
}
```

---

### 3) Create Song

**POST** `/api/songs`

Body:

* `title` (optional, default: “Untitled”)
* `content` (optional)

Returns the created song object.

---

### 4) Get Song

**GET** `/api/songs/{song_id}`

---

### 5) Update Song Metadata

**PATCH** `/api/songs/{song_id}`

Body may include:

* `title`
* `status`
* `tags` (optional, can be deferred)

---

### 6) Pin / Unpin Song

**POST** `/api/songs/{song_id}/pin`
**DELETE** `/api/songs/{song_id}/pin`

---

### 7) Archive / Unarchive Song

**POST** `/api/songs/{song_id}/archive`
**DELETE** `/api/songs/{song_id}/archive`

---

## B) Session Tracking

### 1) Start Session

**POST** `/api/sessions/start`

Body:

* `song_id` (optional)

Returns:

* `session_id`

---

### 2) End Session

**POST** `/api/sessions/{session_id}/end`

Body:

* `song_id` (optional)
* `words_added` or `lines_added` (computed client-side)

---

### 3) Weekly Writing Stats

**GET** `/api/stats/writing?range=week`

Returns:

```json
{
  "minutes": 140,
  "sessions": 5,
  "words_added": 420
}
```

---

# 4) Storing Scope in the Repository

Including scope documentation in the repository is strongly recommended.

## Benefits

* Prevents uncontrolled scope expansion
* Makes project re-entry easier over time
* Supports building in public with clear references
* Improves issue and pull request clarity by anchoring work to defined scope
.
