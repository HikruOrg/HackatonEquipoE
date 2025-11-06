import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { storageApi, type StorageSearchParams } from '../services';
import type { Resume, JobDescription, StorageFile } from '../types';

export const useStorageFiles = (params?: StorageSearchParams) => {
	return useQuery({
		queryKey: ['talent-matcher', 'storage', 'files', params],
		queryFn: () => storageApi.listFiles(params)
	});
};

export const useStorageFile = (fileId: string | null, enabled = true) => {
	return useQuery({
		queryKey: ['talent-matcher', 'storage', 'files', fileId],
		queryFn: () => storageApi.getFile(fileId!),
		enabled: enabled && !!fileId
	});
};

export const useSaveResume = () => {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: (resume: Resume) => storageApi.saveResume(resume),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ['talent-matcher', 'storage', 'files'] });
		}
	});
};

export const useSaveJobDescription = () => {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: (jd: JobDescription) => storageApi.saveJobDescription(jd),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ['talent-matcher', 'storage', 'files'] });
		}
	});
};

export const useDeleteStorageFile = () => {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: (fileId: string) => storageApi.deleteFile(fileId),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ['talent-matcher', 'storage', 'files'] });
		}
	});
};

export const useSearchStorage = () => {
	return useMutation({
		mutationFn: ({ query, params }: { query: string; params?: StorageSearchParams }) =>
			storageApi.searchFiles(query, params)
	});
};

