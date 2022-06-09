from Parser import Parser
import asyncio


async def main():

    parser = Parser()
    try:
        await parser.run()
    except Exception as ex:
        str(ex)
    parser.save()

asyncio.run(main())
