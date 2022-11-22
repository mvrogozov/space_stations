import pytest
from django.contrib.auth import get_user_model
from stations.models import Station, Command


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
def test_endpoint_post_requests_stations(project_client, post_url, post_data):
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
def test_endpoint_post_requests_commands(
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
        'Проверьте, что при команде изменения координаты х,'
        ' происходит корректное изменение координаты х.'
    )
    assert coord_after.z == (
        coord_before.z + int(command_data[2]['distance'])
        ), (
        'Проверьте, что при команде изменения координаты х,'
        ' происходит корректное изменение координаты х.'
    )
