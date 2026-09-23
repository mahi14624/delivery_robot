from setuptools import find_packages, setup
from glob import glob

package_name = 'robot_services'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name , glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mahinour',
    maintainer_email='mahimoh462@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': ['nav_publisher = robot_services.nav_publisher:main',
                             'nav_subscriber = robot_services.nav_subscriber:main',
                             'nav_service_server = robot_services.nav_service_server:main'
        ],
    },
)
