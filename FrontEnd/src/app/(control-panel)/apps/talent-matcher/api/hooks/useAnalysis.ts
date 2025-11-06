import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { analysisApi } from '../services';
import type { AnalysisRequest, ProcessingStatus, AnalysisResponse } from '../types';

export const useStartAnalysis = () => {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: (request: AnalysisRequest) => analysisApi.startAnalysis(request),
		onSuccess: () => {
			// Invalidate status to trigger refetch
			queryClient.invalidateQueries({ queryKey: ['talent-matcher', 'analysis', 'status'] });
		}
	});
};

export const useAnalysisStatus = (analysisId?: string | null, enabled = true) => {
	return useQuery({
		queryKey: ['talent-matcher', 'analysis', 'status'],
		queryFn: () => analysisApi.getAnalysisStatus(),
		enabled: enabled,
		refetchInterval: (query) => {
			// Poll every 2 seconds if processing, otherwise stop polling
			if (query.state.data?.status === 'processing') {
				return 2000;
			}
			return false;
		}
	});
};

export const useAnalysisResults = (analysisId?: string | null, enabled = true) => {
	return useQuery({
		queryKey: ['talent-matcher', 'analysis', 'results'],
		queryFn: () => analysisApi.getAnalysisResults(),
		enabled: enabled
	});
};

export const useCancelAnalysis = () => {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: () => analysisApi.cancelAnalysis(),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ['talent-matcher', 'analysis', 'status'] });
		}
	});
};

