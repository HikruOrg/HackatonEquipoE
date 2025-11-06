'use client';

import { useState, useCallback } from 'react';
import {
	Box,
	Button,
	Card,
	CardContent,
	Typography,
	Divider,
	Chip,
	Alert
} from '@mui/material';
import { PlayArrow as PlayArrowIcon, CloudUpload as CloudUploadIcon } from '@mui/icons-material';
import FileDropZone from '../ui/FileDropZone';
import FilePreview from '../ui/FilePreview';
import StorageSearchModal from '../ui/StorageSearchModal';
import { validateFile, generateFileId, MAX_FILE_SIZE, MAX_RESUME_FILES } from '../../lib/utils';
import { useMultipleFileUpload, useFileValidation } from '../../api/hooks/useFileUpload';
import type { UploadedFile, FileType, StorageFile, Resume, JobDescription } from '../../api/types';

type FileUploadViewProps = {
	onProcess: (resumes: (Resume | string)[], jobDescription: JobDescription | string) => void;
};

/**
 * FileUploadView - Main view for uploading files (PDF/JSON)
 */
export default function FileUploadView({ onProcess }: FileUploadViewProps) {
	const [resumeFiles, setResumeFiles] = useState<UploadedFile[]>([]);
	const [jdFile, setJdFile] = useState<UploadedFile | null>(null);
	const [storageModalOpen, setStorageModalOpen] = useState(false);
	const [storageModalType, setStorageModalType] = useState<'resume' | 'job_description'>('resume');

	const uploadMutation = useMultipleFileUpload();
	const validationMutation = useFileValidation();

	const processFiles = useCallback(async (files: File[], type: 'resume' | 'job_description') => {
		const uploadedFiles: UploadedFile[] = [];

		for (const file of files) {
			// Validate file size
			if (file.size > MAX_FILE_SIZE) {
				uploadedFiles.push({
					id: generateFileId(),
					name: file.name,
					type: file.name.endsWith('.pdf') ? 'pdf' : 'json',
					size: file.size,
					file,
					status: 'invalid',
					error: 'File size exceeds maximum allowed size (10MB)'
				});
				continue;
			}

			// Validate file type
			const validation = validateFile(file);
			if (!validation.valid) {
				uploadedFiles.push({
					id: generateFileId(),
					name: file.name,
					type: validation.type || 'pdf',
					size: file.size,
					file,
					status: 'invalid',
					error: validation.error
				});
				continue;
			}

			// Create uploaded file object
			const uploadedFile: UploadedFile = {
				id: generateFileId(),
				name: file.name,
				type: validation.type as FileType,
				size: file.size,
				file,
				status: 'valid'
			};

			uploadedFiles.push(uploadedFile);
		}

		if (type === 'resume') {
			setResumeFiles((prev) => [...prev, ...uploadedFiles]);
		} else {
			if (uploadedFiles.length > 0) {
				setJdFile(uploadedFiles[0]);
			}
		}
	}, []);

	const handleResumeFilesSelected = useCallback(
		(files: File[]) => {
			if (resumeFiles.length + files.length > MAX_RESUME_FILES) {
				// Show error
				return;
			}
			processFiles(files, 'resume');
		},
		[resumeFiles.length, processFiles]
	);

	const handleJdFileSelected = useCallback(
		(files: File[]) => {
			if (files.length > 0) {
				processFiles([files[0]], 'job_description');
			}
		},
		[processFiles]
	);

	const handleRemoveResumeFile = useCallback((fileId: string) => {
		setResumeFiles((prev) => prev.filter((f) => f.id !== fileId));
	}, []);

	const handleRemoveJdFile = useCallback(() => {
		setJdFile(null);
	}, []);

	const handleStorageSelect = useCallback((file: StorageFile) => {
		// Handle storage file selection
		// This would need to fetch the actual file content
		setStorageModalOpen(false);
	}, []);

	const handleProcess = () => {
		// Convert uploaded files to resume/jd format
		// For now, we'll pass the file IDs or file objects
		const resumeIds = resumeFiles.map((f) => f.id);
		const jdId = jdFile?.id || '';

		if (resumeIds.length > 0 && jdId) {
			onProcess(resumeIds, jdId);
		}
	};

	const canProcess = resumeFiles.length > 0 && jdFile !== null && resumeFiles.every((f) => f.status === 'valid') && jdFile.status === 'valid';

	return (
		<Box sx={{ p: 3 }}>
			<Typography variant="h4" gutterBottom>
				Upload Files
			</Typography>
			<Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
				Upload resumes and job description files (PDF or JSON format)
			</Typography>

			<Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3, mb: 3 }}>
				{/* Resumes Section */}
				<Card>
					<CardContent>
						<Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
							<Typography variant="h6">Resumes</Typography>
							<Box sx={{ display: 'flex', gap: 1 }}>
								<Chip label={`${resumeFiles.length} files`} size="small" />
								<Button
									size="small"
									variant="outlined"
									startIcon={<CloudUploadIcon />}
									onClick={() => {
										setStorageModalType('resume');
										setStorageModalOpen(true);
									}}
								>
									From Storage
								</Button>
							</Box>
						</Box>
						<FileDropZone
							onFilesSelected={handleResumeFilesSelected}
							fileType="pdf"
							multiple
							maxFiles={MAX_RESUME_FILES}
						/>
						<Box sx={{ mt: 2 }}>
							{resumeFiles.map((file) => (
								<FilePreview key={file.id} file={file} onRemove={handleRemoveResumeFile} />
							))}
						</Box>
					</CardContent>
				</Card>

				{/* Job Description Section */}
				<Card>
					<CardContent>
						<Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
							<Typography variant="h6">Job Description</Typography>
							<Button
								size="small"
								variant="outlined"
								startIcon={<CloudUploadIcon />}
								onClick={() => {
									setStorageModalType('job_description');
									setStorageModalOpen(true);
								}}
							>
								From Storage
							</Button>
						</Box>
						<FileDropZone
							onFilesSelected={handleJdFileSelected}
							fileType="json"
							multiple={false}
						/>
						{jdFile && (
							<Box sx={{ mt: 2 }}>
								<FilePreview file={jdFile} onRemove={handleRemoveJdFile} />
							</Box>
						)}
					</CardContent>
				</Card>
			</Box>

			{!canProcess && (
				<Alert severity="info" sx={{ mb: 2 }}>
					Please upload at least one resume and one job description file to proceed.
				</Alert>
			)}

			<Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
				<Button
					variant="contained"
					size="large"
					startIcon={<PlayArrowIcon />}
					onClick={handleProcess}
					disabled={!canProcess || uploadMutation.isPending}
				>
					Process Files
				</Button>
			</Box>

			<StorageSearchModal
				open={storageModalOpen}
				type={storageModalType}
				onSelect={handleStorageSelect}
				onClose={() => setStorageModalOpen(false)}
			/>
		</Box>
	);
}

