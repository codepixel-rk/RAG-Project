# Functional Design Document
## PDF Chatbot using Retrieval-Augmented Generation (RAG)

**Project Name:** PDF Chatbot  
**Date:** June 27, 2026  
**Version:** 1.0  
**Status:** Active Development

---

## 1. Executive Summary

This document details the functional specifications and behavioral requirements of the PDF Chatbot system. It defines what the system does, how users interact with it, and the expected outputs for various inputs. The document serves as a bridge between technical architecture and user experience.

---

## 2. System Purpose & Scope

### 2.1 Purpose

The PDF Chatbot enables users to:
- Upload or reference PDF documents
- Ask natural language questions about the document content
- Receive accurate, context-aware answers sourced from the document
- Understand answer provenance through source references

### 2.2 Scope

**Included:**
- Single PDF document processing
- Natural language question answering
- Vector-based semantic search
- Real-time response generation
- Web-based user interface

**Out of Scope (Current Version):**
- Multiple document support
- Document upload functionality
- Chat history persistence
- Multi-user authentication
- Advanced analytics

---

## 3. User Profiles

### 3.1 Primary Users

**Knowledge Seekers**
- Goal: Extract information from documents quickly
- Skill Level: Non-technical
- Frequency: Ad-hoc usage
- Use Case: Research, learning, information discovery

**Business Analysts**
- Goal: Find specific information and trends
- Skill Level: Technical
- Frequency: Regular usage
- Use Case: Data analysis, reporting, insights

**Researchers**
- Goal: Comprehensive document understanding
- Skill Level: Technical
- Frequency: Extended sessions
- Use Case: Literature review, deep analysis

### 3.2 User Scenarios

**Scenario 1: Quick Lookup**
- User: "What is Kafka?"
- System: Returns brief definition with context
- Time: 2-5 seconds

**Scenario 2: Detailed Explanation**
- User: "Explain Kafka architecture and components"
- System: Provides comprehensive explanation
- Time: 5-10 seconds

**Scenario 3: Comparison Query**
- User: "What are the differences between producers and consumers in Kafka?"
- System: Returns comparative analysis
- Time: 3-8 seconds

**Scenario 4: Troubleshooting**
- User: "How do I fix replication lag in Kafka?"
- System: Provides relevant solutions and configurations
- Time: 2-7 seconds

---

## 4. Core Features

### 4.1 Feature List

| Feature | Priority | Status | Description |
|---------|----------|--------|-------------|
| PDF Document Loading | Critical | Implemented | Load and parse PDF files |
| Text Chunking | Critical | Implemented | Split documents into searchable units |
| Vector Embedding | Critical | Implemented | Convert text to embeddings |
| Semantic Search | Critical | Implemented | Find relevant content using vectors |
| Answer Generation | Critical | Implemented | Generate responses using LLM |
| Web Interface | Critical | Implemented | User-friendly question input |
| Response Display | Critical | Implemented | Show answers to users |
| Answer Caching | High | Implemented | Cache repeated queries |
| Model Caching | High | Implemented | Load models once per session |
| Performance Logging | Medium | Implemented | Track execution times |
| Error Handling | High | Not Implemented | Graceful error management |
| Source Citation | High | Not Implemented | Show source references |
| Query History | Medium | Not Implemented | Store user queries |
| Multi-document Support | Medium | Planned | Support multiple PDFs |
| Document Upload | Medium | Planned | Allow user uploads |

### 4.2 Feature Descriptions

#### 4.2.1 PDF Document Loading

**Functionality:**
- Load PDF file from specified path
- Extract text content from all pages
- Preserve document structure metadata
- Handle multi-page documents

**Input:**
- PDF file path: `G:\AI Project\pdf-chatbot\data\Kafka.pdf`

**Output:**
- List of document pages with content
- Metadata: number of pages, total content length

**Example:**
```
Input: "Kafka.pdf" (500 pages)
Output: 500 pages with text content extracted
```

#### 4.2.2 Text Chunking

