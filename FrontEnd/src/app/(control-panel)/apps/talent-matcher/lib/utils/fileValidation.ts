import type { FileType, FileValidationResult } from '../../api/types';

/**
 * Validate file type and format
 */
export const validateFile = (file: File): FileValidationResult => {
	// Check file extension
	const extension = file.name.split('.').pop()?.toLowerCase();

	if (!extension) {
		return {
			valid: false,
			error: 'File must have an extension'
		};
	}

	if (extension === 'pdf') {
		// Check MIME type for PDF
		if (file.type && file.type !== 'application/pdf') {
			return {
				valid: false,
				error: 'Invalid PDF file type'
			};
		}
		return {
			valid: true,
			type: 'pdf'
		};
	}

	if (extension === 'json') {
		// Check MIME type for JSON
		if (file.type && file.type !== 'application/json' && file.type !== 'text/json') {
			// Some browsers don't set MIME type correctly for JSON, so we'll be lenient
		}
		return {
			valid: true,
			type: 'json'
		};
	}

	return {
		valid: false,
		error: `Unsupported file type: .${extension}. Only PDF and JSON files are supported.`
	};
};

/**
 * Validate JSON file content
 */
export const validateJsonFile = async (file: File): Promise<{ valid: boolean; error?: string; data?: unknown }> => {
	try {
		const text = await file.text();
		const data = JSON.parse(text);
		return {
			valid: true,
			data
		};
	} catch (error) {
		return {
			valid: false,
			error: error instanceof Error ? error.message : 'Invalid JSON format'
		};
	}
};

/**
 * Format file size to human readable format
 */
export const formatFileSize = (bytes: number): string => {
	if (bytes === 0) return '0 Bytes';

	const k = 1024;
	const sizes = ['Bytes', 'KB', 'MB', 'GB'];
	const i = Math.floor(Math.log(bytes) / Math.log(k));

	return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
};

/**
 * Generate unique ID for uploaded files
 */
export const generateFileId = (): string => {
	return `file_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};

