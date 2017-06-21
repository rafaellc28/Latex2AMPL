import setuptools

if __name__ == '__main__':
	setuptools.setup(
		name='Latex to Mathprog2',

		packages=setuptools.find_packages(),
		
		entry_points={
			'console_scripts': [
				'latex2mathprog2 = latex2mathprog2.main:main',
			],
		},
		
		setup_requires=['pytest-runner', 'ply'],
		tests_require=['pytest'],
	)