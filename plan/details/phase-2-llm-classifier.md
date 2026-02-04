# Task 2.2: Implement LLM-Based Classifier with Azure OpenAI

**Phase:** 2 - Categorization Engine
**Estimated Time:** 1 day
**Dependencies:** Azure OpenAI resource provisioned

---

## Description

Implement an LLM-based classifier using Azure OpenAI (GPT-4o-mini) to categorize meetings that are ambiguous or don't match clear rule-based patterns. This provides flexible, context-aware classification.

---

## Acceptance Criteria

### LLM Classifier Module Created

- [ ] `src/magic_umbrella/categorization/llm_classifier.py` created
- [ ] `LLMClassifier` class implemented
- [ ] Azure OpenAI client integrated

### Core Functionality

- [ ] Generate classification prompt with meeting context
- [ ] Include known customers/projects in prompt
- [ ] Request structured JSON response
- [ ] Parse LLM response into `MeetingClassification` object
- [ ] Handle API errors gracefully
- [ ] Implement retry logic with exponential backoff

### Prompt Engineering

- [ ] Prompt includes clear classification instructions
- [ ] Known customers list provided for few-shot learning
- [ ] Known projects list provided
- [ ] Meeting type categories clearly defined
- [ ] Request confidence score and reasoning
- [ ] Temperature set to 0.1 for consistency

### Response Parsing

- [ ] JSON response validated against schema
- [ ] Handle malformed JSON responses
- [ ] Extract customer, project, type, confidence, reasoning
- [ ] Default values for missing fields
- [ ] Source marked as "llm"

### Performance & Cost

- [ ] Token usage optimized (truncate long bodies)
- [ ] Cost tracking implemented
- [ ] Response cached for repeated calls (optional)
- [ ] Timeout set appropriately (30 seconds)

### Security

- [ ] API key loaded from environment variable
- [ ] Sensitive meeting data sanitized before sending
- [ ] Attendee emails anonymized (optional)
- [ ] API endpoint configurable

---

## Implementation Details

### Class Structure

```python
# src/magic_umbrella/categorization/llm_classifier.py

from openai import AzureOpenAI
from typing import Optional
import json
import os

class LLMClassifier:
    """LLM-based meeting classifier using Azure OpenAI."""

    def __init__(
        self,
        config_loader,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        model: str = "gpt-4o-mini"
    ):
        """Initialize LLM classifier."""
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.model = model

        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version="2024-02-01",
            azure_endpoint=self.endpoint
        )

        self.customers = config_loader.get_customers()
        self.projects = config_loader.get_projects()

    def classify(
        self,
        subject: str,
        body: str,
        attendees: list[str],
        categories: list[str]
    ) -> MeetingClassification:
        """Classify meeting using LLM."""
        prompt = self._build_prompt(subject, body, attendees, categories)
        response = self._call_llm(prompt)
        return self._parse_response(response)

    def _build_prompt(
        self,
        subject: str,
        body: str,
        attendees: list[str],
        categories: list[str]
    ) -> str:
        """Build classification prompt."""
        pass

    def _call_llm(self, prompt: str) -> str:
        """Call Azure OpenAI API."""
        pass

    def _parse_response(self, response: str) -> MeetingClassification:
        """Parse LLM JSON response."""
        pass

    def _sanitize_body(self, body: str, max_chars: int = 500) -> str:
        """Truncate and sanitize meeting body."""
        return body[:max_chars] if body else ""

    def _anonymize_attendees(self, attendees: list[str]) -> list[str]:
        """Optionally anonymize attendee emails."""
        # Keep domains but anonymize names: john@contoso.com -> ***@contoso.com
        pass
```

### Prompt Template

```python
CLASSIFICATION_PROMPT = """Analyze this calendar meeting and categorize it.

Meeting Title: {subject}
Description: {body_preview}
Attendees: {attendee_count} people
Outlook Categories: {categories}

Known Customers:
{customer_list}

Known Projects:
{project_list}

Meeting Types:
- Customer Meeting: External meeting with a customer
- Internal Project: Internal work on a specific project
- 1:1 Meeting: One-on-one with colleague
- Team Meeting: Team sync, standup, all-hands
- Administrative: HR, expenses, admin tasks
- Training: Learning, workshops, courses
- Uncategorized: Cannot be determined

Return JSON with:
{{
  "customer": "Customer name from list above or null",
  "project": "Project name from list above or null",
  "meeting_type": "One of the types above",
  "confidence": 0.0 to 1.0,
  "reasoning": "Brief explanation (1-2 sentences)"
}}

Be conservative with confidence scores. Use 0.9+ only for very clear cases.
"""
```

### API Call Configuration

```python
response = self.client.chat.completions.create(
    model=self.model,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that categorizes calendar meetings."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    response_format={"type": "json_object"},
    temperature=0.1,  # Low temperature for consistency
    max_tokens=200,   # Short responses only
    timeout=30
)
```

### Response Schema

```json
{
  "customer": "Contoso" | null,
  "project": "Project Alpha" | null,
  "meeting_type": "Customer Meeting",
  "confidence": 0.85,
  "reasoning": "Meeting title mentions Contoso and has external attendees."
}
```

---

## Error Handling

### API Errors to Handle

- [ ] Network timeout
- [ ] Rate limiting (429 status)
- [ ] Invalid API key (401 status)
- [ ] Malformed JSON response
- [ ] Missing required fields in response
- [ ] Quota exceeded

### Retry Strategy

```python
def _call_llm_with_retry(self, prompt: str, max_retries: int = 3) -> str:
    """Call LLM with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            return self._call_llm(prompt)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            time.sleep(wait_time)
```

---

## Cost Optimization

### Token Usage Estimation

```
Prompt components:
- Template: ~200 tokens
- Customer list (10 customers): ~50 tokens
- Project list (10 projects): ~50 tokens
- Meeting title: ~10 tokens
- Meeting body (truncated): ~100 tokens
- Response: ~50 tokens
Total: ~460 tokens per meeting
```

### Cost Calculation

```
GPT-4o-mini pricing:
- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens

For 50 meetings/week:
- Input: 50 × 400 = 20,000 tokens = $0.003
- Output: 50 × 50 = 2,500 tokens = $0.0015
- Total: $0.0045/week = $0.23/year
```

---

## Testing Checklist

- [ ] Test with clear customer meeting
- [ ] Test with ambiguous title
- [ ] Test with long body (truncation)
- [ ] Test with empty body
- [ ] Test with no attendees
- [ ] Test API error handling
- [ ] Test malformed JSON response
- [ ] Test rate limiting
- [ ] Verify token usage is reasonable
- [ ] Verify confidence scores make sense

---

## References

- Research Document: [research/initial-research.md](../../research/initial-research.md) (Lines 325-391)
- Cost Estimation: [research/initial-research.md](../../research/initial-research.md) (Lines 388-390)
- Prompt Example: [research/initial-research.md](../../research/initial-research.md) (Lines 340-375)

---

## Validation Steps

1. Set up Azure OpenAI resource
2. Configure API key in `.env`
3. Test classification with sample meetings
4. Verify JSON responses are valid
5. Check classification accuracy vs. ground truth
6. Monitor token usage in Azure portal
