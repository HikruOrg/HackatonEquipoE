import { useMutation } from '@tanstack/react-query';
import { exportApi } from '../services';
import type { AnalysisResult } from '../types';

export const useExportToCsv = () => {
	return useMutation({
		mutationFn: (analysisId: string) => exportApi.exportToCsv(analysisId)
	});
};

export const useGenerateCsv = () => {
	return useMutation({
		mutationFn: (results: AnalysisResult[]) => exportApi.generateCsv(results)
	});
};

