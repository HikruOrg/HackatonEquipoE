'use client';

import { useState } from 'react';
import FusePageSimple from '@fuse/core/FusePageSimple';
import { Box, Tabs, Tab } from '@mui/material';
import FileUploadView from './FileUploadView';
import FormView from './FormView';
import ProcessingView from './ProcessingView';
import ResultsView from './ResultsView';
import JobDescriptionsView from './JobDescriptionsView';
import { useStartAnalysis } from '../../api/hooks/useAnalysis';
import type { Resume, JobDescription, AnalysisResult } from '../../api/types';

type ViewType = 'upload' | 'form' | 'processing' | 'results' | 'job-descriptions';

/**
 * TalentMatcherAppView - Main application view
 */
export default function TalentMatcherAppView() {
	const [currentView, setCurrentView] = useState<ViewType>('upload');
	const [uploadTab, setUploadTab] = useState(0);
	const [mainTab, setMainTab] = useState(0);
	const [results, setResults] = useState<AnalysisResult[]>([]);

	const startAnalysisMutation = useStartAnalysis();

	const handleProcessFiles = async (resumes: (Resume | string)[], jobDescription: JobDescription | string) => {
		try {
			await startAnalysisMutation.mutateAsync({
				resumes: resumes.map((r) => (typeof r === 'string' ? r : r.candidate_id)),
				job_description: typeof jobDescription === 'string' ? jobDescription : jobDescription.jd_id
			});
			setCurrentView('processing');
		} catch (error) {
			console.error('Error starting analysis:', error);
		}
	};

	const handleFormSubmit = async (resume: unknown, jd: unknown) => {
		// Convert form data to Resume/JobDescription format
		// This would need proper conversion logic
		const resumeData = resume as Resume;
		const jdData = jd as JobDescription;
		await handleProcessFiles([resumeData], jdData);
	};

	const handleAnalysisComplete = (analysisResults: AnalysisResult[]) => {
		setResults(analysisResults);
		setCurrentView('results');
	};

	const handleNewAnalysis = () => {
		setCurrentView('upload');
		setMainTab(1); // Tab 1 is now "New Analysis"
		setResults([]);
		setUploadTab(0);
	};

	const handleMainTabChange = (_: unknown, newValue: number) => {
		setMainTab(newValue);
		if (newValue === 0) {
			setCurrentView('job-descriptions');
		} else if (newValue === 1) {
			setCurrentView('upload');
		}
	};

	return (
		<FusePageSimple
			content={
				<Box sx={{ height: '100%' }}>
					{/* Main Navigation Tabs */}
					<Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
						<Tabs value={mainTab} onChange={handleMainTabChange}>
							<Tab label="Job Descriptions & Results" />
							<Tab label="New Analysis" />
						</Tabs>
					</Box>

					{/* Job Descriptions Tab */}
					{mainTab === 0 && <JobDescriptionsView />}

					{/* New Analysis Tab */}
					{mainTab === 1 && (
						<>
							{currentView === 'upload' && (
								<>
									<Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
										<Tabs value={uploadTab} onChange={(_, newValue) => setUploadTab(newValue)}>
											<Tab label="File Upload" />
											<Tab label="Manual Entry" />
										</Tabs>
									</Box>
									{uploadTab === 0 && <FileUploadView onProcess={handleProcessFiles} />}
									{uploadTab === 1 && (
										<FormView onSubmit={handleFormSubmit} onCancel={handleNewAnalysis} />
									)}
								</>
							)}

							{currentView === 'processing' && (
								<ProcessingView
									onComplete={handleAnalysisComplete}
									onCancel={handleNewAnalysis}
								/>
							)}

							{currentView === 'results' && (
								<ResultsView results={results} onNewAnalysis={handleNewAnalysis} />
							)}
						</>
					)}
				</Box>
			}
		/>
	);
}