**Functionality:**
- Split documents into optimal chunks
- Maintain context with overlapping text
- Preserve paragraph boundaries when possible
- Generate chunk boundaries

**Parameters:**
- Chunk Size: 1000 characters
- Overlap: 200 characters

**Output:**
- List of text chunks with metadata

**Example:**
```
Input: 500-page document
Output: 450 chunks of ~1000 chars each with 200 char overlap
```

#### 4.2.3 Vector Embedding

**Functionality:**
- Convert text chunks to numerical vectors
- Generate 384-dimensional embeddings
- Normalize vectors for comparison
- Store embeddings efficiently

**Model:**
- `sentence-transformers/all-MiniLM-L6-v2`
- Output: 384-dimensional vectors

**Example:**
```
Input: "What is Kafka?"
Output: [0.21, 0.44, 0.55, ..., 0.99] (384 dimensions)
```

#### 4.2.4 Semantic Search

**Functionality:**
- Convert user question to embedding
- Calculate similarity to chunk embeddings
- Return top-k most relevant chunks
- Rank results by relevance

**Parameters:**
- k (number of results): 3

**Output:**
- Top 3 most relevant document chunks
- Similarity scores

**Example:**
```
Input: "What is Kafka?"
Output: [
  {chunk: "Kafka is a distributed...", score: 0.87},
  {chunk: "Apache Kafka is used for...", score: 0.85},
  {chunk: "Kafka provides...", score: 0.82}
]
```

#### 4.2.5 Answer Generation

**Functionality:**
- Combine retrieved documents and question into prompt
- Send to LLM for processing
- Generate natural language response
- Return complete answer to user

**Model:**
- Ollama llama3 (local LLM)
- Context window: Model-dependent

**Prompt Template:**
```
Context: [Retrieved document chunks]
Question: [User question]
Answer: [Generated response]
```

**Output:**
- Natural language answer
- Generation time

**Example:**
```
Input: 
  Context: "Kafka is a distributed event streaming platform..."
  Question: "What is Kafka?"
Output: "Kafka is a distributed event streaming platform developed 
         by Apache. It is designed for handling real-time data feeds 
         with high throughput and low latency..."
```

#### 4.2.6 Web User Interface

**Functionality:**
- Display application title and description
- Accept user questions via text input
- Trigger search and generation on button click
- Display loading indicator during processing
- Show results to user
- Maintain session state

**Components:**
- Page configuration (title, icon)
- Title heading with emoji
- Instructions text
- Question input field
- Ask button
- Loading spinner
- Success message
- Answer display

**Example Flow:**
```
User Interface
    |
    v
[Enter Question] -> [Ask Button] -> [Loading...] -> [Display Answer]
```

#### 4.2.7 Answer Caching

**Functionality:**
- Store previously generated answers
- Return cached answer for repeated questions
- Reduce computation time
- Improve user experience

**Implementation:**
- Streamlit session state caching
- Decorator: `@st.cache_data`

**Example:**
```
First Query: "What is Kafka?"
  - No cache hit
  - Compute: ~5-10 seconds
  
Second Query: "What is Kafka?"
  - Cache hit
  - Return: ~0.1 seconds
```

#### 4.2.8 Model Caching

**Functionality:**
- Load embedding model once per session
- Load FAISS database once per session
- Load LLM once per session
- Avoid redundant model initialization

**Implementation:**
- Streamlit resource caching
- Decorator: `@st.cache_resource`

**Benefit:**
```
Session Start: Load models (~30 seconds)
First Query:  Use cached models (~2 seconds)
Subsequent:   Use cached models (~2 seconds each)
```

---

## 5. User Workflows

### 5.1 Main Workflow: Ask a Question

**Workflow Name:** User Question-Answering

**Actors:**
- End User (asks questions)
- PDF Chatbot System (processes and responds)

**Preconditions:**
- System is running
- PDF document is loaded and indexed
- Models are loaded in memory

**Main Flow:**

1. User opens web application
2. User sees interface with input field
3. User types question in text input
4. User clicks "Ask" button
5. System validates question (non-empty)
6. System displays loading spinner
7. System retrieves relevant documents
8. System generates answer using LLM
9. System caches question and answer
10. System displays answer to user
11. User reads answer
12. User can ask follow-up question (loop to step 3)

