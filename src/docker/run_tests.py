import subprocess
from glob import glob


# flake8 --ignore E501 dags --benchmark || exit 1
EXCLUDE_DIRS = ('/opt/airflow/dags/online_retail/dbt',)

def run_flake8():
    print('STARTING FLAKE8 TESTS...')
    fnames = (fname for fname in glob('/opt/airflow/dags/**/*.py', recursive=True) if not fname.startswith(EXCLUDE_DIRS))
    return subprocess.call(('flake8', '-v', '--ignore', 'E501', *fnames))


def run_tests():
    print('STARTING PYTEST TESTS...')
    subprocess.call(('pytest', '--cache-clear', '-rsxX', '-l', '--tb=short', '--strict', '-v', 'tests/'))

def run_black():
    print('STARTING BLACK TESTS...')
    subprocess.call(('pytest', '--black', '-p', f'no:{EXCLUDE_DIRS}/dbt_packages/dbt_utils/tests/conftest.py', '-v', 'dags/'))

    
def main():
    run_flake8()
    run_black()    
    run_tests()
    print('ALL TESTS COMPLETED SUCCESSFULLY! 🥳')
    
if __name__ == '__main__':
    exit(main())