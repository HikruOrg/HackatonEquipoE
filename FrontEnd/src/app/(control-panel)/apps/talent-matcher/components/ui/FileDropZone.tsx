'use client';

import { useCallback, useState } from 'react';
import { Box, Paper, Typography, styled } from '@mui/material';
import { Upload as UploadIcon } from '@mui/icons-material';
import type { FileType } from '../../api/types';

const DropZoneRoot = styled(Paper)(({ theme }) => ({
	border: `2px dashed ${theme.palette.divider}`,
	borderRadius: theme.shape.borderRadius,
	padding: theme.spacing(4),
	textAlign: 'center',
	cursor: 'pointer',
	transition: theme.transitions.create(['border-color', 'background-color']),
	'&:hover': {
		borderColor: theme.palette.primary.main,
		backgroundColor: theme.palette.action.hover
	},
	'&.dragging': {
		borderColor: theme.palette.primary.main,
		backgroundColor: theme.palette.action.selected
	}
}));

type FileDropZoneProps = {
	onFilesSelected: (files: File[]) => void;
	accept?: string;
	multiple?: boolean;
	maxFiles?: number;
	fileType?: FileType;
	disabled?: boolean;
};

/**
 * FileDropZone component for drag-and-drop file upload
 */
export default function FileDropZone({
	onFilesSelected,
	accept = '.pdf,.json',
	multiple = true,
	maxFiles,
	fileType,
	disabled = false
}: FileDropZoneProps) {
	const [isDragging, setIsDragging] = useState(false);

	const handleDragEnter = useCallback((e: React.DragEvent) => {
		e.preventDefault();
		e.stopPropagation();
		if (!disabled) {
			setIsDragging(true);
		}
	}, [disabled]);

	const handleDragLeave = useCallback((e: React.DragEvent) => {
		e.preventDefault();
		e.stopPropagation();
		setIsDragging(false);
	}, []);

	const handleDragOver = useCallback((e: React.DragEvent) => {
		e.preventDefault();
		e.stopPropagation();
	}, []);

	const handleDrop = useCallback(
		(e: React.DragEvent) => {
			e.preventDefault();
			e.stopPropagation();
			setIsDragging(false);

			if (disabled) return;

			const files = Array.from(e.dataTransfer.files);
			if (maxFiles && files.length > maxFiles) {
				// Handle error - too many files
				return;
			}

			onFilesSelected(files);
		},
		[disabled, maxFiles, onFilesSelected]
	);

	const handleFileInput = useCallback(
		(e: React.ChangeEvent<HTMLInputElement>) => {
			if (e.target.files) {
				const files = Array.from(e.target.files);
				if (maxFiles && files.length > maxFiles) {
					// Handle error - too many files
					return;
				}
				onFilesSelected(files);
			}
		},
		[maxFiles, onFilesSelected]
	);

	const handleClick = useCallback(() => {
		if (!disabled) {
			document.getElementById(`file-input-${fileType}`)?.click();
		}
	}, [disabled, fileType]);

	return (
		<>
			<input
				id={`file-input-${fileType}`}
				type="file"
				accept={accept}
				multiple={multiple}
				onChange={handleFileInput}
				style={{ display: 'none' }}
				disabled={disabled}
			/>
			<DropZoneRoot
				onDragEnter={handleDragEnter}
				onDragOver={handleDragOver}
				onDragLeave={handleDragLeave}
				onDrop={handleDrop}
				onClick={handleClick}
				className={isDragging ? 'dragging' : ''}
				elevation={isDragging ? 4 : 1}
			>
				<Box
					sx={{
						display: 'flex',
						flexDirection: 'column',
						alignItems: 'center',
						gap: 2
					}}
				>
					<UploadIcon
						sx={{
							fontSize: 48,
							color: 'text.secondary'
						}}
					/>
					<Typography variant="h6" color="text.secondary">
						{isDragging ? 'Drop files here' : 'Drag and drop files here'}
					</Typography>
					<Typography variant="body2" color="text.secondary">
						or click to browse
					</Typography>
					<Typography variant="caption" color="text.secondary">
						Supported formats: PDF, JSON
					</Typography>
				</Box>
			</DropZoneRoot>
		</>
	);
}

