export type ReasonCode = {
	code: string;
	description: string;
	resume_section?: string;
	matched_requirements?: string[];
};

export type AnalysisResult = {
	candidate_id: string;
	name: string;
	overall_score: number;
	similarity_score: number;
	must_have_hits: number;
	recency_boost: number;
	reason_codes: ReasonCode[];
	matched_requirements?: string[];
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

