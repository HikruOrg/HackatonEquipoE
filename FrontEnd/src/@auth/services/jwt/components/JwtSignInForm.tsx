import { useState } from 'react';
import Button from '@mui/material/Button';
import { Box, Typography } from '@mui/material';
import useJwtAuth from '../useJwtAuth';

function JwtSignInForm() {
	const { signIn } = useJwtAuth();
	const [isLoading, setIsLoading] = useState(false);

	const handleSignIn = async () => {
		setIsLoading(true);
		try {
			// Usar credenciales por defecto del usuario admin
			await signIn({
				email: 'admin@fusetheme.com',
				password: '5;4+0IOx:\\Dy'
			});
		} catch (error) {
			console.error('Error signing in:', error);
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<Box className="flex w-full flex-col justify-center items-center gap-4">
			<Typography variant="h6" className="text-center">
				Bienvenido a Talent Matcher
			</Typography>
			<Typography variant="body2" color="text.secondary" className="text-center mb-4">
				Haz clic en el botón para iniciar sesión automáticamente
			</Typography>
			<Button
				variant="contained"
				color="secondary"
				className="w-full"
				aria-label="Sign in"
				onClick={handleSignIn}
				disabled={isLoading}
				size="large"
			>
				{isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
			</Button>
		</Box>
	);
}

export default JwtSignInForm;
