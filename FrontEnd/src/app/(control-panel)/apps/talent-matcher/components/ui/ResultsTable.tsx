'use client';

import { useState } from 'react';
import {
	Box,
	Button,
	Chip,
	IconButton,
	Paper,
	Table,
	TableBody,
	TableCell,
	TableContainer,
	TableHead,
	TableRow,
	Typography,
	TableSortLabel,
	Collapse
} from '@mui/material';
import { ExpandMore as ExpandMoreIcon, ExpandLess as ExpandLessIcon, Visibility as VisibilityIcon } from '@mui/icons-material';
import { formatScore } from '../../lib/utils';
import type { AnalysisResult } from '../../api/types';

type ResultsTableProps = {
	results: AnalysisResult[];
	onViewDetails?: (result: AnalysisResult) => void;
};

/**
 * ResultsTable component to display ranked analysis results
 */
export default function ResultsTable({ results, onViewDetails }: ResultsTableProps) {
	const [expandedRows, setExpandedRows] = useState<Set<number>>(new Set());
	const [sortBy, setSortBy] = useState<keyof AnalysisResult | null>(null);
	const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

	const handleSort = (column: keyof AnalysisResult) => {
		if (sortBy === column) {
			setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
		} else {
			setSortBy(column);
			setSortOrder('desc');
		}
	};

	const toggleRow = (index: number) => {
		const newExpanded = new Set(expandedRows);
		if (newExpanded.has(index)) {
			newExpanded.delete(index);
		} else {
			newExpanded.add(index);
		}
		setExpandedRows(newExpanded);
	};

	const sortedResults = [...results].sort((a, b) => {
		if (!sortBy) return 0;
		const aValue = a[sortBy];
		const bValue = b[sortBy];
		const comparison = typeof aValue === 'number' && typeof bValue === 'number' 
			? aValue - bValue 
			: String(aValue).localeCompare(String(bValue));
		return sortOrder === 'asc' ? comparison : -comparison;
	});

	return (
		<TableContainer component={Paper}>
			<Table>
				<TableHead>
					<TableRow>
						<TableCell width={50}>Rank</TableCell>
						<TableCell>
							<TableSortLabel
								active={sortBy === 'name'}
								direction={sortBy === 'name' ? sortOrder : 'asc'}
								onClick={() => handleSort('name')}
							>
								Name
							</TableSortLabel>
						</TableCell>
						<TableCell>
							<TableSortLabel
								active={sortBy === 'final_score'}
								direction={sortBy === 'final_score' ? sortOrder : 'desc'}
								onClick={() => handleSort('final_score')}
							>
								Final Score
							</TableSortLabel>
						</TableCell>
						<TableCell>
							<TableSortLabel
								active={sortBy === 'similarity_score'}
								direction={sortBy === 'similarity_score' ? sortOrder : 'desc'}
								onClick={() => handleSort('similarity_score')}
							>
								Similarity Score
							</TableSortLabel>
						</TableCell>
						<TableCell>
							Must-Have Matches
						</TableCell>
						<TableCell>Recency Boost</TableCell>
						<TableCell width={100}>Actions</TableCell>
					</TableRow>
				</TableHead>
				<TableBody>
					{sortedResults.map((result, index) => {
						const scoreInfo = formatScore(result.final_score);
						const rowColor = result.final_score >= 80 ? 'success.light' : result.final_score >= 60 ? 'warning.light' : 'error.light';
						const isExpanded = expandedRows.has(index);

						return (
							<>
								<TableRow
									key={result.candidate_id}
									sx={{
										backgroundColor: rowColor,
										'&:hover': {
											backgroundColor: 'action.hover'
										}
									}}
								>
									<TableCell>{index + 1}</TableCell>
									<TableCell>{result.name}</TableCell>
									<TableCell>
										<Chip label={scoreInfo.value} color={scoreInfo.color} size="small" />
									</TableCell>
									<TableCell>{(result.similarity_score ?? 0).toFixed(2)}</TableCell>
									<TableCell>{result.must_have_matches?.length ?? 0}</TableCell>
									<TableCell>{(result.recency_boost ?? 0).toFixed(2)}</TableCell>
									<TableCell>
										<Box sx={{ display: 'flex', gap: 1 }}>
											<IconButton size="small" onClick={() => toggleRow(index)}>
												{isExpanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
											</IconButton>
											{onViewDetails && (
												<IconButton size="small" onClick={() => onViewDetails(result)}>
													<VisibilityIcon />
												</IconButton>
											)}
										</Box>
									</TableCell>
								</TableRow>
								<TableRow>
									<TableCell colSpan={7} sx={{ py: 0 }}>
										<Collapse in={isExpanded} timeout="auto" unmountOnExit>
											<Box sx={{ p: 2 }}>
												<Typography variant="subtitle2" gutterBottom>
													Reason Codes:
												</Typography>
												<Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
													{result.reason_codes.map((rc, rcIndex) => (
														<Chip
															key={rcIndex}
															label={rc}
															size="small"
															variant="outlined"
														/>
													))}
												</Box>
												{result.must_have_matches && result.must_have_matches.length > 0 && (
													<Box sx={{ mt: 2 }}>
														<Typography variant="subtitle2" gutterBottom>
															Must-Have Matches:
														</Typography>
														<Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
															{result.must_have_matches.map((req, reqIndex) => (
																<Chip key={reqIndex} label={req} size="small" color="success" />
															))}
														</Box>
													</Box>
												)}
											</Box>
										</Collapse>
									</TableCell>
								</TableRow>
							</>
						);
					})}
				</TableBody>
			</Table>
		</TableContainer>
	);
}

