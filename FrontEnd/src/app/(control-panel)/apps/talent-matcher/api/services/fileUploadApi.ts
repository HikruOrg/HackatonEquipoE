import { api } from '@/utils/api';
import type { UploadedFile, FileValidationResult, Resume, JobDescription } from '../types';

export const fileUploadApi = {
	/**
	 * Upload resume files (PDF, JSON, or TXT) for processing
	 */
	uploadResumes: async (files: File[]): Promise<{ uploaded: number; files: Array<{ filename: string; resume_id: string; type: string; status: string }>; errors: string[] }> => {
		const formData = new FormData();
		files.forEach((file) => {
			formData.append('files', file);
		});

		const response = await api
			.post('upload/resumes', {
				body: formData
			})
			.json<{ uploaded: number; files: Array<{ filename: string; resume_id: string; type: string; status: string }>; errors: string[] }>();

		return response;
	},

	/**
	 * Upload job description file (PDF, JSON, or TXT)
	 */
	uploadJobDescription: async (file: File): Promise<{ filename: string; jd_id: string; type: string; status: string }> => {
		const formData = new FormData();
		formData.append('file', file);

		const response = await api
			.post('upload/job-description', {
				body: formData
			})
			.json<{ filename: string; jd_id: string; type: string; status: string }>();

		return response;
	},

	/**
	 * Validate a file before upload
	 */
	validateFile: async (file: File): Promise<FileValidationResult> => {
		const formData = new FormData();
		formData.append('file', file);

		const response = await api
			.post('talent-matcher/files/validate', {
				body: formData
			})
			.json<FileValidationResult>();

		return response;
	},

	/**
	 * Extract text from PDF or TXT
	 */
	extractPdfText: async (fileId: string): Promise<{ text: string; pages: number }> => {
		const response = await api
			.post(`talent-matcher/files/${fileId}/extract-pdf`, {})
			.json<{ text: string; pages: number }>();

		return response;
	},

	/**
	 * Parse PDF or TXT text to structured JSON (Resume or JD)
	 */
	parsePdfToJson: async (
		fileId: string,
		type: 'resume' | 'job_description'
	): Promise<Resume | JobDescription> => {
		const response = await api
			.post(`talent-matcher/files/${fileId}/parse-pdf`, {
				json: { type }
			})
			.json<Resume | JobDescription>();

		return response;
	}
};

