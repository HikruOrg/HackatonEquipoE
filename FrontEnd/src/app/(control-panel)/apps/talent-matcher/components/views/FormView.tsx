'use client';

import { useState } from 'react';
import { Box, Button, Tabs, Tab, Typography } from '@mui/material';
import ResumeForm from '../forms/ResumeForm';
import JobDescriptionForm from '../forms/JobDescriptionForm';
import StorageSearchModal from '../ui/StorageSearchModal';
import type { ResumeFormData, JobDescriptionFormData, StorageFile } from '../../api/types';
import { useSaveResume, useSaveJobDescription } from '../../api/hooks/useStorage';

type FormViewProps = {
	onSubmit: (resume: ResumeFormData, jd: JobDescriptionFormData) => void;
	onCancel?: () => void;
};

/**
 * FormView - View for manual data entry via forms
 */
export default function FormView({ onSubmit, onCancel }: FormViewProps) {
	const [tabValue, setTabValue] = useState(0);
	const [resumeData, setResumeData] = useState<ResumeFormData | null>(null);
	const [jdData, setJdData] = useState<JobDescriptionFormData | null>(null);
	const [storageModalOpen, setStorageModalOpen] = useState(false);
	const [storageModalType, setStorageModalType] = useState<'resume' | 'job_description'>('resume');

	const saveResumeMutation = useSaveResume();
	const saveJdMutation = useSaveJobDescription();

	const handleResumeSubmit = (data: ResumeFormData) => {
		setResumeData(data);
		setTabValue(1); // Switch to JD form
	};

	const handleJdSubmit = (data: JobDescriptionFormData) => {
		setJdData(data);
		if (resumeData) {
			onSubmit(resumeData, data);
		}
	};

	const handleStorageSelect = (file: StorageFile) => {
		// Load file from storage and populate form
		// This would need to fetch the actual file content
		setStorageModalOpen(false);
	};

	return (
		<Box sx={{ p: 3 }}>
			<Typography variant="h4" gutterBottom>
				Manual Entry
			</Typography>
			<Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
				Enter resume and job description data manually or load from storage
			</Typography>

			<Box sx={{ mb: 2 }}>
				<Button
					variant="outlined"
					onClick={() => {
						setStorageModalType('resume');
						setStorageModalOpen(true);
					}}
					sx={{ mr: 1 }}
				>
					Load Resume from Storage
				</Button>
				<Button
					variant="outlined"
					onClick={() => {
						setStorageModalType('job_description');
						setStorageModalOpen(true);
					}}
				>
					Load JD from Storage
				</Button>
			</Box>

			<Tabs value={tabValue} onChange={(_, newValue) => setTabValue(newValue)} sx={{ mb: 3 }}>
				<Tab label="Resume" />
				<Tab label="Job Description" disabled={!resumeData} />
			</Tabs>

			{tabValue === 0 && (
				<ResumeForm
					initialData={resumeData || undefined}
					onSubmit={handleResumeSubmit}
					onCancel={onCancel}
				/>
			)}

			{tabValue === 1 && (
				<JobDescriptionForm
					initialData={jdData || undefined}
					onSubmit={handleJdSubmit}
					onCancel={() => setTabValue(0)}
				/>
			)}

			<StorageSearchModal
				open={storageModalOpen}
				type={storageModalType}
				onSelect={handleStorageSelect}
				onClose={() => setStorageModalOpen(false)}
			/>
		</Box>
	);
}

