# 🎯 AI Decision & Accountability Auditor
## Project Documentation

---

## 📋 Project Overview

**AI Decision & Accountability Auditor** is an AI-powered tool for accountability that analyzes meeting transcripts to extract key decisions, action items, and dependencies. It provides accountability and traceability by mapping relationships between organizational decisions and assigned tasks.

**Live Tool:** https://patchamomma-frontend-kxd7wnyafa-uc.a.run.app

---

## 🎯 Core Problem Statement

Organizations struggle with:
- **Lost Accountability**: Decisions made in meetings aren't tracked or assigned
- **Orphaned Action Items**: Tasks lack clear ownership or deadlines
- **Hidden Dependencies**: Relationships between decisions and actions aren't visible
- **No Evidence Trail**: Decisions can't be linked back to the exact meeting discussion

**Solution**: Automatically extract, map, and validate all meeting outcomes in seconds.

---

## ✨ Key Features

### 1. **Decision Extraction**
- Identifies all explicit decisions from meeting transcripts
- Assigns confidence scores (0-1.0) based on clarity
- Links decisions to exact transcript quotes
- Captures speaker name and timestamp

### 2. **Action Item Extraction**
- Extracts tasks, TODOs, and assignments
- Identifies:
  - **Owner**: Person responsible
  - **Deadline**: Date/time (converts relative dates like "by Friday")
  - **Priority**: High/Medium/Low
  - **Evidence**: Exact quote from transcript

### 3. **Dependency Mapping**
- Maps relationships between decisions and actions
- Relationship types:
  - `blocks` - Decision prevents action
  - `depends_on` - Action requires decision
  - `conflicts_with` - Decision contradicts action
  - `enables` - Decision enables action

### 4. **Validation & Conflict Detection**
- Detects duplicate decisions/actions
- Identifies missing task owners
- Flags unrealistic deadlines
- Highlights conflicting decisions
- Validates against business rules

### 5. **Result Caching**
- Identical transcripts return instant cached results
- 24-hour TTL for cached analyses
- Reduces API calls and costs

### 6. **Dark Mode Support**
- Full light/dark theme toggle
- Responsive design for all devices

---

## 🏗️ Architecture

### Frontend
- **Framework**: React 18 + Tailwind CSS
- **Deployment**: Google Cloud Run
- **URL**: https://patchamomma-frontend-kxd7wnyafa-uc.a.run.app
- **Features**:
  - Real-time transcript analysis
  - Drag-and-drop file upload
  - JSON download of results
  - Expandable decision cards
  - Filter by priority and search

### Backend API
- **Framework**: FastAPI (Python)
- **Deployment**: Google Cloud Run
- **URL**: https://patchamomma-api-509553055814.us-central1.run.app
- **AI Model**: Google Gemini 3-Flash
- **Features**:
  - REST API with CORS enabled
  - Deterministic extraction (temperature=0)
  - Model fallback (primary + backup)
  - Validation pipeline
  - Result caching

### AI Agents
1. **Decision Extractor** - Identifies decisions from transcripts
2. **Action Extractor** - Extracts action items and assignments
3. **Dependency Mapper** - Maps relationships between decisions/actions
4. **Validators** - Decision & action validation
5. **Conflict Detector** - Identifies contradictions

### Data Models
- `Decision` - Extracted decision with confidence score
- `ActionItem` - Task with owner, deadline, priority
- `Dependency` - Relationship between decisions/actions
- `ValidationResult` - Issues and recommendations

---

## 🚀 How It Works

### User Flow
1. **Upload Transcript**
   - Paste meeting text or upload .txt file
   - Minimum 50 characters required

2. **AI Analysis** (5-15 seconds)
   - Extracts decisions with confidence scores
   - Identifies action items with owners/deadlines
   - Maps dependencies between items
   - Validates for conflicts and issues

3. **View Results**
   - Dashboard shows summary statistics
   - 4 tabs: Decisions, Actions, Dependencies, Validation
   - Expandable cards with evidence/details
   - Filters and search

4. **Download Report**
   - Export full analysis as JSON
   - Includes all decisions, actions, dependencies
   - Validation results and conflict alerts

---

## 📊 Example Analysis

### Input: Meeting Transcript
```
"We decided to implement TLS for all endpoints by Sept 15.
Tom will handle the implementation.
We need Pydantic validation first.
Security clearance is required before launch."
```

### Output:
**Decisions (3)**
- Use TLS for all endpoints (95% confident)
- Implement Pydantic validation (85% confident)
- Require security clearance before launch (90% confident)

