""" app entrypoint """

import logging
import asyncio
import asyncpg

import config as cfg

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    asyncio.run(run())
    return "Hello, World!"

async def run():
    conn = await asyncpg.connect(
        user=cfg.DATABASE_USER, password=cfg.DATABASE_USER_PASSWORD,
        database=cfg.DATABASE_NAME, host=cfg.DATABASE_SERVICE
    )
    values = await conn.fetch('SELECT * FROM accounts')
    logging.info("values: %s", values)
    await conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename="run.log", filemode="w")
    app.run(host="0.0.0.0", port=5000)
