from typing import Optional, Annotated
from datetime import datetime

# Third-party Dependencies
from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status,
    Form,
    Path,
    Depends,
    Cookie
)
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select

# Local Dependencies
from core.config import settings
from core.models.podcast import PodcastEpisode, PodcastEpisodeBase
from core.logger import logger
from api.dependencies import AsyncSessionDep
from crud import PodcastCRUD, RssCRUD

router = APIRouter(tags=["Admin"])

# Initialize Jinja2 template
template = Jinja2Templates(directory="templates")

def check_admin_auth(admin_session: Optional[str] = Cookie(None)) -> bool:
    """Check if user is authenticated as admin"""
    return admin_session == "authenticated"

async def require_admin(request: Request):
    """Dependency to require admin authentication"""
    admin_session = request.cookies.get("admin_session")
    if admin_session != "authenticated":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin authentication required"
        )
    return True

@router.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    """Admin login page"""
    return template.TemplateResponse(
        request=request,
        name="components/admin/login.html",
        context={
            "title": "Admin Login",
            "error": None
        }
    )

@router.post("/admin/login", response_class=HTMLResponse)
async def admin_login(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    """Admin login handler"""
    if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
        response = RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="admin_session", value="authenticated", httponly=True, max_age=3600*24)  # 24 hours
        return response
    else:
        return template.TemplateResponse(
            request=request,
            status_code=status.HTTP_401_UNAUTHORIZED,
            name="components/admin/login.html",
            context={
                "title": "Admin Login",
                "error": "Invalid username or password"
            }
        )

@router.get("/admin/logout")
async def admin_logout():
    """Admin logout handler"""
    response = RedirectResponse(url="/admin/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="admin_session")
    return response

@router.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    session: AsyncSessionDep,
    _: bool = Depends(require_admin)
):
    """Admin dashboard with statistics"""
    try:
        # Get statistics
        total_episodes = await session.execute(
            select(func.count(PodcastEpisode.id))
        )
        episode_count = total_episodes.scalar() or 0
        
        # Get recent episodes
        recent_episodes = await PodcastCRUD(session).read_all(
            PodcastEpisode,
            offset=0,
            limit=5
        )
        
        # Get RSS feed count (if available)
        try:
            feeds = await RssCRUD.fetch_all(url=settings.RSS_URL, limit=100)
            rss_count = len(feeds) if feeds else 0
        except Exception as e:
            logger.error(f"Error fetching RSS feeds: {e}")
            rss_count = 0
        
        return template.TemplateResponse(
            request=request,
            name="components/admin/dashboard.html",
            context={
                "title": "Admin Dashboard",
                "episode_count": episode_count,
                "rss_count": rss_count,
                "recent_episodes": recent_episodes or [],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    except Exception as e:
        logger.error(f"Error in admin dashboard: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error loading dashboard"
        )

@router.get("/admin/episodes", response_class=HTMLResponse)
async def admin_episodes(
    request: Request,
    session: AsyncSessionDep,
    _: bool = Depends(require_admin),
    offset: int = 0,
    limit: Optional[int] = None
):
    """Admin view of all episodes"""
    try:
        episodes = await PodcastCRUD(session).read_all(
            PodcastEpisode,
            offset=offset,
            limit=limit
        )
        
        total_count = await session.execute(
            select(func.count(PodcastEpisode.id))
        )
        total = total_count.scalar() or 0
        
        return template.TemplateResponse(
            request=request,
            name="components/admin/episodes.html",
            context={
                "title": "Manage Episodes",
                "episodes": episodes or [],
                "total_count": total,
                "offset": offset,
                "limit": limit
            }
        )
    except Exception as e:
        logger.error(f"Error loading episodes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error loading episodes"
        )

@router.get("/admin/episodes/add", response_class=HTMLResponse)
async def admin_add_episode_form(
    request: Request,
    _: bool = Depends(require_admin)
):
    """Admin form to add new episode"""
    return template.TemplateResponse(
        request=request,
        name="components/admin/add_episode.html",
        context={
            "title": "Add New Episode"
        }
    )

@router.post("/admin/episodes/add", response_class=HTMLResponse)
async def admin_add_episode(
    request: Request,
    session: AsyncSessionDep,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    host: Annotated[str, Form()],
    _: bool = Depends(require_admin)
):
    """Admin handler to add new episode"""
    try:
        await PodcastCRUD(session).create(
            PodcastEpisode(
                title=title,
                description=description,
                host=host
            )
        )
        return RedirectResponse(url="/admin/episodes", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        logger.error(f"Error creating episode: {e}")
        return template.TemplateResponse(
            request=request,
            name="components/admin/add_episode.html",
            context={
                "title": "Add New Episode",
                "error": "Failed to create episode. Please try again."
            }
        )

@router.get("/admin/episodes/{episode_id}/edit", response_class=HTMLResponse)
async def admin_edit_episode_form(
    request: Request,
    session: AsyncSessionDep,
    episode_id: Annotated[int, Path()],
    _: bool = Depends(require_admin)
):
    """Admin form to edit episode"""
    episode = await PodcastCRUD(session).read_by_id(episode_id)
    if not episode:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Episode not found"
        )
    
    return template.TemplateResponse(
        request=request,
        name="components/admin/edit_episode.html",
        context={
            "title": "Edit Episode",
            "episode": episode
        }
    )

@router.post("/admin/episodes/{episode_id}/edit", response_class=HTMLResponse)
async def admin_edit_episode(
    request: Request,
    session: AsyncSessionDep,
    episode_id: Annotated[int, Path()],
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    host: Annotated[str, Form()],
    _: bool = Depends(require_admin)
):
    """Admin handler to update episode"""
    try:
        episode = await PodcastCRUD(session).update(
            episode_id,
            data={
                "title": title,
                "description": description,
                "host": host
            }
        )
        if not episode:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Episode not found"
            )
        return RedirectResponse(url="/admin/episodes", status_code=status.HTTP_303_SEE_OTHER)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating episode: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating episode"
        )

@router.delete("/admin/episodes/{episode_id}/delete")
async def admin_delete_episode(
    episode_id: Annotated[int, Path()],
    session: AsyncSessionDep,
    _: bool = Depends(require_admin)
):
    """Admin handler to delete episode"""
    try:
        episode = await PodcastCRUD(session).remove_by_id(episode_id)
        if not episode:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Episode not found"
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Episode deleted successfully"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting episode: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting episode"
        )

@router.get("/admin/rss", response_class=HTMLResponse)
async def admin_rss_feeds(
    request: Request,
    _: bool = Depends(require_admin)
):
    """Admin view of RSS feeds"""
    try:
        feeds = await RssCRUD.fetch_all(url=settings.RSS_URL, limit=50)
        return template.TemplateResponse(
            request=request,
            name="components/admin/rss_feeds.html",
            context={
                "title": "RSS Feeds",
                "feeds": feeds or [],
                "total_count": len(feeds) if feeds else 0
            }
        )
    except Exception as e:
        logger.error(f"Error loading RSS feeds: {e}")
        return template.TemplateResponse(
            request=request,
            name="components/admin/rss_feeds.html",
            context={
                "title": "RSS Feeds",
                "feeds": [],
                "total_count": 0,
                "error": "Failed to load RSS feeds"
            }
        )

