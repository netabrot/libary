"""
Orders Router
-------------

This file defines the API endpoints for managing book orders and waiting lists.

Endpoints:
- GET /orders/         → List orders with optional filters (user orders or all for admin/librarian)
- POST /orders/        → Create a new book order (member+)
- PUT /orders/{id}   → Update order details (admin/librarian only)
- DELETE /orders/{id}  → Cancel/delete an order (owner or admin/librarian)

Notes:
- Admin/Librarian actions require authentication and role checks.
- Database sessions are provided via `Depends(get_db)`.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.core.enums import UserRole
from app.db import get_db
from app.db.models import User
from app.schemas import CreateBookOrder, ShowBookOrder
from app.services import crud_order as order

router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)


@router.get("/", response_model=List[ShowBookOrder])
def list_orders(
        user_id: int | None = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    """List orders. Users see only their orders, admin/librarian can see all."""
    if current_user.role not in [UserRole.ADMIN, UserRole.LIBRARIAN]:
        orders = order.get_user_orders(db, user_id=current_user.id)
    else:
        if user_id:
            orders = order.get_user_orders(db, user_id=user_id)
        else:
            orders = db.query(order.model).all()

    return orders


@router.post("/", response_model=ShowBookOrder, status_code=status.HTTP_201_CREATED)
def create_order(payload: CreateBookOrder, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    """Create a new book order (join waiting list)."""
    try:
        created = order.create_order_by_title(
            db,
            user_id=current_user.id,
            book_title=payload.book_title,
        )
        return created

    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete/cancel an order by ID. Users can only cancel their own orders."""
    if current_user.role not in [UserRole.ADMIN, UserRole.LIBRARIAN]:
        try:
            order.cancel_order(db, order_id=order_id, user_id=current_user.id)
        except ValueError as e:
            if "not found" in str(e):
                raise HTTPException(status_code=404, detail=str(e))
            else:
                raise HTTPException(status_code=400, detail=str(e))
    else:
        obj = order.get(db, id=order_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Order not found")
        order.remove(db, id=order_id)

    return


@router.get("/waiting/{book_id}")
def get_waiting_list(
        book_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role(UserRole.LIBRARIAN))
):
    """Get waiting list for a specific book (Librarian+ only)."""
    waiting_orders = order.get_waiting_orders_by_book(db, book_id=book_id)

    return {
        "book_id": book_id,
        "total_waiting": len(waiting_orders),
        "waiting_list": [
            {
                "order_id": order_obj.id,
                "user_name": order_obj.user.full_name,
                "user_email": order_obj.user.email,
                "order_date": order_obj.order_date,
                "position": idx + 1,
            }
            for idx, order_obj in enumerate(waiting_orders)
        ]
    }


@router.get("/my-orders")
def get_my_orders(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get current user's orders."""
    orders = order.get_user_orders(db, user_id=current_user.id)
    return orders
