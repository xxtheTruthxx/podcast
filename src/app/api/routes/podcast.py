from typing import Optional, Annotated, Literal

# Third-party Dependencies
from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status,
    Form,
    Path,
    Query,
)
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# Local Dependencies
from core.config import settings
from core.models.podcast import (
  PodcastEpisode,
  PodcastEpisodeBase,
  PodcastEpisodeAlternative
)
from core.services import GroqClient
from api.dependencies import AsyncSessionDep
from crud import PodcastCRUD

router = APIRouter(tags=["Podcast"])

# Initilize Jinja2
template = Jinja2Templates(directory="templates")

@router.get("/episodes/all",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK)
async def get_episodes(
    request: Request,
    session: AsyncSessionDep,
    offset: int = 0,
    limit: Optional[Annotated[int, Query()]] = None
):
    """
    Get all episodes.
    """
    if not (episodes := await PodcastCRUD(session).read_all(PodcastEpisode, offset=offset, limit=limit)):
      return template.TemplateResponse(
        request=request,
        status_code=status.HTTP_404_NOT_FOUND,
        name="components/notFound.html",
        context={
          "title": settings.NAME
        }
      )
    
    return template.TemplateResponse(
      request=request, name="components/podcast/list_episodes.html", context={
        "request": request,
        "episodes": episodes,
        "title": settings.NAME
      }
    )

@router.get("/episodes/create",
  response_class=HTMLResponse,
  name="create_episode_form")
async def create_episode_form(request: Request):
    return template.TemplateResponse(
        request=request,
        status_code=status.HTTP_201_CREATED,
        name="components/podcast/create_episode.html",
        context={
          "title": settings.NAME,
          "request": request
        }
    )

@router.post("/episodes/create",
    response_model=PodcastEpisode,
    status_code=status.HTTP_201_CREATED,
    name="create_episode")
async def create_episode(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    host: Annotated[str, Form()],
    session: AsyncSessionDep
):
    """
    Create an episode.
    """
    
    await PodcastCRUD(session).create(
      PodcastEpisode(
        title=title,
        description=description,
        host=host
      )
    )

    return RedirectResponse(f"/podcast/episodes/all", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/episodes/{episode_id}/generate_alternative",
  response_class=HTMLResponse,
  name="create_alternative_form")
async def create_alternative_form(
  request: Request,
  session: AsyncSessionDep,
  episode_id: Annotated[int, Path()]
):
  if not await PodcastCRUD(session).read_by_id(episode_id):
    return template.TemplateResponse(
        request=request,
        status_code=status.HTTP_404_NOT_FOUND,
        name="components/notFound.html",
        context={
          "title": settings.NAME
        }
      )
  
  return template.TemplateResponse(
    request=request,
    name="components/podcast/create_alternative_episode.html",
    context={
      "title": settings.NAME,
      "request": request,
      "episode_id": episode_id
    }
  )

@router.post("/episodes/{episode_id}/generate_alternative",
  response_model=PodcastEpisodeAlternative)
async def get_alternative_episode(
    request: Request,
    episode_id: Annotated[int, Path()],
    target: Annotated[Literal["title", "description"], Form()],
    prompt: Annotated[str, Form()],
    session: AsyncSessionDep
):
    """
    Generate an alternative version of the episode.
    """
    if not (result := await PodcastCRUD(session).read_by_id(episode_id)):
      return template.TemplateResponse(
        request=request,
        status_code=status.HTTP_404_NOT_FOUND,
        name="components/notFound.html",
        context={
          "title": settings.NAME
        }
      )
    
    origional_episode = PodcastEpisodeBase.model_validate(result)
    
    groq = GroqClient(
        model=settings.GROQ_MODEL,
    ).create_template(
        prompt=f"{settings.GROQ_MODEL_TEMPLATE}. Prompt: {prompt}."
    )

    field_value = getattr(origional_episode, target)
    generated_alternative = await groq.ask(field_value)

    if not await PodcastCRUD(session).update(
      episode_id,
      data={
        target: str(generated_alternative)
      }
    ):
      return template.TemplateResponse(
        request=request,
        status_code=status.HTTP_404_NOT_FOUND,
        name="components/notFound.html",
        context={
          "title": settings.NAME
        }
      )

    return RedirectResponse(f"/podcast/episodes/all", status_code=status.HTTP_303_SEE_OTHER)

@router.delete("/episodes/{episode_id}/delete",
  name="delete_episode")
async def delete_episode(
  episode_id: Annotated[int, Path()],
  session: AsyncSessionDep
):
  """
  Deletes episode using `id`,
  """
  if not await PodcastCRUD(session).remove_by_id(episode_id):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Episode not found."
      )

  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={"message": "Episode has been removed successfully."}
  )