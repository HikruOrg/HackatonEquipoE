export type FileType = 'pdf' | 'json' | 'txt';

export type FileStatus = 'pending' | 'validating' | 'valid' | 'invalid' | 'processing' | 'processed' | 'error';

export type UploadedFile = {
	id: string;
	name: string;
	type: FileType;
	size: number;
	file: File;
	status: FileStatus;
	error?: string;
	pages?: number; // For PDFs
	preview?: string; // Preview of content
	metadata?: {
		candidate_id?: string;
		jd_id?: string;
		extracted_text?: string;
		parsed_data?: unknown;
	};
};

export type FileValidationResult = {
	valid: boolean;
	error?: string;
	type?: FileType;
};

export type StorageFile = {
	id: string;
	name: string;
	type: 'resume' | 'job_description';
	created_at: string;
	updated_at: string;
	size: number;
	metadata?: Record<string, unknown>;
};

