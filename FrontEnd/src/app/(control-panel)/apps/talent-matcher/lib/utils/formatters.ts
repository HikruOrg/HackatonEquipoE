/**
 * Format score with color indicator
 */
export const formatScore = (score: number): { value: string; color: 'success' | 'warning' | 'error' } => {
	const value = score.toFixed(2);
	if (score >= 80) {
		return { value, color: 'success' };
	}
	if (score >= 60) {
		return { value, color: 'warning' };
	}
	return { value, color: 'error' };
};

/**
 * Format date to readable string
 */
export const formatDate = (date: string | Date): string => {
	const d = typeof date === 'string' ? new Date(date) : date;
	return d.toLocaleDateString('es-ES', {
		year: 'numeric',
		month: 'long',
		day: 'numeric'
	});
};

/**
 * Calculate estimated time remaining
 */
export const calculateEstimatedTime = (
	current: number,
	total: number,
	elapsedSeconds: number
): number | undefined => {
	if (current === 0 || total === 0) return undefined;

	const avgTimePerCandidate = elapsedSeconds / current;
	const remaining = total - current;
	return Math.ceil(remaining * avgTimePerCandidate);
};

