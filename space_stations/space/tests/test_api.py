import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from stations.models import Command, Coordinates, Station

User = get_user_model()
endpoints_status = [
        ('/api/stations/', 200),
        ('/api/stations/{}/', 200),
        ('/api/stations/{}/state/', 200)
]


@pytest.mark.parametrize('test_input, expected', endpoints_status)
@pytest.mark.django_db(transaction=True)
def test_endpoints_response_status(
    project_client,
    test_input,
    resource_setup,
    expected
):
    """Проверка доступности эндпоинтов"""
    station_id = Station.objects.all()[0].id
    response = project_client.get(test_input.format(station_id))
    assert response.status_code == expected, (
        f'Неверный статус ответа при GET запросе к эндпоинту {test_input}.'
    )


@pytest.mark.django_db(transaction=True)
def test_post_requests_stations(project_client, post_url, post_data):
    """Проверка POST запросов на создание станции"""
    count_before = Station.objects.count()
    response = project_client.post(post_url, data=post_data)
    assert response.status_code == 201, (
        f'Ошибка при обращении к {post_url}.'
    )

    count_after = Station.objects.count()
    assert count_after == count_before + 1, (
        f'Проверьте, что при POST запросе к {post_url},'
        f' происходит добавление в БД.'
    )
    obj = Station.objects.latest('create_date')
    assert obj.name == post_data['name'], (
        f'Проверьте, что при POST запросе к {post_url},'
        f' происходит добавление в БД правильных данных.'
    )

    assert obj.status == 'OK', (
        f'Проверьте, что при POST запросе к {post_url},'
        f' происходит добавление станции со статусом "running".'
    )
    assert obj.coordinates is not None, (
        f'Проверьте, что при POST запросе к {post_url},'
        f' происходит добавление координат станции.'
    )


@pytest.mark.django_db(transaction=True)
def test_post_requests_commands(
    project_client,
    command_url,
    resource_setup,
    command_data
):
    """Проверка POST запросов на передвижение станции"""
    count_before = Command.objects.count()
    station = Station.objects.all()[0]
    coord_before = station.coordinates
    user = User.objects.create(
        username='User1'
    )
    for command in command_data:
        command['user'] = user.id
        response = project_client.post(
            command_url.format(station.id),
            data=command
        )
    assert response.status_code == 201, (
        f'Ошибка при обращении к {command_url}.'
    )

    count_after = Command.objects.count()
    assert count_after == count_before + len(command_data), (
        f'Проверьте, что при POST запросе к {command_url},'
        f' происходит добавление в БД команд.'
    )

    station.refresh_from_db()
    coord_after = station.coordinates
    assert coord_after.x == (
        coord_before.x + int(command_data[0]['distance'])
        ), (
        'Проверьте, что при команде изменения координаты х,'
        ' происходит корректное изменение координаты х.'
    )
    assert coord_after.y == (
        coord_before.y + int(command_data[1]['distance'])
        ), (
        'Проверьте, что при команде изменения координаты y,'
        ' происходит корректное изменение координаты y.'
    )
    assert coord_after.z == (
        coord_before.z + int(command_data[2]['distance'])
        ), (
        'Проверьте, что при команде изменения координаты z,'
        ' происходит корректное изменение координаты z.'
    )


@pytest.mark.django_db(transaction=True)
def test_station_break(
    project_client,
    command_url,
    resource_setup,
    command_data
):
    """Проверка условий изменения статуса станции."""
    station = Station.objects.all()[0]
    status_before = station.status
    user = User.objects.all()[0]
    data = {
        'user': user.id,
        'axis': 'x',
        'distance': '-100'
    }
    project_client.post(command_url.format(station.id), data=data)
    station.refresh_from_db()
    status_after = station.status
    assert status_after != status_before, (
        'Проверьте, что при переходе в отрицательные координаты, '
        'меняется статус станции'
    )

    data['distance'] = 1000
    project_client.post(command_url.format(station.id), data=data)
    station.refresh_from_db()
    status_back = station.status
    assert status_after == status_back, (
        'Проверьте, что при возврате в положительные координаты, '
        'не меняется статус станции'
    )


@pytest.mark.django_db(transaction=True)
def test_patch_requests_stations(project_client, resource_setup):
    """Проверка PATCH запросов на изменение станции"""
    station = Station.objects.latest('create_date')
    data = {
        'name': 'patched name',
        'status': 'BR',
        'create_date': timezone.now(),
        'brake_date': timezone.now()
    }
    project_client.patch(endpoints_status[1][0].format(station.id), data=data)
    patched_station = Station.objects.get(id=station.id)
    assert station.name != patched_station.name, (
        'Проверьте, что при PATCH запросе '
        'меняется имя станции'
    )
    assert station.status == patched_station.status, (
        'Проверьте, что при PATCH запросе '
        'не меняется состояние станции'
    )
    assert station.brake_date == patched_station.brake_date, (
        'Проверьте, что при PATCH запросе '
        'не меняется время поломки станции'
    )
    assert station.create_date == patched_station.create_date, (
        'Проверьте, что при PATCH запросе '
        'не меняется время создания станции'
    )


@pytest.mark.django_db(transaction=True)
def test_models_str(project_client, resource_setup):
    """Проверка PATCH запросов на изменение станции"""
    station = Station.objects.latest('create_date')
    coordinates = Coordinates.objects.all()[0]
    command = Command.objects.all()[0]
    assert station.name == str(station), (
        'Проверьте, что в модели "Station" правильно описан метод "__str__"'
    )
    assert (
        f'{coordinates.x},{coordinates.y},{coordinates.z}' == str(coordinates)
    ), 'Проверьте, что в модели "Coordinates" правильно описан метод "__str__"'

    assert f'{command.user} - {command.station.name}' == str(command), (
        'Проверьте, что в модели "Command" правильно описан метод "__str__"'
    )
