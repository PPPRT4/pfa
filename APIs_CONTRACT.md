# Contrat API — Second Brain v3

---

## Base URL
```
http://localhost:8000        ← dev local
```

---

## Structure d'une note
Voici l'objet note tel qu'il circule entre front et back :

```json
{
  "id":        1711234567890,
  "content":   "Lire le livre Atomic Habits ce weekend",
  "createdAt": "2026-03-25T11:00:00.000Z",
  "apiStatus": "success",
  "aiResult": {
    "type":     "task",
    "summary":  "Lecture planifiée pour le weekend",
    "keywords": ["lecture", "habits", "productivité"]
  }
}
```

---

## Endpoints

### 1. `POST /add-note`
Ajoute une nouvelle note.

**Request**
```json
{ "content": "Lire le livre Atomic Habits ce weekend" }
```

**Response 200**
```json
{ "status": "success" }
```

**Response 4xx/5xx** → le front affiche "Note saved locally — server unreachable."

---

### 2. `GET /notes`
Retourne toutes les notes sauvegardées.

**Response 200**
```json
[
  {
    "id":        1711234567890,
    "content":   "Lire le livre Atomic Habits ce weekend",
    "createdAt": "2026-03-25T11:00:00.000Z",
    "apiStatus": "success",
    "aiResult": {
      "type":     "task",
      "summary":  "Lecture planifiée pour le weekend",
      "keywords": ["lecture", "habits", "productivité"]
    }
  }
]
```

---

### 3. `DELETE /notes/:id`
Supprime une note par son id.

**Request** → pas de body, l'id est dans l'URL
```
DELETE /notes/1711234567890
```

**Response 200**
```json
{ "status": "deleted" }
```

---

### 4. `PUT /notes/:id`
Met à jour le contenu d'une note.

**Request**
```json
{ "content": "Nouveau contenu de la note" }
```

**Response 200** → retourne la note mise à jour
```json
{
  "id":        1711234567890,
  "content":   "Nouveau contenu de la note",
  "createdAt": "2026-03-25T11:00:00.000Z",
  "apiStatus": "success",
  "aiResult":  null
}
```

---

### 5. `POST /chat`
Envoie un message au chat IA avec les notes comme contexte.

**Request**
```json
{
  "messages": [
    { "role": "user",      "content": "Résume mes tâches" },
    { "role": "assistant", "content": "Tu as 2 tâches en cours..." },
    { "role": "user",      "content": "Laquelle est la plus urgente ?" }
  ],
  "notes": [
    {
      "content":  "Lire Atomic Habits ce weekend",
      "aiResult": {
        "type":     "task",
        "summary":  "Lecture planifiée",
        "keywords": ["lecture", "habits"]
      }
    }
  ]
}
```

**Response 200**
```json
{
  "text":    "La tâche la plus urgente semble être...",
  "noteRef": "Lire Atomic Habits ce weekend…"
}
```

---

### 6. `GET /stats`
Retourne les statistiques globales des notes.

**Response 200**
```json
{
  "total":    12,
  "analyzed":  10,
  "synced":    12,
  "breakdown": {
    "task":     4,
    "idea":     3,
    "reminder": 2,
    "resource": 1,
    "other":    2
  }
}
```

---

### 7. `POST /search`
Recherche sémantique (embeddings) dans les notes.

**Request**
```json
{ "query": "habitudes productivité" }
```

**Response 200**
```json
{
  "results": [
    {
      "id":      1711234567890,
      "content": "Lire le livre Atomic Habits ce weekend",
      "score":   0.92,
      "aiResult": {
        "type":     "task",
        "summary":  "Lecture planifiée",
        "keywords": ["lecture", "habits"]
      }
    }
  ]
}
```

---

## Headers CORS requis
Le backend doit autoriser les appels depuis `http://localhost:3000` (frontend React) :

```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## Types de notes reconnus par le front

| Type       | Description              |
|------------|--------------------------|
| `task`     | Tâche à faire            |
| `idea`     | Idée ou brainstorming    |
| `reminder` | Rappel ou deadline       |
| `resource` | Lien, article, ressource |
| `other`    | Autre / non classifié    |
