'use client';

import { Box, Chip, IconButton, Paper, Typography, styled } from '@mui/material';
import { Delete as DeleteIcon, CheckCircle, Error as ErrorIcon, CloudUpload } from '@mui/icons-material';
import { formatFileSize } from '../../lib/utils';
import type { UploadedFile } from '../../api/types';

const FilePreviewRoot = styled(Paper)(({ theme }) => ({
	padding: theme.spacing(2),
	marginBottom: theme.spacing(1),
	display: 'flex',
	alignItems: 'center',
	gap: theme.spacing(2)
}));

type FilePreviewProps = {
	file: UploadedFile;
	onRemove?: (fileId: string) => void;
	showActions?: boolean;
};

/**
 * FilePreview component to display uploaded file information
 */
export default function FilePreview({ file, onRemove, showActions = true }: FilePreviewProps) {
	const getStatusIcon = () => {
		switch (file.status) {
			case 'valid':
			case 'processed':
				return <CheckCircle color="success" />;
			case 'invalid':
			case 'error':
				return <ErrorIcon color="error" />;
			case 'processing':
				return <CloudUpload color="primary" />;
			default:
				return null;
		}
	};

	const getStatusColor = (): 'default' | 'primary' | 'success' | 'error' => {
		switch (file.status) {
			case 'valid':
			case 'processed':
				return 'success';
			case 'invalid':
			case 'error':
				return 'error';
			case 'processing':
				return 'primary';
			default:
				return 'default';
		}
	};

	return (
		<FilePreviewRoot elevation={1}>
			{getStatusIcon()}
			<Box sx={{ flex: 1, minWidth: 0 }}>
				<Typography variant="body1" noWrap>
					{file.name}
				</Typography>
				<Box sx={{ display: 'flex', gap: 1, mt: 0.5, flexWrap: 'wrap' }}>
					<Chip label={file.type.toUpperCase()} size="small" color={file.type === 'pdf' ? 'primary' : 'secondary'} />
					<Chip label={formatFileSize(file.size)} size="small" variant="outlined" />
					{file.pages && (
						<Chip label={`${file.pages} pages`} size="small" variant="outlined" />
					)}
					<Chip label={file.status} size="small" color={getStatusColor()} />
				</Box>
				{file.error && (
					<Typography variant="caption" color="error" sx={{ mt: 0.5, display: 'block' }}>
						{file.error}
					</Typography>
				)}
			</Box>
			{showActions && onRemove && (
				<IconButton
					size="small"
					onClick={() => onRemove(file.id)}
					color="error"
					disabled={file.status === 'processing'}
				>
					<DeleteIcon />
				</IconButton>
			)}
		</FilePreviewRoot>
	);
}

