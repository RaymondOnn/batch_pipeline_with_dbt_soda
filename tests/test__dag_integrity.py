import logging
from contextlib import contextmanager


@contextmanager
def suppress_logging(namespace):
    logger = logging.getLogger(namespace)
    old_value = logger.disabled
    logger.disabled = True
    try:
        yield
    finally:
        logger.disabled = old_value


def test_dagbag(dag_bag):
    """
    Validate DAG files using Airflow's DagBag
    Includes sanity checks e.g. do task have required arguments,
        are DAG ids unique, are DAGs cyclical
    """
    assert (
        not dag_bag.import_errors
    )  # import errors not raised but captured to ensure all DAGs are parsed

    # Add project-specific checks here e.g. to enforce each DAG has a tag
    # for dag_id, dag in dag_bag.dags.items():
    #     error_msg = f'{dag_id} in {dag.full_filepath} has no tags'
    #     assert dag.tags, error_msg


def test_dag_id_contains_prefix(dag_bag):
    for dag_id, dag in dag_bag.dags.items():
        print(dag_id, dag)

        assert str.lower(dag_id).find("__") != -1


# def test_task_count(dag_bag):
#         """Check task count for a dag"""
#         dag_id='check_for_new_files'
#         dag = dag_bag.get_dag(dag_id)
#         assert len(dag.tasks) == 1