**Postconditions:**
- User receives answer
- Answer is cached for future reference
- Session state is updated

**Alternate Flows:**

**A1: Empty Question**
- If user clicks Ask with empty question
- System does not process
- No loading spinner shown
- No answer displayed

**A2: Repeated Question**
- If user asks same question again
- System retrieves from cache
- Answer displayed immediately
- No LLM call needed

**A3: Network/System Error**
- If LLM is unavailable
- Error message displayed
- User prompted to retry

**Business Rules:**
- Only non-empty questions are processed
- Maximum question length: 5000 characters
- Answers generated within 10 second timeout
- Top 3 document chunks used for context

**Example:**

```
User: "What is Kafka?"

System Processing:
1. Convert question to embedding: [0.21, 0.44, ...]
2. Search FAISS: Find top 3 chunks
3. Build context: "Kafka is a distributed...
                   Apache Kafka provides...
                   Kafka is used for..."
4. Generate answer: "Kafka is a distributed event 
                     streaming platform..."
5. Display answer

User sees: "Answer: Kafka is a distributed event 
            streaming platform designed for handling 
            real-time data feeds..."
```

### 5.2 Data Processing Workflow: Ingest PDF

**Workflow Name:** Document Ingestion

**Actors:**
- Administrator (initiates)
- Ingestion System (processes)

**Preconditions:**
- PDF file exists at specified path
- Sufficient disk space for vectorstore
- HuggingFace models available

**Main Flow:**

1. Administrator runs `ingest.py`
2. System authenticates with HuggingFace
3. System loads PDF file
4. System extracts pages and content
5. System logs loading time and page count
6. System splits content into chunks
7. System logs chunk count and split time
8. System loads embedding model
9. System generates vectors for all chunks
10. System logs embedding time
11. System creates FAISS database
12. System saves database to disk
13. System logs success message and total time

**Postconditions:**
- FAISS vectorstore created and saved
- Document is ready for querying
- Performance metrics logged

**Example:**

```
Administrator: python ingest.py

System Output:
Loading PDF...time taken 2.45
Pages Loaded: 500
Chunks Created: 447
Splitting Documents time taken... 1.23
Generating embeddings...
Generating embeddings time taken... 8.90
Creating FAISS database...
Vector DB Saved Successfully
Creating FAISS database time taken... 3.45
```

---

## 6. Data Flow Specifications

### 6.1 Question Processing Data Flow

```
User Question
    |
    v
[Validation] --> Check non-empty
    |
    v [Valid]
[Embedding Generation] --> Convert to vector (384-dim)
    |
    v
[FAISS Search] --> Similarity search (k=3)
    |
    v
[Document Retrieval] --> Extract top 3 chunks
    |
    v
[Context Building] --> Concatenate documents
    |
    v
[Prompt Construction] --> Question + Context
    |
    v
[LLM Generation] --> Call llama3 model
    |
    v
[Answer Output] --> Display result to user
    |
    v
[Caching] --> Store question + answer
    |
    v
User Response
```

### 6.2 Document Ingestion Data Flow

```
PDF File (Kafka.pdf)
    |
    v
[PyPDFLoader] --> Extract pages
    |
    v
Document Pages (500 pages)
    |
    v
[RecursiveCharacterTextSplitter]
    |  (chunk_size=1000, overlap=200)
    v
Document Chunks (447 chunks)
    |
    v
[HuggingFaceEmbeddings]
    |  (all-MiniLM-L6-v2)
    v
Embedding Vectors (447 x 384)
    |
    v
[FAISS.from_documents]
    |
    v
FAISS Index
    |
    v
[db.save_local("vectorstore")]
    |
    v
Persisted Vector Store (index.faiss, index.pkl, docstore.pkl)
```

---

## 7. Business Rules & Constraints

### 7.1 Data Processing Rules

