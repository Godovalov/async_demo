from aiohttp import ClientSession
import asyncio


async def request_json(invoice_number: str, session: ClientSession, headers: dict) -> dict:
    """
        Отправка запросов
    """
    request_url = f'https://api.godovalov.ru/exec_sp/main/Backoffice_Get_Invoices?dateFrom=2021-09-19&dateTo=2021-10-19&invoiceNum={invoice_number}'
    response = await session.get(url=request_url, headers=headers, ssl=False)
    try:
        response_json = await response.json()
        print(f'Количество найденных накладных {invoice_number}: ', len(response_json))
        print(response_json)
    except:
        response_json = {'error': 'Ошибка сервера! Данные не найдены'}
        print(f'Количество найденных накладных {invoice_number}: 0')
        print(response_json)
    return response_json


async def gather_tasks(invoices, headers):
    """
        Создаём задачи для асинхронного выполнения
    """
    async with ClientSession() as session:
        tasks = []
        for invoice in invoices:
            tasks.append(request_json(invoice_number=invoice, session=session, headers=headers))
        return await asyncio.gather(*tasks)


def demo_async():
    headers = {'Authorization': '7eb363ad-869d-4c72-a014-9f7c097aee56'}
    invoices = ['11810-', '1S65426513', '1X65643505']
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(gather_tasks(invoices, headers))  # Асинхронная отправка запросов


if __name__ == '__main__':
    demo_async()
