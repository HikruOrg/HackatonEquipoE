import { api } from '@/utils/api';
import type { AnalysisRequest, AnalysisResponse, AnalysisResult, ProcessingStatus } from '../types';

export const analysisApi = {
	/**
	 * Start analysis of resumes against job description using stored files
	 */
	startAnalysis: async (request: AnalysisRequest): Promise<{ status: string; message: string }> => {
		// The backend expects jd_id as query parameter
		const jdId = typeof request.job_description === 'string' ? request.job_description : request.job_description;
		
		const response = await api
			.post(`process/stored?jd_id=${jdId}`)
			.json<{ status: string; message: string; jd_id: string; total_resumes: number }>();

		return { status: response.status, message: response.message };
	},

	/**
	 * Get analysis status
	 */
	getAnalysisStatus: async (analysisId?: string): Promise<ProcessingStatus> => {
		const response = await api
			.get('process/status')
			.json<ProcessingStatus>();

		return response;
	},

	/**
	 * Get analysis results
	 */
	getAnalysisResults: async (analysisId?: string): Promise<AnalysisResponse> => {
		const response = await api
			.get('results')
			.json<{ results: AnalysisResult[]; total: number }>();

		return { 
			results: response.results,
			total_processed: response.total,
			total_failed: 0,
			processing_time: 0
		};
	},

	/**
	 * Cancel ongoing analysis
	 */
	cancelAnalysis: async (analysisId?: string): Promise<void> => {
		// Backend doesn't have a cancel endpoint yet
		console.warn('Cancel analysis not implemented in backend');
	}
};

/**
 * Helper function to get latest results
 */
export const getResults = async () => {
	const response = await api.get('results').json<{ results: AnalysisResult[]; total: number }>();
	return response.results;
};

/**
 * Helper function to start processing with stored files
 */
export const processStoredFiles = async (jdId: string) => {
	const response = await api.post(`process/stored?jd_id=${jdId}`).json<{
		status: string;
		message: string;
		jd_id: string;
		total_resumes: number;
	}>();
	return response;
};

/**
 * Helper function to get processing status
 */
export const getProcessingStatus = async () => {
	const response = await api.get('process/status').json<{
		status: string;
		progress: number;
		total: number;
		results: any[];
		errors: any[];
	}>();
	return response;
};

