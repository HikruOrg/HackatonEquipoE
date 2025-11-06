'use client';

import { Box, LinearProgress, Typography, Paper, styled } from '@mui/material';
import { calculateEstimatedTime } from '../../lib/utils';
import type { ProcessingStatus } from '../../api/types';

const ProgressRoot = styled(Paper)(({ theme }) => ({
	padding: theme.spacing(3),
	marginBottom: theme.spacing(2)
}));

type ProgressBarProps = {
	status: ProcessingStatus;
};

/**
 * ProgressBar component to show analysis progress
 */
export default function ProgressBar({ status }: ProgressBarProps) {
	const formatTime = (seconds?: number): string => {
		if (!seconds) return 'Calculating...';
		if (seconds < 60) return `${seconds}s`;
		const minutes = Math.floor(seconds / 60);
		const secs = seconds % 60;
		return `${minutes}m ${secs}s`;
	};

	const getStatusText = (): string => {
		switch (status.status) {
			case 'idle':
				return 'Ready to start';
			case 'processing':
				return `Processing candidate ${status.current_candidate} of ${status.total_candidates}`;
			case 'completed':
				return 'Analysis completed';
			case 'error':
				return `Error: ${status.error_message || 'Unknown error'}`;
			default:
				return 'Unknown status';
		}
	};

	return (
		<ProgressRoot elevation={2}>
			<Box sx={{ mb: 2 }}>
				<Typography variant="h6" gutterBottom>
					Analysis Progress
				</Typography>
				<Typography variant="body2" color="text.secondary">
					{getStatusText()}
				</Typography>
			</Box>
			<LinearProgress
				variant="determinate"
				value={status.progress_percentage}
				sx={{
					height: 8,
					borderRadius: 4,
					mb: 1
				}}
			/>
			<Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
				<Typography variant="caption" color="text.secondary">
					{status.progress_percentage.toFixed(1)}% complete
				</Typography>
				{status.status === 'processing' && status.estimated_time_remaining && (
					<Typography variant="caption" color="text.secondary">
						Estimated time remaining: {formatTime(status.estimated_time_remaining)}
					</Typography>
				)}
			</Box>
		</ProgressRoot>
	);
}

