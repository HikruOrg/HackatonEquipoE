import { api } from '@/utils/api';
import type { AnalysisRequest, AnalysisResponse, AnalysisResult, ProcessingStatus } from '../types';

export const analysisApi = {
	/**
	 * Start analysis of resumes against job description
	 */
	startAnalysis: async (request: AnalysisRequest): Promise<{ analysis_id: string }> => {
		const response = await api
			.post('talent-matcher/analysis/start', {
				json: request
			})
			.json<{ analysis_id: string }>();

		return response;
	},

	/**
	 * Get analysis status
	 */
	getAnalysisStatus: async (analysisId: string): Promise<ProcessingStatus> => {
		const response = await api
			.get(`talent-matcher/analysis/${analysisId}/status`)
			.json<ProcessingStatus>();

		return response;
	},

	/**
	 * Get analysis results
	 */
	getAnalysisResults: async (analysisId: string): Promise<AnalysisResponse> => {
		const response = await api
			.get(`talent-matcher/analysis/${analysisId}/results`)
			.json<AnalysisResponse>();

		return response;
	},

	/**
	 * Cancel ongoing analysis
	 */
	cancelAnalysis: async (analysisId: string): Promise<void> => {
		await api.delete(`talent-matcher/analysis/${analysisId}`);
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

