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
	Stack
} from '@mui/material';
import {
	WorkOutline as WorkIcon,
	Person as PersonIcon,
	EmojiEvents as TrophyIcon,
	Assessment as AssessmentIcon
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

	// Vista de candidatos rankeados para la JD seleccionada
	return (
		<Box sx={{ p: 3 }}>
			<Box sx={{ display: 'flex', gap: 2, mb: 2, alignItems: 'center' }}>
				<Button onClick={handleBack}>
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

			<Paper sx={{ p: 3, mb: 3 }}>
				<Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
					<WorkIcon />
					{selectedJD.title}
				</Typography>

				<Typography variant="body1" color="text.secondary" paragraph>
					{selectedJD.description}
				</Typography>

				<Divider sx={{ my: 2 }} />

				<Typography variant="subtitle2" gutterBottom>
					Must-Have Requirements:
				</Typography>
				<Stack direction="row" spacing={1} flexWrap="wrap" sx={{ mb: 2, gap: 1 }}>
					{selectedJD.must_have_requirements?.map((req, idx) => (
						<Chip key={idx} label={req} color="primary" />
					))}
				</Stack>

				{selectedJD.nice_to_have && selectedJD.nice_to_have.length > 0 && (
					<>
						<Typography variant="subtitle2" gutterBottom>
							Nice-to-Have:
						</Typography>
						<Stack direction="row" spacing={1} flexWrap="wrap" sx={{ gap: 1 }}>
							{selectedJD.nice_to_have.map((req, idx) => (
								<Chip key={idx} label={req} variant="outlined" />
							))}
						</Stack>
					</>
				)}
			</Paper>

			<Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
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
					No hay candidatos evaluados para esta posición. Ejecuta un análisis primero desde la pestaña "New
					Analysis".
				</Alert>
			) : (
				<Stack spacing={2}>
					{results
						.sort((a, b) => b.overall_score - a.overall_score)
						.map((candidate, index) => (
							<CandidateCard key={candidate.candidate_id} candidate={candidate} rank={index + 1} />
						))}
				</Stack>
			)}
		</Box>
	);
}

/**
 * CandidateCard - Tarjeta individual de candidato
 */
function CandidateCard({ candidate, rank }: { candidate: AnalysisResult; rank: number }) {
	const getRankColor = (rankNum: number) => {
		if (rankNum === 1) return 'gold';
		if (rankNum === 2) return 'silver';
		if (rankNum === 3) return '#cd7f32'; // bronze
		return 'text.secondary';
	};

	const getScoreColor = (score: number) => {
		if (score >= 80) return 'success.main';
		if (score >= 60) return 'warning.main';
		return 'error.main';
	};

	return (
		<Card
			sx={{
				border: rank <= 3 ? 2 : 0,
				borderColor: rank <= 3 ? getRankColor(rank) : 'transparent'
			}}
		>
			<CardContent>
				<Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, alignItems: 'center' }}>
					{/* Rank Badge */}
					<Box
						sx={{
							width: 60,
							height: 60,
							borderRadius: '50%',
							bgcolor: rank <= 3 ? getRankColor(rank) : 'grey.300',
							display: 'flex',
							alignItems: 'center',
							justifyContent: 'center',
							fontWeight: 'bold',
							fontSize: 24,
							color: rank <= 3 ? 'white' : 'text.primary',
							flexShrink: 0
						}}
					>
						#{rank}
					</Box>

					{/* Candidate Name */}
					<Box sx={{ flex: 1, minWidth: 200 }}>
						<Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
							<PersonIcon />
							{candidate.name}
						</Typography>
						<Typography variant="caption" color="text.secondary">
							ID: {candidate.candidate_id}
						</Typography>
					</Box>

					{/* Scores */}
					<Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
						<Box sx={{ textAlign: 'center' }}>
							<Typography variant="caption" color="text.secondary">
								Overall Score
							</Typography>
							<Typography
								variant="h5"
								sx={{ color: getScoreColor(candidate.final_score || 0), fontWeight: 'bold' }}
							>
								{(candidate.final_score || 0).toFixed(1)}
							</Typography>
						</Box>
						<Box sx={{ textAlign: 'center' }}>
							<Typography variant="caption" color="text.secondary">
								Similarity
							</Typography>
							<Typography variant="h6">{(candidate.similarity_score || 0).toFixed(1)}</Typography>
						</Box>
						<Box sx={{ textAlign: 'center' }}>
							<Typography variant="caption" color="text.secondary">
								Must-Have
							</Typography>
							<Typography variant="h6">
								{Array.isArray(candidate.must_have_matches) 
									? candidate.must_have_matches.length 
									: 0}
							</Typography>
						</Box>
						<Box sx={{ textAlign: 'center' }}>
							<Typography variant="caption" color="text.secondary">
								Recency
							</Typography>
							<Typography variant="h6">{(candidate.recency_boost || 0).toFixed(1)}</Typography>
						</Box>
					</Box>
				</Box>

				{/* Reason Codes */}
				{candidate.reason_codes && candidate.reason_codes.length > 0 && (
					<Box sx={{ mt: 2 }}>
						<Typography variant="subtitle2" gutterBottom>
							Reason Codes:
						</Typography>
						<Stack direction="row" spacing={1} flexWrap="wrap" sx={{ gap: 1 }}>
							{candidate.reason_codes.map((reason, idx) => (
								<Chip
									key={idx}
									label={typeof reason === 'string' ? reason : reason.code || reason.description}
									size="small"
									variant="outlined"
									title={typeof reason === 'object' ? reason.description : undefined}
								/>
							))}
						</Stack>
					</Box>
				)}

				{/* Matched Requirements */}
				{candidate.must_have_matches && candidate.must_have_matches.length > 0 && (
					<Box sx={{ mt: 2 }}>
						<Typography variant="subtitle2" gutterBottom>
							Matched Must-Have Requirements:
						</Typography>
						<List dense>
							{candidate.must_have_matches.map((req, idx) => (
								<ListItem key={idx} disablePadding>
									<ListItemText primary={`✓ ${req}`} />
								</ListItem>
							))}
						</List>
					</Box>
				)}
			</CardContent>
		</Card>
	);
}
