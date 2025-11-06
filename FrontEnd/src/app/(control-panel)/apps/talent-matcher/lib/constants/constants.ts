/**
 * Maximum file size allowed (10MB)
 */
export const MAX_FILE_SIZE = 10 * 1024 * 1024;

/**
 * Maximum number of resume files allowed
 */
export const MAX_RESUME_FILES = 50;

/**
 * Supported file types
 */
export const SUPPORTED_FILE_TYPES = ['application/pdf', 'application/json', 'text/json'] as const;

/**
 * File type extensions
 */
export const FILE_EXTENSIONS = {
	pdf: ['.pdf'],
	json: ['.json']
} as const;

/**
 * Score thresholds
 */
export const SCORE_THRESHOLDS = {
	excellent: 80,
	good: 60,
	fair: 40
} as const;

/**
 * Reason code types
 */
export const REASON_CODE_TYPES = {
	SKILL_MATCH: 'SKILL_MATCH',
	EXPERIENCE_MATCH: 'EXPERIENCE_MATCH',
	MUST_HAVE_MATCH: 'MUST_HAVE_MATCH',
	RECENT_EXP: 'RECENT_EXP',
	EDUCATION_MATCH: 'EDUCATION_MATCH',
	MISSING_REQUIREMENT: 'MISSING_REQUIREMENT'
} as const;

