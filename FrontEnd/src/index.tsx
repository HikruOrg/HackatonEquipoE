import '@i18n/i18n';
import './styles/index.css';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router';
import routes from 'src/configs/routesConfig';
import { worker } from '@mock-utils/mswMockAdapter';

async function mockSetup() {
	try {
		await worker.start({
			onUnhandledRequest: 'bypass',
			serviceWorker: {
				// Use current origin instead of API_BASE_URL to avoid port mismatch
				url: `${window.location.origin}/mockServiceWorker.js`
			}
		});
		console.log('✅ MSW Service Worker started successfully');
	} catch (error) {
		console.error('❌ Failed to start MSW Service Worker:', error);
		// Continue anyway - the app should still work
	}
}

/**
 * The root element of the application.
 */
const container = document.getElementById('app');

if (!container) {
	throw new Error('Failed to find the root element');
}

mockSetup().then(() => {
	/**
	 * The root component of the application.
	 */
	const root = createRoot(container, {
		onUncaughtError: (error, errorInfo) => {
			console.error('UncaughtError error', error, errorInfo.componentStack);
		},
		onCaughtError: (error, errorInfo) => {
			console.error('Caught error', error, errorInfo.componentStack);
		}
	});

	const router = createBrowserRouter(routes);

	root.render(<RouterProvider router={router} />);
});
