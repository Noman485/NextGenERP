from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from database.connection import engine
from models.category import Category
from models.product import Product
from models.user import User
from services.audit import category_state, record_audit

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    dependencies=[Depends(get_current_user)],
)


def get_db():
    with Session(engine) as session:
        yield session


def validate_category(db: Session, name: str, category_id: int | None = None) -> str:
    name = name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Category name is required")

    duplicate_name = db.query(Category).filter(Category.name == name)
    if category_id is not None:
        duplicate_name = duplicate_name.filter(Category.id != category_id)
    if duplicate_name.first():
        raise HTTPException(status_code=409, detail="A category with this name already exists")

    return name


@router.post("/")
def create_category(
    request: Request,
    name: str = Query(..., min_length=1, max_length=120),
    description: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_category = Category(
        name=validate_category(db, name),
        description=description
    )

    db.add(new_category)
    try:
        db.flush()
        record_audit(
            db,
            action="category.create",
            entity_type="category",
            entity_id=new_category.id,
            actor=current_user,
            after=category_state(new_category),
            request=request,
        )
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A category with this name already exists",
        ) from error
    db.refresh(new_category)

    return new_category


@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.put("/{category_id}")
def update_category(
    category_id: int,
    request: Request,
    name: str = Query(..., min_length=1, max_length=120),
    description: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .with_for_update()
        .first()
    )

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    before = category_state(category)
    category.name = validate_category(db, name, category_id)
    category.description = description
    record_audit(
        db,
        action="category.update",
        entity_type="category",
        entity_id=category.id,
        actor=current_user,
        before=before,
        after=category_state(category),
        request=request,
    )
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A category with this name already exists",
        ) from error
    db.refresh(category)
    return category


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .with_for_update()
        .first()
    )

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if db.query(Product.id).filter(Product.category_id == category_id).first():
        raise HTTPException(
            status_code=409,
            detail="Category cannot be deleted while products are assigned to it",
        )

    record_audit(
        db,
        action="category.delete",
        entity_type="category",
        entity_id=category.id,
        actor=current_user,
        before=category_state(category),
        request=request,
    )
    db.delete(category)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Category cannot be deleted while products are assigned to it",
        ) from error
    return {"message": "Category deleted successfully"}