| Rule | Description | Enforcement |
|------|-------------|------------|
| R1 | Chunk size must be 1000 characters | Code constant |
| R2 | Chunk overlap must be 200 characters | Code constant |
| R3 | Top k results = 3 documents | Code constant |
| R4 | Embedding model = all-MiniLM-L6-v2 | Configuration |
| R5 | LLM model = llama3 | Configuration |
| R6 | Questions must be non-empty | UI validation |
| R7 | Max question length = 5000 characters | Code validation |
| R8 | FAISS index must be serializable | Code requirement |

### 7.2 Performance Rules

| Rule | Description | Target |
|------|-------------|--------|
| P1 | Question-to-answer time | <10 seconds |
| P2 | Cached query time | <1 second |
| P3 | Model loading time | <30 seconds |
| P4 | PDF loading time | <5 seconds |
| P5 | Embedding generation time | <1 second per query |
| P6 | FAISS search time | <100ms |

### 7.3 Quality Rules

| Rule | Description | Verification |
|------|-------------|--------------|
| Q1 | Retrieved documents must be relevant | Manual testing |
| Q2 | Answers must be factually accurate | Source documents |
| Q3 | Answers must be complete | User feedback |
| Q4 | Response must be natural language | LLM quality |
| Q5 | No hallucinated information | RAG verification |

---

## 8. System Behavior Specifications

### 8.1 Input Specifications

#### 8.1.1 User Question Input

**Input Type:** Text String

**Format:**
- Plain text
- Natural language English
- May contain special characters
- May contain domain-specific terminology

**Validation Rules:**
- Non-empty (required)
- Length: 1-5000 characters
- No null values
- No binary content

**Valid Examples:**
```
"What is Kafka?"
"Explain the architecture of Kafka including producers and consumers"
"How do I configure Kafka for high throughput?"
"What are the differences between RabbitMQ and Kafka?"
```

**Invalid Examples:**
```
"" (empty)
"a" (too short is allowed, but empty not)
"\x00\x01\x02" (binary)
NULL (null value)
```

#### 8.1.2 PDF Document Input

**Input Type:** File

**Format:**
- PDF (.pdf extension)
- Binary PDF format
- Single file
- Any number of pages

**Validation Rules:**
- Must exist at specified path
- Must be readable
- Must be valid PDF structure
- Must contain extractable text

**Valid Location:**
```
G:\AI Project\pdf-chatbot\data\Kafka.pdf
```

### 8.2 Output Specifications

#### 8.2.1 Answer Output

**Output Type:** Text String

**Format:**
- Plain text
- Natural language English
- May span multiple paragraphs
- Generated by LLM

**Content Requirements:**
- Answers user's question directly
- Sourced from document content
- Factually accurate
- Complete and coherent

**Structure:**
```
[Direct answer to question]
[Supporting details]
[Context or examples]
[Related information if relevant]
```

**Example Output:**
```
"Kafka is a distributed event streaming platform developed 
by the Apache Software Foundation. It is designed to handle 
real-time data feeds with high throughput and low latency. 

Kafka works by organizing data into topics, which are further 
divided into partitions for parallel processing. Producers 
send messages to topics, while consumers read messages from 
these topics.

The key benefits of Kafka include:
- High throughput for processing millions of messages per second
- Fault tolerance through replication
- Scalability through partitioning
- Durability through persistent storage"
```

#### 8.2.2 Cache Storage

**Output Type:** Session State Dictionary

**Format:**
```python
{
    "question": "What is Kafka?",
    "answer": "Kafka is a distributed event streaming platform...",
    "timestamp": 1719525600
}
```

**Purpose:**
- Avoid recomputation
- Improve response time
- Track user session data

### 8.3 State Management

#### 8.3.1 Session State Variables

| Variable | Type | Purpose | Scope |
|----------|------|---------|-------|
| session.answer | string | Store last answer | Session |
| cached_embeddings | object | Cache loaded models | Session |
| cached_db | object | Cache FAISS DB | Session |
| cached_llm | object | Cache LLM model | Session |

#### 8.3.2 State Transitions

