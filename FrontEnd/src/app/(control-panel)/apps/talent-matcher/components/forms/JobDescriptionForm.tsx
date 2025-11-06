'use client';

import { useState } from 'react';
import {
	Box,
	Button,
	Card,
	CardContent,
	TextField,
	Typography,
	IconButton,
	Divider
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import type { JobDescriptionFormData } from '../../api/types';

type JobDescriptionFormProps = {
	initialData?: Partial<JobDescriptionFormData>;
	onSubmit: (data: JobDescriptionFormData) => void;
	onCancel?: () => void;
};

/**
 * JobDescriptionForm component for manual JD data entry
 */
export default function JobDescriptionForm({ initialData, onSubmit, onCancel }: JobDescriptionFormProps) {
	const [formData, setFormData] = useState<JobDescriptionFormData>({
		title: initialData?.title || '',
		description: initialData?.description || '',
		must_have_requirements: initialData?.must_have_requirements || [],
		nice_to_have: initialData?.nice_to_have || [],
		experience_years_required: initialData?.experience_years_required
	});

	const [mustHaveInput, setMustHaveInput] = useState('');
	const [niceToHaveInput, setNiceToHaveInput] = useState('');

	const handleAddMustHave = () => {
		if (mustHaveInput.trim() && !formData.must_have_requirements.includes(mustHaveInput.trim())) {
			setFormData({
				...formData,
				must_have_requirements: [...formData.must_have_requirements, mustHaveInput.trim()]
			});
			setMustHaveInput('');
		}
	};

	const handleRemoveMustHave = (index: number) => {
		setFormData({
			...formData,
			must_have_requirements: formData.must_have_requirements.filter((_, i) => i !== index)
		});
	};

	const handleAddNiceToHave = () => {
		if (niceToHaveInput.trim() && !formData.nice_to_have.includes(niceToHaveInput.trim())) {
			setFormData({
				...formData,
				nice_to_have: [...formData.nice_to_have, niceToHaveInput.trim()]
			});
			setNiceToHaveInput('');
		}
	};

	const handleRemoveNiceToHave = (index: number) => {
		setFormData({
			...formData,
			nice_to_have: formData.nice_to_have.filter((_, i) => i !== index)
		});
	};

	const handleSubmit = () => {
		if (formData.title.trim() && formData.description.trim()) {
			onSubmit(formData);
		}
	};

	return (
		<Card>
			<CardContent>
				<Typography variant="h6" gutterBottom>
					Job Description Information
				</Typography>

				<TextField
					fullWidth
					label="Job Title"
					value={formData.title}
					onChange={(e) => setFormData({ ...formData, title: e.target.value })}
					margin="normal"
					required
				/>

				<TextField
					fullWidth
					label="Description"
					value={formData.description}
					onChange={(e) => setFormData({ ...formData, description: e.target.value })}
					multiline
					rows={4}
					margin="normal"
					required
				/>

				<TextField
					fullWidth
					label="Years of Experience Required"
					type="number"
					value={formData.experience_years_required || ''}
					onChange={(e) =>
						setFormData({
							...formData,
							experience_years_required: e.target.value ? parseInt(e.target.value, 10) : undefined
						})
					}
					margin="normal"
					inputProps={{ min: 0 }}
				/>

				<Divider sx={{ my: 3 }} />

				<Box sx={{ mb: 2 }}>
					<Typography variant="subtitle2" gutterBottom>
						Must-Have Requirements
					</Typography>
					<Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
						<TextField
							size="small"
							placeholder="Add requirement"
							value={mustHaveInput}
							onChange={(e) => setMustHaveInput(e.target.value)}
							onKeyPress={(e) => {
								if (e.key === 'Enter') {
									e.preventDefault();
									handleAddMustHave();
								}
							}}
							sx={{ flex: 1 }}
						/>
						<Button variant="outlined" onClick={handleAddMustHave}>
							<AddIcon />
						</Button>
					</Box>
					<Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
						{formData.must_have_requirements.map((req, index) => (
							<Box
								key={index}
								sx={{
									display: 'flex',
									alignItems: 'center',
									gap: 0.5,
									padding: '4px 8px',
									bgcolor: 'error.light',
									borderRadius: 1
								}}
							>
								<Typography variant="body2">{req}</Typography>
								<IconButton size="small" onClick={() => handleRemoveMustHave(index)}>
									<DeleteIcon fontSize="small" />
								</IconButton>
							</Box>
						))}
					</Box>
				</Box>

				<Box sx={{ mb: 2 }}>
					<Typography variant="subtitle2" gutterBottom>
						Nice-to-Have Requirements
					</Typography>
					<Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
						<TextField
							size="small"
							placeholder="Add requirement"
							value={niceToHaveInput}
							onChange={(e) => setNiceToHaveInput(e.target.value)}
							onKeyPress={(e) => {
								if (e.key === 'Enter') {
									e.preventDefault();
									handleAddNiceToHave();
								}
							}}
							sx={{ flex: 1 }}
						/>
						<Button variant="outlined" onClick={handleAddNiceToHave}>
							<AddIcon />
						</Button>
					</Box>
					<Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
						{formData.nice_to_have.map((req, index) => (
							<Box
								key={index}
								sx={{
									display: 'flex',
									alignItems: 'center',
									gap: 0.5,
									padding: '4px 8px',
									bgcolor: 'info.light',
									borderRadius: 1
								}}
							>
								<Typography variant="body2">{req}</Typography>
								<IconButton size="small" onClick={() => handleRemoveNiceToHave(index)}>
									<DeleteIcon fontSize="small" />
								</IconButton>
							</Box>
						))}
					</Box>
				</Box>

				<Box sx={{ display: 'flex', gap: 2, mt: 3, justifyContent: 'flex-end' }}>
					{onCancel && (
						<Button variant="outlined" onClick={onCancel}>
							Cancel
						</Button>
					)}
					<Button
						variant="contained"
						onClick={handleSubmit}
						disabled={!formData.title.trim() || !formData.description.trim()}
					>
						Submit
					</Button>
				</Box>
			</CardContent>
		</Card>
	);
}

