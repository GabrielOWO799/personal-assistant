# QMD Memory Management

## Memory Hierarchy

### 1. Working Memory (SESSION-STATE.md)
- Active task context
- Current conversation state  
- Temporary variables and decisions
- Updated in real-time with WAL protocol

### 2. Daily Memory (memory/YYYY-MM-DD.md)
- Raw session logs
- Daily events and interactions
- Unprocessed memories
- Created automatically each day

### 3. Long-term Memory (MEMORY.md)
- Curated knowledge
- User preferences and personality
- Important decisions and lessons
- Distilled from daily memories

### 4. Knowledge Base (skills/, references/)
- External knowledge sources
- Skill documentation
- Reference materials
- Domain-specific information

## Memory Search Protocol

### Step 1: Semantic Search
```bash
memory_search("query")
```
- Searches MEMORY.md + memory/*.md
- Returns top relevant snippets
- Uses vector similarity matching

### Step 2: Contextual Filtering
- Filter results by recency
- Prioritize verified information
- Exclude outdated content

### Step 3: Memory Retrieval
```bash
memory_get(path, from, lines)
```
- Fetch specific memory segments
- Keep context window efficient
- Only retrieve what's needed

## Memory Update Rules

### When to Write to Memory
- User corrections ("Actually...", "No, I meant...")
- Important decisions ("Let's do X")
- Preferences ("I like Y", "Don't use Z")
- Proper nouns (names, places, products)
- Specific values (numbers, dates, URLs)

### Memory Quality Guidelines
- Be specific, not vague
- Include context and timestamp
- Verify before committing to long-term memory
- Regular cleanup of outdated information

## QMD Integration Points

### Query Processing
- Before responding, check memory for relevant context
- Use semantic search to find related past interactions
- Apply user preferences from MEMORY.md

### Document Access
- Load relevant skill documentation
- Reference external knowledge when needed
- Cross-reference multiple sources for accuracy

### Memory Maintenance
- Daily cleanup of working memory
- Weekly distillation to long-term memory
- Monthly archive of processed memories