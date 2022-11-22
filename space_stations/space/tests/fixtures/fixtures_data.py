import pytest
from rest_framework.test import APIClient

from stations.models import Coordinates, Station


@pytest.fixture
def post_url():
    return '/api/stations/'


@pytest.fixture
def command_url():
    return '/api/stations/{}/state/'


@pytest.fixture
def post_data():
    return {"name": "test_name 1", "id": "1"}


@pytest.fixture
def command_data():
    return [
        {
            'axis': 'x',
            'distance': '33'
        },
        {
            'axis': 'y',
            'distance': '44'
        },
        {
            'axis': 'z',
            'distance': '55'
        },
    ]


@pytest.fixture
def project_client():
    client = APIClient()
    return client


@pytest.fixture(scope="function")
def resource_setup(request):
    obj = Station.objects.create(
        name='testname',
    )
    Coordinates.objects.create(
        x=1, y=2, z=3, station=obj
    )
    return obj
