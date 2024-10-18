import requests
from variables import vacancies_request_path
from nim_connect import get_talk

def get_vacancy_from_server_db():
    request = requests.get(vacancies_request_path)
    request = request.json()
    return request['results']

def NVIDIA_fill_profession(vacancies: list):
    for num_vacancy in range(0, len(vacancies)):
        vacancy_text = f"{vacancies[num_vacancy]['title']}. {vacancies[num_vacancy]['body']}"
        question = "определи профессию по вакансии из списка ['backend', 'frontend', 'qa', 'devops', 'designer', " \
                   "'game', 'mobile', 'product', 'pm', 'analyst', 'marketing', 'sales_manager', 'hr']. " \
                   "Напиши профессию только одним словом из предложенного списка.\nвакансия: " + vacancy_text
        answer = get_talk(quest=question, user='ruslan', history=False).replace('*', '')
        vacancies[num_vacancy]['NVIDIA_profession'] = answer
    return vacancies

def compose_and_write_excel():
    pass

def save_excel(vacancies: list):
    filename = 'vacancies.xlsx'
    path = './excel/'
    excel_path = path + filename
    return excel_path

def start_process():
    vacancies = get_vacancy_from_server_db()
    vacancies = NVIDIA_fill_profession(vacancies)
    return save_excel(vacancies)


if __name__ == "__main__":
    result = start_process()