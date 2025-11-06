export type ReasonCode = {
	code: string;
	description: string;
	resume_section?: string;
	matched_requirements?: string[];
};

export type AnalysisResult = {
	candidate_id: string;
	name: string;
	final_score: number; // Changed from overall_score to match backend
	similarity_score: number;
	must_have_matches: string[]; // Changed from must_have_hits to match backend (array of matched requirements)
	recency_boost: number;
	reason_codes: string[]; // Changed to string[] to match backend
	hit_mappings?: Record<string, string>; // Added to match backend
	rank?: number; // Added to match backend
};

export type AnalysisRequest = {
	resumes: string[]; // Array of candidate_ids or resume JSONs
	job_description: string; // jd_id or JD JSON
};

export type AnalysisResponse = {
	results: AnalysisResult[];
	total_processed: number;
	total_failed: number;
	processing_time: number;
};

export type ProcessingStatus = {
	status: 'idle' | 'processing' | 'completed' | 'error';
	current_candidate: number;
	total_candidates: number;
	progress_percentage: number;
	estimated_time_remaining?: number;
	error_message?: string;
};