```
Initial State
    |
    v
[User Opens App] -> Session created, answer = ""
    |
    v
[User Asks Question] -> answer = processing
    |
    v
[System Retrieves] -> answer = retrieved_docs
    |
    v
[LLM Generates] -> answer = generated_response
    |
    v
[Display Answer] -> answer shown to user
    |
    v
[User Asks Again] -> answer = new_response
    |
    v (if same question)
[Cache Hit] -> answer = cached_response (instant)
```

---

## 9. Functional Requirements

### 9.1 FR: Document Processing

**ID:** FR-DOC-001  
**Title:** PDF Document Loading  
**Description:** System shall load PDF documents and extract text content

**Requirements:**
- Load file from specified path
- Extract all pages
- Preserve content order
- Handle multi-page documents
- Log loading statistics

**Acceptance Criteria:**
- Can load 500+ page documents
- Extracts 100% of text content
- Completes in <5 seconds
- Logs page count

**Status:** Implemented

---

**ID:** FR-DOC-002  
**Title:** Text Chunking  
**Description:** System shall split documents into contextual chunks

**Requirements:**
- Create chunks of 1000 characters
- Maintain 200 character overlap
- Preserve semantic meaning
- Generate unique identifiers

**Acceptance Criteria:**
- Creates chunks with specified size
- Overlap correctly applied
- Chunk count logged
- Process time tracked

**Status:** Implemented

---

**ID:** FR-DOC-003  
**Title:** Vector Embedding Generation  
**Description:** System shall convert text to embeddings

**Requirements:**
- Use all-MiniLM-L6-v2 model
- Generate 384-dimensional vectors
- Normalize embeddings
- Store efficiently

**Acceptance Criteria:**
- All chunks vectorized
- Embedding dimensions correct
- Process time logged
- FAISS DB created successfully

**Status:** Implemented

---

### 9.2 FR: Question Answering

**ID:** FR-QA-001  
**Title:** Semantic Document Search  
**Description:** System shall retrieve relevant documents using semantic search

**Requirements:**
- Convert question to embedding
- Search FAISS index
- Return top 3 results
- Rank by relevance score

**Acceptance Criteria:**
- Retrieves relevant documents
- Top 3 results returned
- Search completes in <100ms
- Results ranked properly

**Status:** Implemented

---

**ID:** FR-QA-002  
**Title:** Answer Generation  
**Description:** System shall generate natural language answers

**Requirements:**
- Use retrieved documents as context
- Call LLM for generation
- Generate complete answers
- Ensure factual accuracy

**Acceptance Criteria:**
- Answers generated from context
- No hallucinated content
- Completes in <10 seconds
- Grammar and coherence verified

**Status:** Implemented

---

**ID:** FR-QA-003  
**Title:** Question Validation  
**Description:** System shall validate user questions

**Requirements:**
- Reject empty questions
- Enforce character limits
- Sanitize input
- Display error messages

**Acceptance Criteria:**
- Empty questions rejected
- Max length enforced
- Clear error messages
- No system errors

**Status:** Implemented (Basic)

---

### 9.3 FR: User Interface

**ID:** FR-UI-001  
**Title:** Question Input  
**Description:** System shall provide input field for user questions

**Requirements:**
- Display text input field
- Show placeholder text
- Support standard text input
- Clear on submit

**Acceptance Criteria:**
- Input field visible
- Accepts user text
- Placeholder text displays
- Keyboard input works

**Status:** Implemented

---

**ID:** FR-UI-002  
**Title:** Answer Display  
**Description:** System shall display answers to users

**Requirements:**
- Show answer text
- Format for readability
- Display success indicator
- Preserve formatting

**Acceptance Criteria:**
- Answer displays correctly
- Formatting preserved
- Success message shown
- Text is readable

**Status:** Implemented

---

**ID:** FR-UI-003  
**Title:** Loading Indicator  
**Description:** System shall show loading status during processing

**Requirements:**
- Display spinner during processing
- Show progress message
- Hide when complete
- Clear user feedback

**Acceptance Criteria:**
- Spinner appears during processing
- Message is clear
- Spinner disappears on completion
- No visual glitches

