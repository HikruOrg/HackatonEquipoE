'use client';

import { useState } from 'react';
import {
	Box,
	Card,
	CardContent,
	Typography,
	Chip,
	Button,
	CircularProgress,
	Alert,
	List,
	ListItem,
	ListItemText,
	Paper,
	Divider,
	Stack,
	Accordion,
	AccordionSummary,
	AccordionDetails
} from '@mui/material';
import {
	WorkOutline as WorkIcon,
	Person as PersonIcon,
	EmojiEvents as TrophyIcon,
	Assessment as AssessmentIcon,
	ExpandMore as ExpandMoreIcon
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { getStoredJobDescriptions } from '../../api/services/storageApi';
import { getResults, processStoredFiles, getProcessingStatus } from '../../api/services/analysisApi';
import type { JobDescription } from '../../api/types/jobDescription.types';
import type { AnalysisResult } from '../../api/types/analysis.types';

/**
 * JobDescriptionsView - Lista todas las Job Descriptions y permite ver candidatos rankeados
 */
export default function JobDescriptionsView() {
	const [selectedJD, setSelectedJD] = useState<JobDescription | null>(null);
	const [isProcessing, setIsProcessing] = useState(false);
	const [processingProgress, setProcessingProgress] = useState({ progress: 0, total: 0 });
	const [expandedCandidate, setExpandedCandidate] = useState<string | false>(false);

	// Obtener todas las Job Descriptions
	const {
		data: jobDescriptions,
		isLoading: isLoadingJDs,
		error: jdError
	} = useQuery({
		queryKey: ['jobDescriptions'],
		queryFn: getStoredJobDescriptions,
		retry: 1,
		staleTime: 30000 // 30 segundos
	});

	// Obtener resultados (candidatos rankeados)
	const {
		data: results,
		isLoading: isLoadingResults,
		error: resultsError
	} = useQuery({
		queryKey: ['analysisResults'],
		queryFn: async () => {
			try {
				return await getResults();
			} catch (error) {
				// Si el error es 400 (no hay resultados), retornar array vacío
				if (error instanceof Error && error.message.includes('400')) {
					return [];
				}
				throw error;
			}
		},
		enabled: !!selectedJD, // Solo cargar cuando hay una JD seleccionada
		retry: false // No reintentar si falla
	});

	const handleSelectJD = (jd: JobDescription) => {
		setSelectedJD(jd);
	};

	const handleBack = () => {
		setSelectedJD(null);
	};

	const handleProcessCandidates = async () => {
		if (!selectedJD?.jd_id) return;

		try {
			setIsProcessing(true);
			await processStoredFiles(selectedJD.jd_id);

			// Poll for status updates
			const pollInterval = setInterval(async () => {
				try {
					const status = await getProcessingStatus();
					setProcessingProgress({ progress: status.progress, total: status.total });

					if (status.status === 'completed' || status.status === 'error') {
						clearInterval(pollInterval);
						setIsProcessing(false);
						// Refetch results
						window.location.reload();
					}
				} catch (error) {
					console.error('Error polling status:', error);
				}
			}, 2000); // Poll every 2 seconds

			// Timeout after 5 minutes
			setTimeout(() => {
				clearInterval(pollInterval);
				setIsProcessing(false);
			}, 300000);
		} catch (error) {
			console.error('Error processing candidates:', error);
			setIsProcessing(false);
		}
	};

	if (isLoadingJDs) {
		return (
			<Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
				<CircularProgress />
			</Box>
		);
	}

	if (jdError) {
		return (
			<Box sx={{ p: 3 }}>
				<Alert severity="error">Error al cargar Job Descriptions: {String(jdError)}</Alert>
			</Box>
		);
	}

	// Vista de lista de Job Descriptions
	if (!selectedJD) {
		return (
			<Box sx={{ p: 3 }}>
				<Typography variant="h4" gutterBottom sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
					<WorkIcon fontSize="large" />
					Job Descriptions
				</Typography>

				{!jobDescriptions || !Array.isArray(jobDescriptions) || jobDescriptions.length === 0 ? (
					<Alert severity="info">
						No hay Job Descriptions disponibles. Sube una JD primero desde la sección de File Upload.
					</Alert>
				) : (
					<Box
						sx={{
							display: 'grid',
							gridTemplateColumns: { xs: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)' },
							gap: 3
						}}
					>
						{jobDescriptions.map((jd) => (
							<Card
								key={jd.jd_id}
								sx={{
									cursor: 'pointer',
									transition: 'all 0.2s',
									'&:hover': {
										transform: 'translateY(-4px)',
										boxShadow: 6
									}
								}}
								onClick={() => handleSelectJD(jd)}
							>
								<CardContent>
									<Typography variant="h6" gutterBottom noWrap>
										{jd.title}
									</Typography>

									<Typography
										variant="body2"
										color="text.secondary"
										sx={{
											mb: 2,
											overflow: 'hidden',
											textOverflow: 'ellipsis',
											display: '-webkit-box',
											WebkitLineClamp: 3,
											WebkitBoxOrient: 'vertical'
										}}
									>
										{jd.description}
									</Typography>

									<Box sx={{ mb: 2 }}>
										<Typography variant="caption" color="text.secondary" gutterBottom>
											Must-Have Requirements ({jd.must_have_requirements?.length || 0})
										</Typography>
										<Stack direction="row" spacing={1} flexWrap="wrap" sx={{ mt: 1, gap: 1 }}>
											{jd.must_have_requirements?.slice(0, 3).map((req, idx) => (
												<Chip key={idx} label={req} size="small" />
											))}
											{jd.must_have_requirements && jd.must_have_requirements.length > 3 && (
												<Chip
													label={`+${jd.must_have_requirements.length - 3} more`}
													size="small"
													variant="outlined"
												/>
											)}
										</Stack>
									</Box>

									{jd.experience_years_required && (
										<Typography variant="caption" color="text.secondary">
											Experience Required: {jd.experience_years_required}+ years
										</Typography>
									)}

									<Box sx={{ mt: 2 }}>
										<Button
											variant="contained"
											fullWidth
											startIcon={<AssessmentIcon />}
											onClick={(e) => {
												e.stopPropagation();
												handleSelectJD(jd);
											}}
										>
											View Ranked Candidates
										</Button>
									</Box>
								</CardContent>
							</Card>
						))}
					</Box>
				)}
			</Box>
		);
	}

	// Vista de candidatos rankeados para la JD seleccionada (Layout 65-35)
	return (
		<Box sx={{ p: 3 }}>
			{/* Header con botones de acción */}
			<Box sx={{ display: 'flex', gap: 2, mb: 3, alignItems: 'center' }}>
				<Button onClick={handleBack} variant="outlined">
					← Back to Job Descriptions
				</Button>
				<Button 
					variant="contained" 
					color="primary"
					onClick={handleProcessCandidates}
					disabled={isProcessing}
					startIcon={isProcessing ? <CircularProgress size={20} /> : <AssessmentIcon />}
				>
					{isProcessing 
						? `Processing... (${processingProgress.progress}/${processingProgress.total})`
						: 'Process Candidates'}
				</Button>
			</Box>

			{/* Layout 65-35: JD a la izquierda, Candidatos a la derecha */}
			<Box sx={{ 
				display: 'flex', 
				gap: 3,
				flexDirection: { xs: 'column', lg: 'row' },
				alignItems: 'flex-start'
			}}>
				{/* COLUMNA IZQUIERDA: Job Description (65%) */}
				<Paper 
					sx={{ 
						p: 3, 
						flex: { xs: '1 1 100%', lg: '0 0 65%' },
						maxWidth: { lg: '65%' },
						position: { lg: 'sticky' },
						top: { lg: 24 },
						maxHeight: { lg: 'calc(100vh - 200px)' },
						overflowY: { lg: 'auto' }
					}}
				>
					<Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
						<WorkIcon />
						{selectedJD.title}
					</Typography>

					<Divider sx={{ my: 2 }} />

					<Typography variant="body1" paragraph>
						{selectedJD.description}
					</Typography>

					<Divider sx={{ my: 2 }} />

					{/* Experience Required */}
					{selectedJD.experience_years_required && (
						<Box sx={{ mb: 3 }}>
							<Typography variant="subtitle2" color="primary" gutterBottom>
								Experience Required
							</Typography>
							<Typography variant="body1">
								{selectedJD.experience_years_required}+ years
							</Typography>
						</Box>
					)}

					{/* Must-Have Requirements */}
					<Box sx={{ mb: 3 }}>
						<Typography variant="subtitle2" color="primary" gutterBottom>
							Must-Have Requirements ({selectedJD.must_have_requirements?.length || 0})
						</Typography>
						<Stack direction="row" spacing={1} flexWrap="wrap" sx={{ mt: 1, gap: 1 }}>
							{selectedJD.must_have_requirements?.map((req, idx) => (
								<Chip key={idx} label={req} color="primary" size="small" />
							))}
						</Stack>
					</Box>

					{/* Nice-to-Have */}
					{selectedJD.nice_to_have && selectedJD.nice_to_have.length > 0 && (
						<Box sx={{ mb: 3 }}>
							<Typography variant="subtitle2" color="primary" gutterBottom>
								Nice-to-Have ({selectedJD.nice_to_have.length})
							</Typography>
							<Stack direction="row" spacing={1} flexWrap="wrap" sx={{ mt: 1, gap: 1 }}>
								{selectedJD.nice_to_have.map((req, idx) => (
									<Chip key={idx} label={req} variant="outlined" size="small" />
								))}
							</Stack>
						</Box>
					)}

					{/* Raw Text Preview */}
					{selectedJD.raw_text && (
						<Box sx={{ mb: 3 }}>
							<Typography variant="subtitle2" color="primary" gutterBottom>
								Additional Details
							</Typography>
							<Typography 
								variant="body2" 
								color="text.secondary"
								sx={{
									maxHeight: 200,
									overflowY: 'auto',
									whiteSpace: 'pre-wrap',
									bgcolor: 'grey.50',
									p: 2,
									borderRadius: 1,
									fontSize: '0.875rem'
								}}
							>
								{selectedJD.raw_text}
							</Typography>
						</Box>
					)}
				</Paper>

				{/* COLUMNA DERECHA: Candidatos Rankeados (35%) */}
				<Box sx={{ 
					flex: { xs: '1 1 100%', lg: '0 0 35%' },
					maxWidth: { lg: '35%' },
					width: '100%'
				}}>
					<Typography 
						variant="h5" 
						gutterBottom 
						sx={{ 
							display: 'flex', 
							alignItems: 'center', 
							gap: 1,
							mb: 2,
							position: 'sticky',
							top: 0,
							bgcolor: 'background.default',
							zIndex: 1,
							py: 1
						}}
					>
						<TrophyIcon />
						Ranked Candidates
					</Typography>

					{isLoadingResults ? (
						<Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
							<CircularProgress />
						</Box>
					) : resultsError ? (
						<Alert severity="warning">
							No hay resultados disponibles. Para ver candidatos rankeados, primero debes:
							<br />
							1. Ir a la pestaña "New Analysis"
							<br />
							2. Subir resumes y esta job description
							<br />
							3. Ejecutar el análisis
						</Alert>
					) : !results || results.length === 0 ? (
						<Alert severity="info">
							No hay candidatos evaluados para esta posición. Haz click en "Process Candidates" para analizar los resumes almacenados.
						</Alert>
					) : (
						<Stack spacing={1.5}>
							{results
								.sort((a, b) => (b.final_score || 0) - (a.final_score || 0))
								.map((candidate, index) => (
									<CandidateCard 
										key={candidate.candidate_id} 
										candidate={candidate} 
										rank={index + 1}
										expanded={expandedCandidate === candidate.candidate_id}
										onChange={(id) => setExpandedCandidate(expandedCandidate === id ? false : id)}
									/>
								))}
						</Stack>
					)}
				</Box>
			</Box>
		</Box>
	);
}

/**
 * CandidateCard - Acordeón compacto de candidato
 */
function CandidateCard({ 
	candidate, 
	rank, 
	expanded, 
	onChange 
}: { 
	candidate: AnalysisResult; 
	rank: number;
	expanded: boolean;
	onChange: (candidateId: string) => void;
}) {
	const getRankColor = (rankNum: number) => {
		if (rankNum === 1) return '#FFD700'; // gold
		if (rankNum === 2) return '#C0C0C0'; // silver
		if (rankNum === 3) return '#CD7F32'; // bronze
		return 'grey.400';
	};

	const getRankBgColor = (rankNum: number) => {
		if (rankNum === 1) return 'rgba(255, 215, 0, 0.15)';
		if (rankNum === 2) return 'rgba(192, 192, 192, 0.15)';
		if (rankNum === 3) return 'rgba(205, 127, 50, 0.15)';
		return 'transparent';
	};

	const getScoreColor = (score: number) => {
		if (score >= 80) return '#4caf50'; // green
		if (score >= 60) return '#ff9800'; // orange
		if (score >= 40) return '#ff5722'; // deep orange
		return '#f44336'; // red
	};

	return (
		<Accordion 
			expanded={expanded}
			onChange={() => onChange(candidate.candidate_id)}
			sx={{
				border: 1,
				borderColor: rank <= 3 ? getRankColor(rank) : 'divider',
				borderWidth: rank <= 3 ? 2 : 1,
				bgcolor: getRankBgColor(rank),
				'&:before': { display: 'none' },
				boxShadow: expanded ? 3 : 1,
				borderRadius: 1,
				'&:not(:last-child)': {
					mb: 0
				}
			}}
		>
			<AccordionSummary 
				expandIcon={<ExpandMoreIcon />}
				sx={{ 
					minHeight: 72,
					'&.Mui-expanded': { minHeight: 72 },
					'& .MuiAccordionSummary-content': {
						my: 1.5,
						alignItems: 'center'
					}
				}}
			>
				<Box sx={{ 
					display: 'flex', 
					alignItems: 'center', 
					gap: 1.5, 
					width: '100%', 
					pr: 1 
				}}>
					{/* Rank Badge */}
					<Box
						sx={{
							width: 44,
							height: 44,
							borderRadius: '50%',
							bgcolor: getRankColor(rank),
							display: 'flex',
							alignItems: 'center',
							justifyContent: 'center',
							fontWeight: 'bold',
							fontSize: 16,
							color: 'white',
							flexShrink: 0,
							boxShadow: 1
						}}
					>
						#{rank}
					</Box>

					{/* Candidate Name & Info */}
					<Box sx={{ flex: 1, minWidth: 0, overflow: 'hidden' }}>
						<Typography 
							variant="subtitle2" 
							sx={{ 
								fontWeight: 600,
								overflow: 'hidden',
								textOverflow: 'ellipsis',
								whiteSpace: 'nowrap',
								mb: 0.25
							}}
						>
							{candidate.name}
						</Typography>
						<Typography 
							variant="caption" 
							color="text.secondary"
							sx={{
								display: 'block',
								fontSize: '0.7rem'
							}}
						>
							{Array.isArray(candidate.must_have_matches) 
								? candidate.must_have_matches.length 
								: 0} must-have requirements matched
						</Typography>
					</Box>

					{/* Score Badge */}
					<Box
						sx={{
							bgcolor: getScoreColor(candidate.final_score || 0),
							color: 'white',
							fontWeight: 'bold',
							fontSize: 18,
							height: 44,
							minWidth: 60,
							display: 'flex',
							alignItems: 'center',
							justifyContent: 'center',
							borderRadius: 1,
							flexShrink: 0,
							boxShadow: 1
						}}
					>
						{(candidate.final_score || 0).toFixed(1)}
					</Box>
				</Box>
			</AccordionSummary>

			<AccordionDetails sx={{ pt: 0, pb: 2 }}>
				<Divider sx={{ mb: 2 }} />
				
				{/* Detailed Scores */}
				<Box sx={{ mb: 2 }}>
					<Typography variant="caption" color="text.secondary" fontWeight={600} sx={{ mb: 1, display: 'block' }}>
						SCORE BREAKDOWN
					</Typography>
					<Box sx={{ 
						display: 'grid', 
						gridTemplateColumns: 'repeat(3, 1fr)',
						gap: 1.5
					}}>
						<Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
							<Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.65rem' }}>
								Similarity
							</Typography>
							<Typography variant="h6" fontWeight="bold" color="primary">
								{(candidate.similarity_score || 0).toFixed(1)}
							</Typography>
						</Paper>
						<Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
							<Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.65rem' }}>
								Must-Have
							</Typography>
							<Typography variant="h6" fontWeight="bold" color="primary">
								{Array.isArray(candidate.must_have_matches) 
									? candidate.must_have_matches.length 
									: 0}
							</Typography>
						</Paper>
						<Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
							<Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.65rem' }}>
								Recency
							</Typography>
							<Typography variant="h6" fontWeight="bold" color="primary">
								{(candidate.recency_boost || 0).toFixed(1)}
							</Typography>
						</Paper>
					</Box>
				</Box>

				{/* Candidate ID */}
				<Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 2, fontSize: '0.7rem' }}>
					ID: {candidate.candidate_id}
				</Typography>

				{/* Matched Requirements */}
				{candidate.must_have_matches && candidate.must_have_matches.length > 0 && (
					<Box sx={{ mb: 2 }}>
						<Typography variant="caption" color="text.secondary" fontWeight={600} sx={{ mb: 1, display: 'block' }}>
							MATCHED REQUIREMENTS
						</Typography>
						<List dense disablePadding sx={{ 
							bgcolor: 'success.50',
							borderRadius: 1,
							p: 1
						}}>
							{candidate.must_have_matches.map((req, idx) => (
								<ListItem key={idx} sx={{ py: 0.25, px: 0.5 }}>
									<ListItemText 
										primary={`✓ ${req}`}
										primaryTypographyProps={{ 
											variant: 'body2',
											fontSize: '0.8rem',
											color: 'success.dark'
										}}
									/>
								</ListItem>
							))}
						</List>
					</Box>
				)}

				{/* Reason Codes */}
				{candidate.reason_codes && candidate.reason_codes.length > 0 && (
					<Box>
						<Typography variant="caption" color="text.secondary" fontWeight={600} sx={{ mb: 1, display: 'block' }}>
							ANALYSIS REASONS
						</Typography>
						<Stack direction="row" spacing={0.5} flexWrap="wrap" sx={{ gap: 0.5 }}>
							{candidate.reason_codes.map((reason, idx) => (
								<Chip
									key={idx}
									label={reason}
									size="small"
									variant="outlined"
									sx={{ fontSize: '0.7rem', height: 24 }}
								/>
							))}
						</Stack>
					</Box>
				)}
			</AccordionDetails>
		</Accordion>
	);
}
