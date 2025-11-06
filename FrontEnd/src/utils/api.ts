import ky, { KyInstance } from 'ky';

// En desarrollo, usar el origen actual para que MSW pueda interceptar correctamente
// En producción, usar la URL configurada
const getApiBaseUrl = () => {
	if (import.meta.env.DEV) {
		// En desarrollo, usar el origen actual (mismo puerto que la app)
		return window.location.origin;
	}
	// En producción, usar la URL configurada
	return (import.meta.env.VITE_API_BASE_URL as string) || '/';
};

export const API_BASE_URL = getApiBaseUrl();

let globalHeaders: Record<string, string> = {};

export const api: KyInstance = ky.create({
	prefixUrl: `${API_BASE_URL}/api`,
	hooks: {
		beforeRequest: [
			(request) => {
				Object.entries(globalHeaders).forEach(([key, value]) => {
					request.headers.set(key, value);
				});
			}
		]
	},
	retry: {
		limit: 2,
		methods: ['get', 'put', 'head', 'delete', 'options', 'trace']
	}
});

export const setGlobalHeaders = (headers: Record<string, string>) => {
	globalHeaders = { ...globalHeaders, ...headers };
};

export const removeGlobalHeaders = (headerKeys: string[]) => {
	headerKeys.forEach((key) => {
		delete globalHeaders[key];
	});
};

export const getGlobalHeaders = () => {
	return globalHeaders;
};

export default api;