**Status:** Implemented

---

### 9.4 FR: Performance

**ID:** FR-PERF-001  
**Title:** Response Caching  
**Description:** System shall cache responses to repeated queries

**Requirements:**
- Cache question-answer pairs
- Return cached results instantly
- Reduce computation

**Acceptance Criteria:**
- Cached queries return in <1 second
- Cache hit rate tracked
- No stale data returned

**Status:** Implemented

---

**ID:** FR-PERF-002  
**Title:** Model Caching  
**Description:** System shall cache loaded models for session

**Requirements:**
- Load models once per session
- Reuse for all queries
- Reduce startup time

**Acceptance Criteria:**
- Models load once
- All queries use cached models
- Session persistence verified

**Status:** Implemented

---

## 10. Non-Functional Requirements

### 10.1 Performance Requirements

| Requirement | Target | Priority |
|-------------|--------|----------|
| Page Load Time | <2 seconds | High |
| First Query Time | <15 seconds (incl. model loading) | High |
| Cached Query Time | <1 second | High |
| Search Retrieval Time | <100ms | Medium |
| LLM Generation Time | <10 seconds | High |
| Model Memory Usage | <4GB | High |

### 10.2 Reliability Requirements

| Requirement | Target | Priority |
|-------------|--------|----------|
| System Availability | 99% uptime | High |
| Question Validation Rate | 100% | Critical |
| Answer Generation Success Rate | 95%+ | High |
| Cache Hit Rate | 40%+ for typical usage | Medium |

### 10.3 Usability Requirements

| Requirement | Description | Priority |
|-------------|-------------|----------|
| Ease of Use | Single-click question submission | Critical |
| Clarity | Answer should be understandable | High |
| Response Time | User feedback within 10 seconds | High |
| Error Messages | Clear, actionable error messages | High |

### 10.4 Security Requirements

| Requirement | Description | Priority |
|-------------|-------------|----------|
| Token Storage | Secure HF_TOKEN handling | High |
| Data Privacy | Local processing only | Critical |
| Input Validation | Sanitized inputs | Medium |
| Error Messages | No sensitive info exposed | Medium |

### 10.5 Scalability Requirements

| Requirement | Description | Priority |
|-------------|-------------|----------|
| Document Size | Support up to 1000 pages | High |
| Concurrent Users | Support 5+ concurrent sessions | Medium |
| Query Volume | Handle 100+ queries per session | Medium |
| Vector Index | Support 10,000+ vectors | Medium |

---

## 11. Error Handling

### 11.1 Error Scenarios

#### 11.1.1 PDF Loading Errors

**Scenario:** PDF file not found

**Trigger:**
```python
PyPDFLoader("invalid_path.pdf")
```

**Current Behavior:**
- Runtime error
- Application crashes
- User sees error stack trace

**Expected Behavior:**
- Graceful error message
- User-friendly error display
- Recovery option

**Resolution:**
- Add file existence check
- Display error modal
- Suggest corrective action

---

#### 11.1.2 Model Loading Errors

**Scenario:** HuggingFace models unavailable

**Trigger:**
- Network connectivity issue
- Model download failure
- Disk space insufficient

**Current Behavior:**
- Download error
- Application hangs
- User frustrated

**Expected Behavior:**
- Timeout after 30 seconds
- Error message displayed
- Retry option provided

**Resolution:**
- Implement timeout
- Add retry logic
- Cache offline models

---

#### 11.1.3 LLM Generation Errors

**Scenario:** Ollama server unavailable

**Trigger:**
- Ollama not running
- Network connectivity issue
- Model not loaded

**Current Behavior:**
- Connection error
- Blank response
- No error message

**Expected Behavior:**
- Clear error message
- Suggestion to restart Ollama
- Retry option

**Resolution:**
- Add connection check
- Display helpful message
- Implement retry mechanism

---

#### 11.1.4 FAISS Index Errors

**Scenario:** Corrupted vector store

**Trigger:**
- Incomplete vectorstore save
- File corruption
- Version mismatch

