# Content Moderation Service

AI-powered content moderation service for Vietnamese text using PhoBERT.

## Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run service
python main.py
```

Service will be available at: `http://localhost:8123`

### Docker
```bash
# Build image
docker build -t content-moderation .

# Run container
docker run -p 8123:8123 content-moderation
```

## API Usage

### POST /moderate

Check if content violates community guidelines.

**Request**:
```json
{
  "text": "Nội dung cần kiểm tra",
  "threshold": 0.5
}
```

**Response**:
```json
{
  "label": "valid",
  "prob_invalid": 0.23,
  "threshold": 0.5,
  "latency_ms": 45.32
}
```

**Fields**:
- `label`: "valid" or "invalid"
- `prob_invalid`: Probability (0-1) that content violates policy
- `threshold`: The threshold used for classification
- `latency_ms`: Processing time

### GET /docs

FastAPI interactive documentation (Swagger UI)

## Model

- **Model**: `lamdx4/phobert-vi-moderation`
- **Base**: PhoBERT (Vietnamese BERT)
- **Task**: Binary classification (valid/invalid)
- **Language**: Vietnamese

## Integration

This service is integrated with `tro-tot-vn-be` backend:
- Posts with `prob_invalid >= 0.7` are auto-rejected
- Posts with `prob_invalid < 0.7` go to manual review
- AI score is saved to database for tracking

See `AI_MODERATION_GUIDE.md` for full integration details.
