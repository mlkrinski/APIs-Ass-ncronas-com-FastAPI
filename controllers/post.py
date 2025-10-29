from fastapi import HTTPException, status, APIRouter
from models.post import posts
from schemas.post import PostIn, PostUpdate
from views.post import PostOut
from database import database

router = APIRouter(prefix="/posts")


@router.get("/", response_model=list[PostOut])
async def read_posts(
    published: bool = None,
    limit: int = 10,
    skip: int = 0,
):
    query = posts.select().limit(limit).offset(skip)
    if published is not None:
        query = query.where(posts.c.published == published)
    return await database.fetch_all(query)


@router.get("/{post_id}", response_model=PostOut)
async def read_post(post_id: int):
    query = posts.select().where(posts.c.id == post_id)
    post = await database.fetch_one(query)
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def create_posts(post: PostIn):
    command = posts.insert().values(
        title=post.title,
        content=post.content,
        published_at=post.published_at,
        published=post.published,
    )
    last_id = await database.execute(command)
    # fake_db.append(post.model_dump())
    return {**post.model_dump(), "id": last_id}


@router.patch("/{post_id}", response_model=PostOut)
async def update_post(post_id: int, post: PostUpdate):
    existing_post = await database.fetch_one(posts.select().where(posts.c.id == post_id))
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post não encontrado")

    update_data = post.model_dump(exclude_unset=True)  # só campos enviados
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum campo enviado para atualização")

    command = posts.update().where(posts.c.id == post_id).values(**update_data)
    await database.execute(command)

    update_post = await database.fetch_one(posts.select().where(posts.c.id == post_id))
    return update_post


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int):
    post = await database.fetch_one(posts.select().where(posts.c.id == post_id))
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")

    await database.execute(posts.delete().where(posts.c.id == post_id))
    return {"message": f"Post {post_id} deletado com sucesso"}
