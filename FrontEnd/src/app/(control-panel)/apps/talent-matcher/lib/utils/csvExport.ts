import type { AnalysisResult } from '../../api/types';

/**
 * Convert analysis results to CSV format
 */
export const convertResultsToCsv = (results: AnalysisResult[]): string => {
	// CSV Headers
	const headers = [
		'Rank',
		'Candidate ID',
		'Name',
		'Overall Score',
		'Similarity Score',
		'Must-Have Hits',
		'Recency Boost',
		'Reason Codes',
		'Matched Requirements'
	];

	// Convert reason codes to readable format
	const formatReasonCodes = (reasonCodes: AnalysisResult['reason_codes']): string => {
		return reasonCodes.map((rc) => `${rc.code}: ${rc.description}`).join('; ');
	};

	// Convert matched requirements to readable format
	const formatMatchedRequirements = (matched?: string[]): string => {
		return matched?.join('; ') || '';
	};

	// Create CSV rows
	const rows = results.map((result, index) => {
		const rank = index + 1;
		return [
			rank.toString(),
			result.candidate_id,
			result.name,
			result.overall_score.toFixed(2),
			result.similarity_score.toFixed(2),
			result.must_have_hits.toString(),
			result.recency_boost.toFixed(2),
			formatReasonCodes(result.reason_codes),
			formatMatchedRequirements(result.matched_requirements)
		];
	});

	// Combine headers and rows
	const csvContent = [headers.join(','), ...rows.map((row) => row.map((cell) => `"${cell}"`).join(','))].join('\n');

	return csvContent;
};

/**
 * Download CSV file
 */
export const downloadCsv = (csvContent: string, filename: string): void => {
	// Add BOM for UTF-8 encoding
	const BOM = '\uFEFF';
	const blob = new Blob([BOM + csvContent], { type: 'text/csv;charset=utf-8;' });
	const link = document.createElement('a');
	const url = URL.createObjectURL(blob);

	link.setAttribute('href', url);
	link.setAttribute('download', filename);
	link.style.visibility = 'hidden';

	document.body.appendChild(link);
	link.click();
	document.body.removeChild(link);

	URL.revokeObjectURL(url);
};

/**
 * Generate filename with timestamp
 */
export const generateCsvFilename = (): string => {
	const now = new Date();
	const year = now.getFullYear();
	const month = String(now.getMonth() + 1).padStart(2, '0');
	const day = String(now.getDate()).padStart(2, '0');
	const hours = String(now.getHours()).padStart(2, '0');
	const minutes = String(now.getMinutes()).padStart(2, '0');
	const seconds = String(now.getSeconds()).padStart(2, '0');

	return `ranked_candidates_${year}${month}${day}_${hours}${minutes}${seconds}.csv`;
};

