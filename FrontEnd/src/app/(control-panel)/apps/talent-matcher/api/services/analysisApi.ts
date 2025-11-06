import { api } from '@/utils/api';
import type { AnalysisRequest, AnalysisResponse, ProcessingStatus } from '../types';

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

