from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.jobs.models import Job, JobStatus


async def claim_next_job(session: AsyncSession) -> Job | None:
    stmt = (
        select(Job)
        .where(Job.status == JobStatus.pending)
        .order_by(Job.created_at)
        .with_for_update(skip_locked=True)
        .limit(1)
    )
    res = await session.execute(stmt)
    job = res.scalar_one_or_none()
    if job is None:
        return None
    job.status = JobStatus.running
    await session.commit()
    return job


async def mark_job_completed(session: AsyncSession, job_id: int) -> None:
    await session.execute(
        update(Job)
        .where(
            Job.id == job_id,
            Job.status == JobStatus.running,
        )
        .values(status=JobStatus.completed)
    )
    await session.commit()


async def mark_job_failed(session: AsyncSession, job_id: int, error: str) -> None:
    await session.execute(
        update(Job)
        .where(
            Job.id == job_id,
            Job.status == JobStatus.running,
        )
        .values(status=JobStatus.failed, error=error)
    )
    await session.commit()
