'use client';

import { useEffect } from 'react';
import { Box, Button, Typography, Alert } from '@mui/material';
import { Cancel as CancelIcon } from '@mui/icons-material';
import ProgressBar from '../ui/ProgressBar';
import { useAnalysisStatus, useAnalysisResults, useCancelAnalysis } from '../../api/hooks/useAnalysis';
import type { ProcessingStatus, AnalysisResult } from '../../api/types';

type ProcessingViewProps = {
	analysisId: string;
	onComplete: (results: AnalysisResult[]) => void;
	onCancel?: () => void;
};

/**
 * ProcessingView - View showing analysis progress
 */
export default function ProcessingView({ analysisId, onComplete, onCancel }: ProcessingViewProps) {
	const { data: status } = useAnalysisStatus(analysisId, true);
	const { data: results } = useAnalysisResults(analysisId, status?.status === 'completed');
	const cancelMutation = useCancelAnalysis();

	useEffect(() => {
		if (status?.status === 'completed' && results) {
			onComplete(results.results);
		}
	}, [status, results, onComplete]);

	const handleCancel = () => {
		cancelMutation.mutate(analysisId);
		if (onCancel) {
			onCancel();
		}
	};

	if (!status) {
		return (
			<Box sx={{ p: 3, textAlign: 'center' }}>
				<Typography>Loading...</Typography>
			</Box>
		);
	}

	return (
		<Box sx={{ p: 3 }}>
			<Typography variant="h4" gutterBottom>
				Processing Analysis
			</Typography>

			<ProgressBar status={status} />

			{status.status === 'error' && (
				<Alert severity="error" sx={{ mb: 2 }}>
					{status.error_message || 'An error occurred during processing'}
				</Alert>
			)}

			{status.status === 'processing' && (
				<Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
					<Button
						variant="outlined"
						color="error"
						startIcon={<CancelIcon />}
						onClick={handleCancel}
						disabled={cancelMutation.isPending}
					>
						Cancel Analysis
					</Button>
				</Box>
			)}
		</Box>
	);
}

