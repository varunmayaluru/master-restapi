from typing import Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# In-memory storage
post_table: List[Dict] = []
comments_table: List[Dict] = []


# Schemas
class PostCreate(BaseModel):
    body: str


class Post(BaseModel):
    id: int
    body: str


class CommentCreate(BaseModel):
    body: str
    post_id: int


class Comment(BaseModel):
    id: int
    body: str
    post_id: int


# Routes
@router.post("/post", response_model=Post, status_code=201)
def create_post(post: PostCreate):
    post_id = len(post_table)
    new_post = {"id": post_id, "body": post.body}
    post_table.append(new_post)
    return new_post


@router.get("/post", response_model=List[Post])
def get_all_posts():
    return post_table


@router.post("/comment", response_model=Comment, status_code=201)
def create_comment(comment: CommentCreate):
    if comment.post_id >= len(post_table):
        raise HTTPException(status_code=404, detail="Post not found")

    comment_id = len(comments_table)
    new_comment = {
        "id": comment_id,
        "body": comment.body,
        "post_id": comment.post_id,
    }
    comments_table.append(new_comment)
    return new_comment


@router.get("/post/{post_id}/comment", response_model=List[Comment])
def get_comments_for_post(post_id: int):
    if post_id >= len(post_table):
        raise HTTPException(status_code=404, detail="Post not found")
    return [c for c in comments_table if c["post_id"] == post_id]


@router.get("/post/{post_id}")
def get_post_with_comments(post_id: int):
    if post_id >= len(post_table):
        raise HTTPException(status_code=404, detail="Post not found")

    post = post_table[post_id]
    related_comments = [c for c in comments_table if c["post_id"] == post_id]
    return {"post": post, "comments": related_comments}