**Action Items (2)**
- Tom: Implement TLS (by Sept 15, High Priority)
- Team: Setup Pydantic validation (Medium Priority)

**Dependencies (2)**
- Pydantic validation → TLS implementation
- All security tasks → Security clearance → Launch approval

---

## 🔧 Technical Stack

### Frontend
```
React 18
Tailwind CSS
Lucide Icons
Vite (Build tool)
```

### Backend
```
Python 3.10+
FastAPI
Uvicorn
Pydantic (validation)
Google Generative AI SDK
```

### Cloud Infrastructure
```
Google Cloud Run (Frontend & Backend)
Google Cloud Storage (optional logs)
Environment: us-central1
Containerized deployment with Docker
```

### AI/ML
```
Google Gemini 3-Flash (primary)
Google Gemini Pro (fallback)
Deterministic extraction (temperature=0)
```

---

## 🔐 Security Features

- **Input Validation**: Pydantic models validate all data
- **API Authentication**: Environment-variable protected API keys
- **CORS Enabled**: Secure cross-origin requests
- **No Data Storage**: Transcripts aren't stored (processed & discarded)
- **Temperature=0**: Prevents hallucination/randomness
- **Error Handling**: Graceful fallbacks, no sensitive info leaked

---

## 📈 Performance

- **Average Analysis Time**: 5-15 seconds
- **Transcript Limit**: No hard limit (tested up to 50KB)
- **Concurrent Users**: Scales with Cloud Run auto-scaling
- **Caching Hit Rate**: Identical transcripts (instant response)
- **API Quota**: Uses paid Google Gemini API (no daily limits)

---

## 🎓 Use Cases

1. **Meeting Minutes Automation**
   - Replace manual note-taking
   - Auto-generate action item lists
   - Track decision ownership

2. **Project Management**
   - Sync decisions to JIRA/Asana
   - Assign ownership automatically
   - Track dependencies

3. **Compliance & Audit**
   - Evidence trail for decisions
   - Accountability tracking
   - Conflict detection

4. **Executive Reporting**
   - Summarize decisions by date/participant
   - Priority breakdown
   - Implementation status

5. **Onboarding**
   - New team members understand decisions
   - Clear action item assignments
   - Historical context

---

## 🛣️ Roadmap

### Phase 1 (Current) ✅
- Decision extraction
- Action item extraction
- Dependency mapping
- Basic validation

### Phase 2 (Planned)
- [ ] Database persistence (BigQuery)
- [ ] Multi-user workspaces
- [ ] User authentication
- [ ] Historical tracking
- [ ] Integration APIs (JIRA, Slack, Asana)

### Phase 3 (Future)
- [ ] Natural language follow-ups
- [ ] Predictive timeline analysis
- [ ] Risk assessment AI
- [ ] Meeting transcription integration
- [ ] Voice meeting real-time analysis

---

## 🔗 Links & References

| Resource | Link |
|----------|------|
| **Live App** | https://patchamomma-frontend-kxd7wnyafa-uc.a.run.app |
| **API Endpoint** | https://patchamomma-api-509553055814.us-central1.run.app/analyze |
| **GitHub** | (Add if available) |
| **Documentation** | See PROJECT_DOCUMENTATION.md |

---

## 👥 Team & Contact

**Project Owner:** Gayat Vattipalli  
**Email:** Mohith.Vattipalli@blend360.com  
**Status:** Active Development

---

## 📝 Changelog

### Version 1.0.0 (Current)
- ✅ Decision extraction with Gemini AI
- ✅ Action item extraction with ownership tracking
- ✅ Dependency mapping between decisions/actions
- ✅ Conflict detection and validation
- ✅ Result caching (24-hour TTL)
- ✅ Model fallback (primary + backup)
- ✅ Dark mode support
- ✅ JSON export functionality
- ✅ Responsive React frontend
- ✅ Cloud Run deployment

---

## 📞 Support & Troubleshooting

### Common Issues

**Problem**: "0 decisions extracted"
- **Solution**: Ensure transcript has at least 50 characters and contains clear decisions

**Problem**: "Action items not extracted"
- **Solution**: Make sure action items are explicitly mentioned with owners or verbs like "implement", "create", "setup"

**Problem**: "Timeout errors"
- **Solution**: Try with a shorter transcript; clear browser cache; check API quota

**Problem**: "Dependency not mapped"
- **Solution**: Ensure dependencies are logically related; consider rephrasing for clarity

---

## 📄 License & Usage

This accountability is designed for organizational decision tracking and accountability. All data is processed in real-time and not permanently stored.

---

**Last Updated:** September 8, 2026  
**Version:** 1.0.0  
**Status:** Production Ready ✅
