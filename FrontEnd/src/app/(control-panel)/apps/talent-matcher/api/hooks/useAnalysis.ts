import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { analysisApi } from '../services';
import type { AnalysisRequest, ProcessingStatus, AnalysisResponse } from '../types';

export const useStartAnalysis = () => {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: (request: AnalysisRequest) => analysisApi.startAnalysis(request),
		onSuccess: (data) => {
			queryClient.setQueryData(['talent-matcher', 'analysis', data.analysis_id], {
				status: 'processing' as const,
				current_candidate: 0,
				total_candidates: 0,
				progress_percentage: 0
			});
		}
	});
};

export const useAnalysisStatus = (analysisId: string | null, enabled = true) => {
	return useQuery({
		queryKey: ['talent-matcher', 'analysis', analysisId, 'status'],
		queryFn: () => analysisApi.getAnalysisStatus(analysisId!),
		enabled: enabled && !!analysisId,
		refetchInterval: (data) => {
			// Poll every 2 seconds if processing, otherwise stop polling
			if (data?.status === 'processing') {
				return 2000;
			}
			return false;
		}
	});
};

export const useAnalysisResults = (analysisId: string | null, enabled = true) => {
	return useQuery({
		queryKey: ['talent-matcher', 'analysis', analysisId, 'results'],
		queryFn: () => analysisApi.getAnalysisResults(analysisId!),
		enabled: enabled && !!analysisId
	});
};

export const useCancelAnalysis = () => {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: (analysisId: string) => analysisApi.cancelAnalysis(analysisId),
		onSuccess: (_, analysisId) => {
			queryClient.setQueryData<ProcessingStatus>(
				['talent-matcher', 'analysis', analysisId, 'status'],
				(old) => ({
					...old!,
					status: 'error',
					error_message: 'Analysis cancelled by user'
				})
			);
		}
	});
};

