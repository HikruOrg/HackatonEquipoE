export type JobDescription = {
	jd_id: string;
	title: string;
	must_have_requirements: string[];
	nice_to_have?: string[];
	description: string;
	experience_years_required?: number;
	raw_text: string;
};

export type JobDescriptionFormData = {
	title: string;
	description: string;
	must_have_requirements: string[];
	nice_to_have: string[];
	experience_years_required?: number;
};

