from sqlalchemy import select
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
