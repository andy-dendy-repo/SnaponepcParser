import pandas as pd
import httpx


class Parser:

    CLIENT = httpx.AsyncClient()

    cookies = {
        'JSESSIONID': '6D8208E7C9891D3600506147013F9F2B',
        'SBSEPCSID': '92f00fb6-038c-4b1e-896e-7c3ed892c8cd',
        'AWSALB': 'dIwFbhmK/St1tx39nBtdzr1NIoFEzRsaVDQA+nfB7vtA/xf6vtAMz6YBW6ZwMtZxmdB4wz7zGOAwlKHRsIuUe0a+jN3uBRU6+i+UxXIVBvxyxD4PcDGDHjUNPqPH',
        'AWSALBCORS': 'dIwFbhmK/St1tx39nBtdzr1NIoFEzRsaVDQA+nfB7vtA/xf6vtAMz6YBW6ZwMtZxmdB4wz7zGOAwlKHRsIuUe0a+jN3uBRU6+i+UxXIVBvxyxD4PcDGDHjUNPqPH',
    }

    headers = {
        'AMG': 'c00bb0fd-cac7-447a-b0c3-25e6fe500f07',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8,uk;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'JSESSIONID=6D8208E7C9891D3600506147013F9F2B; SBSEPCSID=92f00fb6-038c-4b1e-896e-7c3ed892c8cd; AWSALB=dIwFbhmK/St1tx39nBtdzr1NIoFEzRsaVDQA+nfB7vtA/xf6vtAMz6YBW6ZwMtZxmdB4wz7zGOAwlKHRsIuUe0a+jN3uBRU6+i+UxXIVBvxyxD4PcDGDHjUNPqPH; AWSALBCORS=dIwFbhmK/St1tx39nBtdzr1NIoFEzRsaVDQA+nfB7vtA/xf6vtAMz6YBW6ZwMtZxmdB4wz7zGOAwlKHRsIuUe0a+jN3uBRU6+i+UxXIVBvxyxD4PcDGDHjUNPqPH',
        'DNT': '1',
        'Pragma': 'no-cache',
        'Referer': 'https://snaponepc.com/epc/',
        'SBSEPC5CS': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJSRCI6ImJkZTI0MmVqYiIsIlRTIjoiMjAyMi0wNi0wNlQxOToyMToxMS4xNDNaIiwiUEsiOiJTQlNFUEM1In0.NRnhpvVm9YP7vXXq4OSDI547A0CWgXIg38cS055PxTU',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    URL_PART = '/filterRequest/am9iSWQ9MXxkYXRhU2V0SWQ9ZGVjOTkxM2EtYzA1YS01NTM1LWUwNDMtNj' \
               'BkNDE2YWNhZjM1fG1hbnVhbEZpbHRlcnNFbmFibGVkPXRyd'\
               'WV8bG9jYWxlPWVuLVVTfGJ1c1JlZz1JTkR8cHJpY2VCb29rSWQ9OTFmMTA0O' \
               'TEtY2RlYi00ZDIyLThkMzctMWQ4MzI1MzBiNjZjfHVzZXJ'\
               'JZD1jMDBiYjBmZC1jYWM3LTQ0N2EtYjBjMy0yNWU2ZmU1MDBmMDc='

    API_PART = 'https://snaponepc.com/epc-services/datasets/dec9913a-c05a-5535-e043-60d416acaf35/navigations/'

    START_URL = 'https://snaponepc.com/epc-services/datasets/dec9913a-c05a-5535-e043-60d416acaf35/navigations'\
                '/filterRequest'\
                '/am9iSWQ9MXxkYXRhU2V0SWQ9ZGVjOTkxM2EtYzA1YS01NTM1LWUwNDMtNjB' \
                'kNDE2YWNhZjM1fG1hbnVhbEZpbHRlcnNFbmFibGVkPXRyd'\
                'WV8bG9jYWxlPWVuLVVTfGJ1c1JlZz1JTkR8cHJpY2VCb29rSWQ9OTFmMTA0OTEtY2R' \
                'lYi00ZDIyLThkMzctMWQ4MzI1MzBiNjZjfHVzZXJ'\
                'JZD1jMDBiYjBmZC1jYWM3LTQ0N2EtYjBjMy0yNWU2ZmU1MDBmMDc='

    DRIVER = None

    LIST = []

    HISTORY = []

    async def run(self):
        await self.parse_page(self.START_URL, 0)

    def exists_in_list(self, part):
        partNumber = part['partNumber']

        byPartNumber = [item for item in self.LIST if item['partNo'] == partNumber]

        return len(byPartNumber) > 0

    async def parse_page(self, url, level):
        response = await self.CLIENT.get(
            url,
            cookies=self.cookies, headers=self.headers)

        root = response.json()

        parts = root.get('partItems', None)

        if parts is not None:
            ok = True
            partsTask = [self.parse_part(part['partId'], part['partItemId']) for part in parts if self.exists_in_list(part) is False]
            for partTask in partsTask:
                ok = ok and await partTask

            if ok is False:
                pass
        else:
            links = [self.get_link(item) for item in root['children']['childNodes']]
            for link in links:
                await self.parse_page(link, level+1)

    def get_link(self, item):
        if item['leafNode'] is True:
            image_id = item['imageId']
            return 'https://snaponepc.com/epc-services/datasets/dec9913a-c05a-5535-e043-60d416acaf35/pages/parts/' \
                   + item['serializedPath'] + self.URL_PART + f'?imageId={image_id}'
        else:
            return self.API_PART + item['serializedPath'] + self.URL_PART

    async def parse_part(self, partId, partItemId):
        response = await self.CLIENT.get(
            'https://snaponepc.com/epc-services/partdetails/supersession?ds=dec9913a-c05a-5535-e043-60d416acaf35&pr='
            f'{partId}&fr=am9iSWQ9MXxkYXRhU2V0SWQ9ZGVjOTkxM2EtYzA1YS01NTM1LWUwNDMtNjBkNDE2YWNhZjM1fG1hbnVhbEZpbHRlcnNF'
            'bmFibGVkPXRydWV8ZXF1aXBtZW50UmVmSWQ9NzUwMDR8bG9jYWxlPWVuLVVTfGJ1c1JlZz1JTkR8cHJpY2VCb29rSWQ9OTFmMTA0OTEt'
            'Y2RlYi00ZDIyLThkMzctMWQ4MzI1MzBiNjZjfHVzZXJJZD1jMDBiYjBmZC1jYWM3LTQ0N2EtYjBjMy0yNWU2ZmU1MDBmMDc=&dn=true'
            f'&pi={partItemId}', cookies=self.cookies, headers=self.headers)

        try:
            root = response.json()

            part_no = root['supersessionDataElements'][0]['partNumber']

            prices = root['supersessionDataElements'][0].get('prices', None)

            if prices is None:
                self.LIST.append({'partNo': part_no})
            else:
                for price in prices:
                    price['partNo'] = part_no

                self.LIST.extend(prices)
                print(len(self.LIST))

            return True
        except Exception as ex:
            print(str(ex))
            return False

    def save(self):
        df = pd.DataFrame(self.LIST)
        df.to_csv('result.csv')