**Current Behavior:**
- Deserialization error
- Application crash

**Expected Behavior:**
- Error notification
- Regeneration option

**Resolution:**
- Add index validation
- Implement fallback mechanism
- Provide regeneration option

---

### 11.2 Error Handling Strategy

| Error Type | Severity | Handling | User Message |
|------------|----------|----------|--------------|
| Invalid Question | Low | Skip processing | "Please enter a question" |
| PDF Not Found | High | Fail gracefully | "Document not found" |
| Model Unavailable | Critical | Retry/timeout | "Model loading... please wait" |
| LLM Offline | Critical | Show error | "Answer generation unavailable" |
| Empty Result | Medium | Default response | "No relevant content found" |

---

## 12. Test Cases

### 12.1 Functional Test Cases

**TC-QA-001: Simple Question**

| Aspect | Value |
|--------|-------|
| Input | "What is Kafka?" |
| Expected Output | Definition of Kafka with context |
| Acceptance | Answer contains "Kafka" and "distributed" |
| Status | Pass |

---

**TC-QA-002: Complex Question**

| Aspect | Value |
|--------|-------|
| Input | "Explain Kafka architecture with producers and consumers" |
| Expected Output | Detailed architectural explanation |
| Acceptance | Answer covers producers, consumers, and architecture |
| Status | Pass |

---

**TC-QA-003: Repeated Question (Cache)**

| Aspect | Value |
|--------|-------|
| Input | Same question asked twice |
| Expected Output | Instant response on second query |
| Acceptance | Response time <1 second |
| Status | Pass |

---

**TC-UI-001: Empty Question**

| Aspect | Value |
|--------|-------|
| Input | Click "Ask" with empty field |
| Expected Output | No processing, no answer displayed |
| Acceptance | System doesn't hang, no error shown |
| Status | Pass |

---

**TC-PERF-001: Model Loading**

| Aspect | Value |
|--------|-------|
| Test | First app load |
| Expected | Models load within 30 seconds |
| Acceptance | Embeddings + DB + LLM ready |
| Status | Pass |

---

**TC-PERF-002: Query Response**

| Aspect | Value |
|--------|-------|
| Test | Full question-to-answer cycle |
| Expected | Complete in <10 seconds |
| Acceptance | Answer displayed within timeout |
| Status | Pass |

---

## 13. Integration Points

### 13.1 External Systems

| System | Integration | Purpose |
|--------|-----------|---------|
| HuggingFace | API via Token | Download embedding models |
| Ollama | Local Server | LLM inference |
| FAISS | Python Library | Vector search |
| Streamlit | Framework | Web UI |
| LangChain | Library | Document processing |

### 13.2 Data Interfaces

**PDF Input:**
```
File: Kafka.pdf (local filesystem)
Format: Binary PDF
Loader: PyPDFLoader
```

**Vector Store:**
```
Location: vectorstore/ directory
Format: FAISS index + metadata
Access: FAISS.load_local()
```

**Model Cache:**
```
Location: .cache/ directory
Format: PyTorch/Hugging Face format
Access: HuggingFaceEmbeddings()
```

---

## 14. Assumptions & Constraints

### 14.1 Assumptions

| Assumption | Implication |
|-----------|------------|
| Ollama server running locally | User responsible for Ollama setup |
| HF_TOKEN available | User must set environment variable |
| PDF at fixed location | Limited flexibility for documents |
| Single document only | Can't query multiple PDFs |
| English language documents | May not work with other languages |
| Sufficient disk space | ~1GB for models + vectorstore |
| 8GB+ RAM available | Required for model execution |

### 14.2 Constraints

| Constraint | Impact |
|-----------|--------|
| Single PDF document | Must re-ingest for new document |
| No API authentication | Only for local use |
| Fixed chunk size | May lose context in large tables |
| No chat history | Can't track conversation |
| No source citations | Users don't know answer origin |
| No user management | Single user implied |
| No persistence | Chat lost on session end |

---

## 15. Future Functional Enhancements

### 15.1 Short Term (1-2 months)

