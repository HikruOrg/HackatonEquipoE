import { useMutation, useQueryClient } from '@tanstack/react-query';
import { fileUploadApi } from '../services';
import type { UploadedFile, FileValidationResult } from '../types';

export const useFileUpload = () => {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: (file: File) => fileUploadApi.uploadFile(file),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ['talent-matcher', 'files'] });
		}
	});
};

export const useMultipleFileUpload = () => {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: (files: File[]) => fileUploadApi.uploadFiles(files),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ['talent-matcher', 'files'] });
		}
	});
};

export const useFileValidation = () => {
	return useMutation({
		mutationFn: (file: File): Promise<FileValidationResult> => fileUploadApi.validateFile(file)
	});
};

export const usePdfExtraction = () => {
	return useMutation({
		mutationFn: (fileId: string) => fileUploadApi.extractPdfText(fileId)
	});
};

export const usePdfParsing = () => {
	return useMutation({
		mutationFn: ({ fileId, type }: { fileId: string; type: 'resume' | 'job_description' }) =>
			fileUploadApi.parsePdfToJson(fileId, type)
	});
};

