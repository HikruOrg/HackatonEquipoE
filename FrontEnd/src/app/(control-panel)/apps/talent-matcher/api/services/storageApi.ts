import { api } from '@/utils/api';
import type { StorageFile, Resume, JobDescription } from '../types';

export type StorageSearchParams = {
	type?: 'resume' | 'job_description';
	name?: string;
	created_after?: string;
	created_before?: string;
	limit?: number;
	offset?: number;
};

export const storageApi = {
	/**
	 * List all files in storage
	 */
	listFiles: async (params?: StorageSearchParams): Promise<StorageFile[]> => {
		const searchParams = new URLSearchParams();
		if (params) {
			Object.entries(params).forEach(([key, value]) => {
				if (value !== undefined) {
					searchParams.append(key, String(value));
				}
			});
		}

		const response = await api
			.get('talent-matcher/storage/files', {
				searchParams
			})
			.json<StorageFile[]>();

		return response;
	},

	/**
	 * Get a specific file from storage
	 */
	getFile: async (fileId: string): Promise<Resume | JobDescription> => {
		const response = await api.get(`talent-matcher/storage/files/${fileId}`).json<Resume | JobDescription>();

		return response;
	},

	/**
	 * Save a resume to storage
	 */
	saveResume: async (resume: Resume): Promise<StorageFile> => {
		const response = await api
			.post('talent-matcher/storage/resumes', {
				json: resume
			})
			.json<StorageFile>();

		return response;
	},

	/**
	 * Save a job description to storage
	 */
	saveJobDescription: async (jd: JobDescription): Promise<StorageFile> => {
		const response = await api
			.post('talent-matcher/storage/job-descriptions', {
				json: jd
			})
			.json<StorageFile>();

		return response;
	},

	/**
	 * Delete a file from storage
	 */
	deleteFile: async (fileId: string): Promise<void> => {
		await api.delete(`talent-matcher/storage/files/${fileId}`);
	},

	/**
	 * Search files in storage
	 */
	searchFiles: async (query: string, params?: StorageSearchParams): Promise<StorageFile[]> => {
		const searchParams = new URLSearchParams({ q: query });
		if (params) {
			Object.entries(params).forEach(([key, value]) => {
				if (value !== undefined) {
					searchParams.append(key, String(value));
				}
			});
		}

		const response = await api
			.get('talent-matcher/storage/search', {
				searchParams
			})
			.json<StorageFile[]>();

		return response;
	}
};

