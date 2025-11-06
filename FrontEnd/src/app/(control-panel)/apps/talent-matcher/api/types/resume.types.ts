export type Experience = {
	company: string;
	position: string;
	startDate?: string;
	endDate?: string;
	dates?: string;
	description?: string;
};

export type Education = {
	institution: string;
	degree: string;
	field?: string;
	year?: string;
};

export type Resume = {
	candidate_id: string;
	name: string;
	skills: string[];
	experience: Experience[];
	education: Education[];
	raw_text: string;
};

export type ResumeFormData = {
	name: string;
	skills: string[];
	experience: Experience[];
	education: Education[];
	additionalInfo?: string;
};

