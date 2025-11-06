'use client';

import { useState } from 'react';
import { Box, Button, Typography, Alert } from '@mui/material';
import { FileDownload as FileDownloadIcon } from '@mui/icons-material';
import ResultsTable from '../ui/ResultsTable';
import CandidateDetailsModal from '../ui/CandidateDetailsModal';
import { useGenerateCsv } from '../../api/hooks/useExport';
import { convertResultsToCsv, downloadCsv, generateCsvFilename } from '../../lib/utils';
import type { AnalysisResult } from '../../api/types';

type ResultsViewProps = {
	results: AnalysisResult[];
	onNewAnalysis?: () => void;
};

/**
 * ResultsView - View displaying ranked analysis results
 */
export default function ResultsView({ results, onNewAnalysis }: ResultsViewProps) {
	const [selectedCandidate, setSelectedCandidate] = useState<AnalysisResult | null>(null);
	const [detailsModalOpen, setDetailsModalOpen] = useState(false);
	const exportMutation = useGenerateCsv();

	const handleViewDetails = (result: AnalysisResult) => {
		setSelectedCandidate(result);
		setDetailsModalOpen(true);
	};

	const handleExport = async () => {
		try {
			const csvContent = convertResultsToCsv(results);
			const filename = generateCsvFilename();
			downloadCsv(csvContent, filename);
		} catch (error) {
			console.error('Export error:', error);
		}
	};

	return (
		<Box sx={{ p: 3 }}>
			<Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
				<Typography variant="h4">Analysis Results</Typography>
				<Box sx={{ display: 'flex', gap: 2 }}>
					<Button
						variant="outlined"
						startIcon={<FileDownloadIcon />}
						onClick={handleExport}
						disabled={exportMutation.isPending}
					>
						Export to CSV
					</Button>
					{onNewAnalysis && (
						<Button variant="contained" onClick={onNewAnalysis}>
							New Analysis
						</Button>
					)}
				</Box>
			</Box>

			{results.length === 0 ? (
				<Alert severity="info">No results to display</Alert>
			) : (
				<>
					<Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
						Showing {results.length} ranked candidates
					</Typography>
					<ResultsTable results={results} onViewDetails={handleViewDetails} />
				</>
			)}

			<CandidateDetailsModal
				open={detailsModalOpen}
				result={selectedCandidate}
				onClose={() => setDetailsModalOpen(false)}
			/>
		</Box>
	);
}

