from dotenv import load_dotenv

from apps.jobs.repository import claim_next_job

load_dotenv()

import asyncio
import os

from apps.jobs.models import Job
from core.config import settings
from core.database import Database


async def execute_job(job: Job) -> None:
    try:
        print(f"Execution job: {job.id}")
        await asyncio.sleep(2)
        print(f"Finished job: {job.id}")
    except asyncio.CancelledError as e:
        print(f"Job {job.id} execution was cancelled")
        raise e


async def main():
    database_url = settings.DATABASE_URL
    if not database_url:
        raise RuntimeError("[Worker] Env variables is not loaded")
    database = Database(database_url=database_url, echo=False)
    print("Worker started")
    try:
        while True:
            async with database.SessionLocal() as session:
                job = await claim_next_job(session)
                if job is None:
                    print("No jobs found in the database")
                    await asyncio.sleep(1)
                    continue
                print(f"Claiming job {job.id}")
                await execute_job(job)
    except asyncio.CancelledError:
        print(f"The worker execution was cancelled")
    finally:
        print("Performing Essential clean up")
        await database.dispose()


if __name__ == "__main__":
    asyncio.run(main())
