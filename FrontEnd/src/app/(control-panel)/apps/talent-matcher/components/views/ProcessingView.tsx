'use client';

import { useEffect } from 'react';
import { Box, Button, Typography, Alert } from '@mui/material';
import { Cancel as CancelIcon } from '@mui/icons-material';
import ProgressBar from '../ui/ProgressBar';
import { useAnalysisStatus, useAnalysisResults, useCancelAnalysis } from '../../api/hooks/useAnalysis';
import type { ProcessingStatus, AnalysisResult } from '../../api/types';

type ProcessingViewProps = {
	onComplete: (results: AnalysisResult[]) => void;
	onCancel?: () => void;
};

/**
 * ProcessingView - View showing analysis progress
 */
export default function ProcessingView({ onComplete, onCancel }: ProcessingViewProps) {
	const { data: status } = useAnalysisStatus(undefined, true);
	const { data: results } = useAnalysisResults(undefined, status?.status === 'completed');
	const cancelMutation = useCancelAnalysis();

	useEffect(() => {
		if (status?.status === 'completed' && results) {
			onComplete(results.results);
		}
	}, [status, results, onComplete]);

	const handleCancel = () => {
		cancelMutation.mutate();
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
					{status.errors.length > 0 ? status.errors.join(', ') : 'An error occurred during processing'}
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

