import { api } from '@/utils/api';
import type { UploadedFile, FileValidationResult, Resume, JobDescription } from '../types';

export const fileUploadApi = {
	/**
	 * Upload a file (PDF or JSON) for processing
	 */
	uploadFile: async (file: File): Promise<UploadedFile> => {
		const formData = new FormData();
		formData.append('file', file);

		const response = await api
			.post('talent-matcher/files/upload', {
				body: formData
			})
			.json<UploadedFile>();

		return response;
	},

	/**
	 * Upload multiple files at once
	 */
	uploadFiles: async (files: File[]): Promise<UploadedFile[]> => {
		const formData = new FormData();
		files.forEach((file) => {
			formData.append('files', file);
		});

		const response = await api
			.post('talent-matcher/files/upload-multiple', {
				body: formData
			})
			.json<UploadedFile[]>();

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
	 * Extract text from PDF
	 */
	extractPdfText: async (fileId: string): Promise<{ text: string; pages: number }> => {
		const response = await api
			.post(`talent-matcher/files/${fileId}/extract-pdf`, {})
			.json<{ text: string; pages: number }>();

		return response;
	},

	/**
	 * Parse PDF text to structured JSON (Resume or JD)
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

