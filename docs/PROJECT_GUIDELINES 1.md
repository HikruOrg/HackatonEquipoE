# AI Talent Matcher Project Guide

## Project Overview

**Project Name:** AI Talent Matcher (JD ↔ Resumes)

**Goal:** Rank candidates for a Job Description (JD) with transparent, explainable reasons.

## Core Requirements

### 1. Dual Input Support (PDF and JSON)
- **Input Formats:** 
  - PDF files containing resumes and job descriptions
  - JSON files with structured resume and job description data
- **PDF Processing:** Extract text from PDF files using PDF processing libraries
- **JSON Processing:** Validate and use JSON files directly
- **Storage Integration:** Connect to storage (local or cloud) to retrieve previously stored JSONs
- **Output:** Structured JSON format for analysis

### 2. Resume Preprocessing
- **Input Format:** Text extracted from PDFs OR structured JSON files
- **Processing:** Parse and structure text data into JSON format (if from PDF)
- **Extract:** Skills, experience, education, and other relevant candidate information
- **Structuring:** Use LLM if needed to intelligently structure unstructured text
- **Storage:** Save processed JSONs to storage for future use

### 3. Analysis with LLM
- **Resume Analysis:** Use LLM to analyze resumes against job descriptions
- **JD Analysis:** Process job description requirements
- **LLM Model:** Use OpenAI GPT-4 or GPT-3.5-turbo for analysis
- **Prompts:** Use defined prompts for consistent analysis

### 4. Hybrid Scoring System
- **Similarity Score:** Calculate semantic similarity between JD and resume using LLM analysis
- **Rule-Based Boosts:**
  - **Must-Have Requirements:** Boost score when candidate matches critical JD requirements
  - **Recency:** Boost score based on recent experience or skills
- **Final Score:** Combine similarity score with rule-based boosts

### 5. Explainability & Transparency
- **Reason Codes:** Map scoring hits to specific resume lines/sections
- **Hit Mapping:** Show which parts of the resume matched which JD requirements
- **Transparent Ranking:** Provide clear explanations for each candidate's score

### 6. Export Functionality
- **CSV Export:** Export ranked results with:
  - Candidate rankings
  - Scores (overall and component scores)
  - Must-have requirement hits
  - Reason codes and explanations

## Demo Deliverable

A ranked candidate table displaying:
- **Ranked List:** Candidates sorted by final score
- **Scores:** Overall score and component breakdowns
- **Must-Have Hits:** Which critical requirements each candidate satisfies
- **Reasons:** Transparent explanation of why each candidate received their score
- **CSV Export:** Ability to export the complete ranking table

## Technical Implementation Guidelines

### Data Structure
- **Resume Input:** 
  - PDF files → Text extraction → JSON format with structured content
  - JSON files → Direct validation and use
  - Storage → Retrieve stored JSONs
- **JD Input:** 
  - PDF files → Text extraction → Structured JSON format
  - JSON files → Direct validation and use
  - Storage → Retrieve stored JSONs
- **Output:** Ranked list with scores and explanations

### Scoring Algorithm
```
Final Score = Similarity Score + Must-Have Boost + Recency Boost
```

### Reason Codes
- Map each scoring factor to specific resume sections
- Provide line-level or section-level references
- Explain how each factor contributed to the final score

## Success Criteria

1. ✅ Successfully load data from both PDF and JSON formats
2. ✅ Extract text from PDF resumes and job descriptions
3. ✅ Convert extracted text to structured JSON format
4. ✅ Connect to storage and retrieve stored JSONs
5. ✅ Use LLM to analyze compatibility between resumes and job descriptions
6. ✅ Calculate hybrid scores combining similarity and rule-based boosts
7. ✅ Provide transparent reason codes mapping to resume content
8. ✅ Export ranked results to CSV with all relevant information
9. ✅ Display clear, ranked table with scores and explanations
10. ✅ Support two different loading views (file upload and form-based)

## Next Steps

1. Set up project structure and dependencies (including PDF processing and storage libraries)
2. Implement storage client abstraction and local storage
3. Implement PDF text extraction pipeline
4. Implement resume and JD text-to-JSON conversion pipeline
5. Build two loading views: file upload and form-based
6. Integrate storage search and retrieval functionality
7. Integrate LLM for analysis (using defined prompts)
8. Build hybrid scoring system
9. Implement reason code mapping
10. Create CSV export functionality
11. Build demo interface/visualization

