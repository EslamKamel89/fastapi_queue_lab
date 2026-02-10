from dotenv import load_dotenv

from apps.jobs.repository import claim_next_job, mark_job_completed, mark_job_failed

load_dotenv()

import asyncio
import os

from apps.jobs.models import Job
from core.config import settings
from core.database import Database


async def execute_job(job: Job) -> None:
    print(f"Execution job: {job.id}")
    await asyncio.sleep(2)
    print(f"Finished job: {job.id}")


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
                try:
                    await execute_job(job)
                    async with database.SessionLocal() as session:
                        await mark_job_completed(session, job.id)
                except Exception as exc:
                    async with database.SessionLocal() as session:
                        await mark_job_failed(session, job.id, str(exc))
                    print(f"Job {job.id} failed: {exc}")
    finally:
        print("Performing Essential clean up")
        await database.dispose()


if __name__ == "__main__":
    asyncio.run(main())
