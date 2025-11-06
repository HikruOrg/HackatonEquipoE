'use client';

import { useState } from 'react';
import {
	Dialog,
	DialogTitle,
	DialogContent,
	DialogActions,
	Button,
	TextField,
	Box,
	List,
	ListItem,
	ListItemText,
	ListItemButton,
	Typography,
	Chip,
	Tabs,
	Tab,
	CircularProgress
} from '@mui/material';
import { useStorageFiles, useSearchStorage } from '../../api/hooks/useStorage';
import type { StorageFile } from '../../api/types';

type StorageSearchModalProps = {
	open: boolean;
	type: 'resume' | 'job_description';
	onSelect: (file: StorageFile) => void;
	onClose: () => void;
};

/**
 * StorageSearchModal component to search and select files from storage
 */
export default function StorageSearchModal({ open, type, onSelect, onClose }: StorageSearchModalProps) {
	const [searchQuery, setSearchQuery] = useState('');
	const [tabValue, setTabValue] = useState(0);

	const { data: files, isLoading } = useStorageFiles({
		type: tabValue === 0 ? 'resume' : 'job_description'
	});

	const searchMutation = useSearchStorage();

	const handleSearch = () => {
		if (searchQuery.trim()) {
			searchMutation.mutate({
				query: searchQuery,
				params: {
					type: tabValue === 0 ? 'resume' : 'job_description'
				}
			});
		}
	};

	const displayFiles = searchQuery.trim() && searchMutation.data ? searchMutation.data : files || [];

	return (
		<Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
			<DialogTitle>Search Storage</DialogTitle>
			<DialogContent>
				<Box sx={{ mb: 2 }}>
					<Tabs value={tabValue} onChange={(_, newValue) => setTabValue(newValue)}>
						<Tab label="Resumes" />
						<Tab label="Job Descriptions" />
					</Tabs>
				</Box>

				<Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
					<TextField
						fullWidth
						size="small"
						placeholder="Search by name..."
						value={searchQuery}
						onChange={(e) => setSearchQuery(e.target.value)}
						onKeyPress={(e) => {
							if (e.key === 'Enter') {
								handleSearch();
							}
						}}
					/>
					<Button variant="contained" onClick={handleSearch}>
						Search
					</Button>
				</Box>

				{isLoading || searchMutation.isPending ? (
					<Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
						<CircularProgress />
					</Box>
				) : displayFiles.length === 0 ? (
					<Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', p: 3 }}>
						No files found
					</Typography>
				) : (
					<List>
						{displayFiles.map((file) => (
							<ListItem key={file.id} disablePadding>
								<ListItemButton onClick={() => onSelect(file)}>
									<ListItemText
										primary={file.name}
										secondary={
											<Box sx={{ display: 'flex', gap: 1, mt: 0.5 }}>
												<Chip label={file.type} size="small" />
												<Typography variant="caption" color="text.secondary">
													{new Date(file.created_at).toLocaleDateString()}
												</Typography>
											</Box>
										}
									/>
								</ListItemButton>
							</ListItem>
						))}
					</List>
				)}
			</DialogContent>
			<DialogActions>
				<Button onClick={onClose}>Cancel</Button>
			</DialogActions>
		</Dialog>
	);
}

