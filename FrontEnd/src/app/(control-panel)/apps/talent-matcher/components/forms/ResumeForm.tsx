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
	Divider,
	Grid
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import type { ResumeFormData, Experience, Education } from '../../api/types';

type ResumeFormProps = {
	initialData?: Partial<ResumeFormData>;
	onSubmit: (data: ResumeFormData) => void;
	onCancel?: () => void;
};

/**
 * ResumeForm component for manual resume data entry
 */
export default function ResumeForm({ initialData, onSubmit, onCancel }: ResumeFormProps) {
	const [formData, setFormData] = useState<ResumeFormData>({
		name: initialData?.name || '',
		skills: initialData?.skills || [],
		experience: initialData?.experience || [],
		education: initialData?.education || [],
		additionalInfo: initialData?.additionalInfo || ''
	});

	const [skillInput, setSkillInput] = useState('');

	const handleAddSkill = () => {
		if (skillInput.trim() && !formData.skills.includes(skillInput.trim())) {
			setFormData({
				...formData,
				skills: [...formData.skills, skillInput.trim()]
			});
			setSkillInput('');
		}
	};

	const handleRemoveSkill = (index: number) => {
		setFormData({
			...formData,
			skills: formData.skills.filter((_, i) => i !== index)
		});
	};

	const handleAddExperience = () => {
		setFormData({
			...formData,
			experience: [
				...formData.experience,
				{
					company: '',
					position: '',
					startDate: '',
					endDate: '',
					description: ''
				}
			]
		});
	};

	const handleUpdateExperience = (index: number, field: keyof Experience, value: string) => {
		const updated = [...formData.experience];
		updated[index] = { ...updated[index], [field]: value };
		setFormData({ ...formData, experience: updated });
	};

	const handleRemoveExperience = (index: number) => {
		setFormData({
			...formData,
			experience: formData.experience.filter((_, i) => i !== index)
		});
	};

	const handleAddEducation = () => {
		setFormData({
			...formData,
			education: [
				...formData.education,
				{
					institution: '',
					degree: '',
					field: '',
					year: ''
				}
			]
		});
	};

	const handleUpdateEducation = (index: number, field: keyof Education, value: string) => {
		const updated = [...formData.education];
		updated[index] = { ...updated[index], [field]: value };
		setFormData({ ...formData, education: updated });
	};

	const handleRemoveEducation = (index: number) => {
		setFormData({
			...formData,
			education: formData.education.filter((_, i) => i !== index)
		});
	};

	const handleSubmit = () => {
		if (formData.name.trim()) {
			onSubmit(formData);
		}
	};

	return (
		<Card>
			<CardContent>
				<Typography variant="h6" gutterBottom>
					Resume Information
				</Typography>

				<TextField
					fullWidth
					label="Name"
					value={formData.name}
					onChange={(e) => setFormData({ ...formData, name: e.target.value })}
					margin="normal"
					required
				/>

				<Box sx={{ mt: 2 }}>
					<Typography variant="subtitle2" gutterBottom>
						Skills
					</Typography>
					<Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
						<TextField
							size="small"
							placeholder="Add skill"
							value={skillInput}
							onChange={(e) => setSkillInput(e.target.value)}
							onKeyPress={(e) => {
								if (e.key === 'Enter') {
									e.preventDefault();
									handleAddSkill();
								}
							}}
							sx={{ flex: 1 }}
						/>
						<Button variant="outlined" onClick={handleAddSkill}>
							<AddIcon />
						</Button>
					</Box>
					<Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
						{formData.skills.map((skill, index) => (
							<Box
								key={index}
								sx={{
									display: 'flex',
									alignItems: 'center',
									gap: 0.5,
									padding: '4px 8px',
									bgcolor: 'primary.light',
									borderRadius: 1
								}}
							>
								<Typography variant="body2">{skill}</Typography>
								<IconButton size="small" onClick={() => handleRemoveSkill(index)}>
									<DeleteIcon fontSize="small" />
								</IconButton>
							</Box>
						))}
					</Box>
				</Box>

				<Divider sx={{ my: 3 }} />

				<Box sx={{ mb: 2 }}>
					<Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
						<Typography variant="subtitle2">Experience</Typography>
						<Button size="small" startIcon={<AddIcon />} onClick={handleAddExperience}>
							Add Experience
						</Button>
					</Box>
					{formData.experience.map((exp, index) => (
						<Card key={index} variant="outlined" sx={{ mb: 2, p: 2 }}>
							<Grid container spacing={2}>
								<Grid item xs={12} sm={6}>
									<TextField
										fullWidth
										size="small"
										label="Company"
										value={exp.company}
										onChange={(e) => handleUpdateExperience(index, 'company', e.target.value)}
									/>
								</Grid>
								<Grid item xs={12} sm={6}>
									<TextField
										fullWidth
										size="small"
										label="Position"
										value={exp.position}
										onChange={(e) => handleUpdateExperience(index, 'position', e.target.value)}
									/>
								</Grid>
								<Grid item xs={12} sm={6}>
									<TextField
										fullWidth
										size="small"
										label="Start Date"
										value={exp.startDate}
										onChange={(e) => handleUpdateExperience(index, 'startDate', e.target.value)}
										placeholder="YYYY-MM"
									/>
								</Grid>
								<Grid item xs={12} sm={6}>
									<TextField
										fullWidth
										size="small"
										label="End Date"
										value={exp.endDate}
										onChange={(e) => handleUpdateExperience(index, 'endDate', e.target.value)}
										placeholder="YYYY-MM or Present"
									/>
								</Grid>
								<Grid item xs={12}>
									<TextField
										fullWidth
										size="small"
										label="Description"
										value={exp.description}
										onChange={(e) => handleUpdateExperience(index, 'description', e.target.value)}
										multiline
										rows={2}
									/>
								</Grid>
								<Grid item xs={12}>
									<Button
										size="small"
										color="error"
										startIcon={<DeleteIcon />}
										onClick={() => handleRemoveExperience(index)}
									>
										Remove
									</Button>
								</Grid>
							</Grid>
						</Card>
					))}
				</Box>

				<Divider sx={{ my: 3 }} />

				<Box sx={{ mb: 2 }}>
					<Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
						<Typography variant="subtitle2">Education</Typography>
						<Button size="small" startIcon={<AddIcon />} onClick={handleAddEducation}>
							Add Education
						</Button>
					</Box>
					{formData.education.map((edu, index) => (
						<Card key={index} variant="outlined" sx={{ mb: 2, p: 2 }}>
							<Grid container spacing={2}>
								<Grid item xs={12} sm={6}>
									<TextField
										fullWidth
										size="small"
										label="Institution"
										value={edu.institution}
										onChange={(e) => handleUpdateEducation(index, 'institution', e.target.value)}
									/>
								</Grid>
								<Grid item xs={12} sm={6}>
									<TextField
										fullWidth
										size="small"
										label="Degree"
										value={edu.degree}
										onChange={(e) => handleUpdateEducation(index, 'degree', e.target.value)}
									/>
								</Grid>
								<Grid item xs={12} sm={6}>
									<TextField
										fullWidth
										size="small"
										label="Field"
										value={edu.field}
										onChange={(e) => handleUpdateEducation(index, 'field', e.target.value)}
									/>
								</Grid>
								<Grid item xs={12} sm={6}>
									<TextField
										fullWidth
										size="small"
										label="Year"
										value={edu.year}
										onChange={(e) => handleUpdateEducation(index, 'year', e.target.value)}
									/>
								</Grid>
								<Grid item xs={12}>
									<Button
										size="small"
										color="error"
										startIcon={<DeleteIcon />}
										onClick={() => handleRemoveEducation(index)}
									>
										Remove
									</Button>
								</Grid>
							</Grid>
						</Card>
					))}
				</Box>

				<TextField
					fullWidth
					label="Additional Information"
					value={formData.additionalInfo}
					onChange={(e) => setFormData({ ...formData, additionalInfo: e.target.value })}
					multiline
					rows={4}
					margin="normal"
				/>

				<Box sx={{ display: 'flex', gap: 2, mt: 3, justifyContent: 'flex-end' }}>
					{onCancel && (
						<Button variant="outlined" onClick={onCancel}>
							Cancel
						</Button>
					)}
					<Button variant="contained" onClick={handleSubmit} disabled={!formData.name.trim()}>
						Submit
					</Button>
				</Box>
			</CardContent>
		</Card>
	);
}

