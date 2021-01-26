import requests
from bs4 import BeautifulSoup

serial_base_url = 'https://animego.org'


serials = {
    1: {
        'name': 'Жизнь без оружия 2',
        'url': '/anime/zhizn-bez-oruzhiya-2-1583',
    },
    2: {
        'name': 'Любовь и продюсер',
        'url': '/anime/lyubov-i-prodyuser-1594',
    },
    3: {
        'name': 'Невеста титана',
        'url': '/anime/nevesta-titana-1593',
    },
    4: {
        'name': 'Пламенная бригада пожарных 2',
        'url': '/anime/plamennaya-brigada-pozharnyh-2-1586',
    },
    5: {
        'name': 'Как и ожидалось, моя школьная романтическая жизнь не удалась 3',
        'url': '/anime/kak-i-ozhidalos-moya-shkolnaya-romanticheskaya-zhizn-ne-udalas-3-1591',
    },
    6: {
        'name': 'Удзаки хочет тусоваться!',
        'url': '/anime/udzaki-hochet-tusovatsya-1590',
    },
    7: {
        'name': 'Непризнанный школой владыка демонов',
        'url': '/anime/nepriznannyy-shkoloy-vladyka-demonov-silneyshiy-vladyka-demonov-'
               'v-istorii-postupaet-v-akademiyu-pererodivshis-svoim-potomkom-1584',
    },
    8: {
        'name': 'Питер Грилл и время мудреца',
        'url': '/anime/piter-grill-i-vremya-mudreca-1587',
    },
    9: {
        'name': 'Джибиэйт',
        'url': '/anime/dzhibieyt-1581',
    },
    10: {
        'name': 'Доктор для девушек-монстров',
        'url': '/anime/doktor-dlya-devushek-monstrov-1580',
    },
    11: {
        'name': 'Девушка на час',
        'url': '/anime/devushka-na-chas-1579',
    },
    12: {
        'name': 'Бог старшей школы',
        'url': '/anime/bog-starshey-shkoly-1578',
    },
    13: {
        'name': 'Дека-данс',
        'url': '/anime/deka-dans-1577',
    },
    14: {
        'name': 'Бюро паранормальных расследований Мухё и Родзи 2',
        'url': '/anime/byuro-paranormalnyh-rassledovaniy-muhe-i-rodzi-2-1576',
    },
    15: {
        'name': 'Лазурные огни',
        'url': '/anime/lazurnye-ogni-1575',
    },
    16: {
        'name': 'Формирование извращённой силы',
        'url': '/anime/formirovanie-izvraschennoy-sily-1574',
    },
    17: {
        'name': 'Re: Жизнь в альтернативном мире с нуля 2',
        'url': '/anime/rezero-zhizn-s-nulya-v-alternativnom-mire-2-1569',
    },
    18: {
        'name': 'Мастера Меча Онлайн: Алисизация — Война в Подмирье 2',
        'url': '/anime/mastera-mecha-onlayn-alisizaciya-voyna-v-podmire-2-1464',
    },
    19: {
        'name': 'Боруто: Новое поколение Наруто',
        'url': '/anime/boruto-novoe-pokolenie-naruto-70',
    },
    20: {
        'name': 'Чёрный клевер',
        'url': '/anime/chernyy-klever-27',
    },
}


def get_serial_html_info(serial_path: str) -> str:
    # получаем страницу с сериалом
    serial_url = serial_base_url + serial_path
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