**FE-001: Multi-Document Support**
- Load multiple PDFs
- Cross-document search
- Document selection UI
- Combined indexing

**FE-002: Source Citations**
- Track answer sources
- Display page numbers
- Highlight source text
- Citation formatting

**FE-003: Chat History**
- Store conversation history
- Previous query browsing
- Context continuity
- Export conversations

**FE-004: Error Recovery**
- Graceful error handling
- User-friendly messages
- Automatic retries
- Recovery suggestions

### 15.2 Medium Term (2-4 months)

**FE-005: Document Upload**
- Allow users to upload PDFs
- Processing queue
- Status tracking
- Upload validation

**FE-006: Advanced Search**
- Hybrid search (semantic + keyword)
- Filters and facets
- Query expansion
- Result ranking

**FE-007: Answer Refinement**
- Follow-up questions
- Answer clarification
- Related topics
- Confidence scoring

**FE-008: User Preferences**
- Answer length control
- Language selection
- Detail level preference
- Display themes

### 15.3 Long Term (4+ months)

**FE-009: Analytics Dashboard**
- Query analytics
- Popular questions
- Usage patterns
- Performance metrics

**FE-010: Collaborative Features**
- User authentication
- Multi-user support
- Question sharing
- Comments/annotations

**FE-011: Advanced RAG**
- Reranking models
- Query expansion
- Hybrid retrieval
- Multi-hop reasoning

**FE-012: Mobile App**
- Mobile UI
- Responsive design
- Offline support
- Native app option

---

## 16. Success Metrics

### 16.1 Functional Success Metrics

| Metric | Target | Measurement |
|--------|--------|------------|
| Question Processing Rate | 100% | Processed/Submitted |
| Answer Accuracy | 90%+ | Manual review |
| Cache Hit Rate | 40%+ | Cached/Total queries |
| System Uptime | 99%+ | Minutes available/total |
| Response Completeness | 95%+ | Full answers/total |

### 16.2 Performance Success Metrics

| Metric | Target | Measurement |
|--------|--------|------------|
| Page Load Time | <2 seconds | Time to interactive |
| First Query Time | <15 seconds | Time to response |
| Cached Query Time | <1 second | Time to cached response |
| Model Load Time | <30 seconds | Initialization time |
| Avg Query Time | 5-10 seconds | Mean response time |

### 16.3 User Experience Metrics

| Metric | Target | Measurement |
|--------|--------|------------|
| User Satisfaction | 4.5/5 | Survey rating |
| Task Completion Rate | 95%+ | Successful queries |
| Return Rate | 60%+ | Repeat users |
| Question Clarity | High | User feedback |
| Answer Usefulness | 80%+ | User feedback |

---

## 17. Conclusion

This Functional Design Document provides a comprehensive specification of the PDF Chatbot system's capabilities, behavior, and requirements. It serves as the blueprint for development, testing, and user acceptance validation.

The system successfully implements a RAG-based question-answering platform that provides users with an intuitive interface for querying PDF documents. Key features include semantic search, LLM-based answer generation, and performance optimizations through caching.

Future enhancements will expand functionality to support multiple documents, advanced search capabilities, and enterprise features, positioning the system for broader adoption and use cases.

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| RAG | Retrieval-Augmented Generation - combining retrieval with LLM generation |
| Embedding | Numerical vector representation of text |
| FAISS | Facebook AI Similarity Search - vector database |
| LLM | Large Language Model for text generation |
| Semantic Search | Finding content based on meaning, not keywords |
| Chunk | A segment of text from the original document |
| Vectorstore | Database storing and indexing vectors |
| Prompt | Input text sent to LLM for generation |
| Token | Subword unit used by language models |
| Cache | Storing data for fast retrieval |

---

## Appendix B: References

| Document | Purpose |
|----------|---------|
| Technical Design Document | System architecture and components |
| API Documentation | Model and library specifications |
| User Guide | End-user instructions |
| Development Guide | Setup and deployment instructions |

---

**Document Version:** 1.0  
**Last Updated:** June 27, 2026  
**Next Review:** September 27, 2026
