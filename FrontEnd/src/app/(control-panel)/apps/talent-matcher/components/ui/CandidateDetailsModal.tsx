'use client';

import {
	Dialog,
	DialogTitle,
	DialogContent,
	DialogActions,
	Button,
	Typography,
	Box,
	Chip,
	Divider,
	Paper
} from '@mui/material';
import { formatScore } from '../../lib/utils';
import type { AnalysisResult } from '../../api/types';

type CandidateDetailsModalProps = {
	open: boolean;
	result: AnalysisResult | null;
	onClose: () => void;
};

/**
 * CandidateDetailsModal component to show detailed candidate information
 */
export default function CandidateDetailsModal({ open, result, onClose }: CandidateDetailsModalProps) {
	if (!result) return null;

	const scoreInfo = formatScore(result.overall_score);

	return (
		<Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
			<DialogTitle>
				<Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
					<Typography variant="h6">{result.name}</Typography>
					<Chip label={`Score: ${scoreInfo.value}`} color={scoreInfo.color} />
				</Box>
			</DialogTitle>
			<DialogContent>
				<Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
					<Paper variant="outlined" sx={{ p: 2 }}>
						<Typography variant="subtitle1" gutterBottom>
							Score Breakdown
						</Typography>
						<Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 2, mt: 1 }}>
							<Box>
								<Typography variant="caption" color="text.secondary">
									Overall Score
								</Typography>
								<Typography variant="h6">{result.overall_score.toFixed(2)}</Typography>
							</Box>
							<Box>
								<Typography variant="caption" color="text.secondary">
									Similarity Score
								</Typography>
								<Typography variant="h6">{result.similarity_score.toFixed(2)}</Typography>
							</Box>
							<Box>
								<Typography variant="caption" color="text.secondary">
									Must-Have Hits
								</Typography>
								<Typography variant="h6">{result.must_have_hits}</Typography>
							</Box>
							<Box>
								<Typography variant="caption" color="text.secondary">
									Recency Boost
								</Typography>
								<Typography variant="h6">{result.recency_boost.toFixed(2)}</Typography>
							</Box>
						</Box>
					</Paper>

					<Divider />

					<Box>
						<Typography variant="subtitle1" gutterBottom>
							Reason Codes
						</Typography>
						<Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, mt: 1 }}>
							{result.reason_codes.map((rc, index) => (
								<Paper key={index} variant="outlined" sx={{ p: 1.5 }}>
									<Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
										<Chip label={rc.code} size="small" color="primary" />
										{rc.resume_section && (
											<Typography variant="caption" color="text.secondary">
												{rc.resume_section}
											</Typography>
										)}
									</Box>
									<Typography variant="body2">{rc.description}</Typography>
									{rc.matched_requirements && rc.matched_requirements.length > 0 && (
										<Box sx={{ mt: 1 }}>
											<Typography variant="caption" color="text.secondary">
												Matched:
											</Typography>
											<Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
												{rc.matched_requirements.map((req, reqIndex) => (
													<Chip key={reqIndex} label={req} size="small" variant="outlined" />
												))}
											</Box>
										</Box>
									)}
								</Paper>
							))}
						</Box>
					</Box>

					{result.matched_requirements && result.matched_requirements.length > 0 && (
						<>
							<Divider />
							<Box>
								<Typography variant="subtitle1" gutterBottom>
									Matched Requirements
								</Typography>
								<Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
									{result.matched_requirements.map((req, index) => (
										<Chip key={index} label={req} color="success" />
									))}
								</Box>
							</Box>
						</>
					)}
				</Box>
			</DialogContent>
			<DialogActions>
				<Button onClick={onClose}>Close</Button>
			</DialogActions>
		</Dialog>
	);
}

