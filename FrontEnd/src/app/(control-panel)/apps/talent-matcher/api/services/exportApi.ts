import { api } from '@/utils/api';
import type { AnalysisResult } from '../types';

export const exportApi = {
	/**
	 * Export analysis results to CSV
	 */
	exportToCsv: async (analysisId: string): Promise<Blob> => {
		const response = await api
			.get(`talent-matcher/export/${analysisId}/csv`, {
				headers: {
					Accept: 'text/csv'
				}
			})
			.blob();

		return response;
	},

	/**
	 * Generate CSV from results data
	 */
	generateCsv: async (results: AnalysisResult[]): Promise<Blob> => {
		const response = await api
			.post('talent-matcher/export/generate-csv', {
				json: { results }
			})
			.blob();

		return response;
	}
};

