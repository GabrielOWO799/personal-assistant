---
name: url-markdown
description: Convert URLs to markdown format with proper formatting, metadata extraction, and link handling. Use when converting web content to markdown, creating formatted links, or processing URLs for documentation.
---

# URL to Markdown Converter

## Overview

This skill helps convert URLs to properly formatted markdown with extracted metadata, titles, and descriptions. It's useful for creating documentation, blog posts, or any content that needs to reference web resources in a clean, readable format.

## When to Use

- Converting raw URLs to formatted markdown links
- Creating documentation that references web resources
- Processing web content for markdown-based systems
- Generating link lists with proper formatting
- Extracting metadata from URLs for content organization

## Basic Usage

### Simple URL to Markdown Link
```
[Page Title](https://example.com)
```

### URL with Description
```
[Page Title](https://example.com) - Brief description of the content
```

### Formatted Link List
```markdown
- [Title 1](https://example1.com) - Description
- [Title 2](https://example2.com) - Description  
- [Title 3](https://example3.com) - Description
```

## Advanced Features

### Metadata Extraction
When possible, extract:
- Page title
- Description/summary
- Author information
- Publication date
- Content type

### Responsive Formatting
- Auto-detect mobile-friendly vs desktop content
- Handle different content types (articles, videos, images, documents)
- Preserve important formatting elements

### Error Handling
- Handle broken/dead links gracefully
- Provide fallback formatting when metadata is unavailable
- Validate URL structure before processing

## Best Practices

1. **Always verify URLs** before including them
2. **Use descriptive link text** instead of raw URLs
3. **Include context** when the link destination isn't obvious
4. **Group related links** together with appropriate headings
5. **Maintain consistent formatting** throughout your document

## Examples

### Blog Post Reference
```markdown
For more information about AI agents, check out [The Ultimate Guide to AI Agents](https://example.com/ai-agents-guide) by John Smith.
```

### Resource List
```markdown
## Helpful Resources

- [OpenClaw Documentation](https://docs.openclaw.ai) - Official documentation and guides
- [GitHub Repository](https://github.com/openclaw/openclaw) - Source code and issue tracking
- [Community Discord](https://discord.com/invite/clawd) - Community support and discussions
```

### Academic Citation
```markdown
According to recent research [published in Nature](https://nature.com/articles/s41586-023-12345-6), AI agents are becoming increasingly capable of autonomous decision-making.
```