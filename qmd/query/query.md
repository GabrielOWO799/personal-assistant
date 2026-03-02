# QMD Query Processing

## Query Analysis Framework

### Step 1: Intent Classification
- **Informational**: Seeking knowledge or facts
- **Transactional**: Wanting to perform an action
- **Navigational**: Looking for specific resources
- **Proactive**: Anticipating future needs

### Step 2: Context Requirements
- **Memory Needed**: Does this require personal context?
- **Documents Needed**: Does this require external knowledge?
- **Both**: Requires integration of memory and documents

### Step 3: Response Strategy
- **Direct Answer**: Simple factual response
- **Memory Integration**: Combine personal context with answer
- **Document Reference**: Cite external sources
- **Hybrid Response**: Integrate all three components

## Query Examples

### Informational + Memory
**Query**: "What did I decide about the AI project timeline?"
**Process**: 
1. Search MEMORY.md for "AI project" and "timeline"
2. Extract relevant decisions
3. Provide direct answer with context

### Transactional + Documents  
**Query**: "Install the new skill for web scraping"
**Process**:
1. Check available skills in ClawHub
2. Verify skill safety and compatibility
3. Install and configure
4. Update TOOLS.md with installation notes

### Proactive + Both
**Query**: "What should I work on today?"
**Process**:
1. Check HEARTBEAT.md for pending tasks
2. Review MEMORY.md for recent priorities
3. Suggest tasks based on patterns and goals
4. Offer specific actionable items