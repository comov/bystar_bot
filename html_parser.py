import requests
from bs4 import BeautifulSoup

serial_base_url = 'https://animego.org'

serials = {
    'Боруто: Новое поколение Наруто': f'{serial_base_url}/anime/boruto-novoe-pokolenie-naruto-70',
    'Мастера Меча': f'{serial_base_url}/anime/mastera-mecha-onlayn-alisizaciya-voyna-v-podmire-2-1464',
}


def get_serial_html_info(serial_url: str) -> str:
    # получаем страницу с сериалом
    response = requests.get(serial_url)
    if response.status_code != 200:
        print(f'Response from {serial_url} return {response.status_code}')
        return ''

    # парсим страницу и находим ссылку для загрузки видео плеера
    root = BeautifulSoup(response.content, 'html.parser')
    video_player_div = root.find(id='video-player')

    # создаем ссылку для загрузки видео плеера
    url_for_load_episode_info = serial_base_url + video_player_div['data-ajax-url']
    url_for_load_episode_info = f'{url_for_load_episode_info}?_allow=true'

    # загружаем информацию о видео плеере
    episode_info_response = requests.get(url_for_load_episode_info, headers={'x-requested-with': 'XMLHttpRequest'})
    if episode_info_response.status_code != 200:
        print(f'Response from {url_for_load_episode_info} return {response.status_code}')
        return ''

    # информация о видео плеере приходит в виде JSON, мы переводим в dict
    episode_info_dict = episode_info_response.json()  # type: dict

    # получаем HTML c списком серий
    return episode_info_dict.get('content') or ''


def get_episode_info(html_info: str) -> str:
    if not html_info:
        return ''

    # парсим HTML с эпизодами
    root = BeautifulSoup(html_info, 'html.parser')

    # находим список всех эпизодов
    all_episodes = root.find_all('div', class_='video-player-bar-series-item')

    # но нам нужен только последний эпизод и у него в data атрибуте есть html с информацией о выходе
    last_episode_main_div = all_episodes[-1]['data-player-notvideo']

    # парсим инфу о дате выхода
    last_episode = BeautifulSoup(last_episode_main_div, 'html.parser')

    # получаем информацию выводящуюся в плеер
    last_episode_div = last_episode.find_all('div', class_='video-player-online-not')[0]

    # получаем текст который нужно печатать пользователю
    return last_episode_div.find_all('div')[0].string


def run_parser():
    for serial_name, serial_url in serials.items():
        serial_info = get_episode_info(get_serial_html_info(serial_url))
        if not serial_info:
            print(f'Не удалось получить список серий для сериала "{serial_name}"')
            continue
        print(f'Для сериала "{serial_name}", {serial_info}')


if __name__ == '__main__':
    run_parser()
