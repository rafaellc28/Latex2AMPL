import setuptools

if __name__ == '__main__':
	setuptools.setup(
		name='LaTeX to AMPL',

		packages=setuptools.find_packages(),
		
		entry_points={
			'console_scripts': [
				'latex2ampl = latex2ampl.main:main',
			],
		},
		
		setup_requires=['pytest-runner', 'ply'],
		tests_require=['pytest'],
	)