"""Service layer for template CRUD operations."""

import json

from sqlalchemy.orm import Session

from app.exceptions import TemplateNotFoundError
from app.models.template import Template
from app.schemas.template import TemplateCreate, TemplateResponse, TemplateUpdate


def _serialize_fields(fields) -> list[dict]:
    """Serialize template fields to list of dicts."""
    if isinstance(fields, str):
        return json.loads(fields)
    return fields


def _to_response(template: Template) -> TemplateResponse:
    """Convert Template model to TemplateResponse schema."""
    return TemplateResponse(
        id=template.id,
        name=template.name,
        description=template.description or "",
        fields=_serialize_fields(template.fields),
        created_at=template.created_at,
        updated_at=template.updated_at,
    )


def create_template(db: Session, template_data: TemplateCreate) -> TemplateResponse:
    """Create a new template.

    Args:
        db: SQLAlchemy database session.
        template_data: Pydantic schema with template creation data.

    Returns:
        TemplateResponse with created template data.
    """
    fields_json = json.dumps([f.model_dump() for f in template_data.fields])
    db_template = Template(
        name=template_data.name,
        description=template_data.description,
        fields=fields_json,
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return _to_response(db_template)


def get_template(db: Session, template_id: int) -> TemplateResponse:
    """Get a template by ID.

    Args:
        db: SQLAlchemy database session.
        template_id: ID of the template to retrieve.

    Returns:
        TemplateResponse with template data.

    Raises:
        TemplateNotFoundError: If template with given ID does not exist.
    """
    template = db.get(Template, template_id)
    if not template:
        raise TemplateNotFoundError(template_id=str(template_id))
    return _to_response(template)


def list_templates(db: Session, skip: int = 0, limit: int = 100) -> list[TemplateResponse]:
    """List all templates with pagination.

    Args:
        db: SQLAlchemy database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        List of TemplateResponse schemas.
    """
    templates = db.query(Template).offset(skip).limit(limit).all()
    return [_to_response(t) for t in templates]


def update_template(db: Session, template_id: int, update_data: TemplateUpdate) -> TemplateResponse:
    """Update an existing template.

    Args:
        db: SQLAlchemy database session.
        template_id: ID of the template to update.
        update_data: Pydantic schema with update data.

    Returns:
        TemplateResponse with updated template data.

    Raises:
        TemplateNotFoundError: If template with given ID does not exist.
    """
    template = db.get(Template, template_id)
    if not template:
        raise TemplateNotFoundError(template_id=str(template_id))

    if update_data.name is not None:
        template.name = update_data.name
    if update_data.description is not None:
        template.description = update_data.description
    if update_data.fields is not None:
        template.fields = json.dumps([f.model_dump() for f in update_data.fields])

    db.commit()
    db.refresh(template)
    return _to_response(template)


def delete_template(db: Session, template_id: int) -> bool:
    """Delete a template by ID.

    Args:
        db: SQLAlchemy database session.
        template_id: ID of the template to delete.

    Returns:
        True if template was deleted, False if not found.
    """
    template = db.get(Template, template_id)
    if not template:
        return False
    db.delete(template)
    db.commit()
    return True


def copy_template(db: Session, template_id: int) -> TemplateResponse:
    """Copy an existing template with a new name.

    Args:
        db: SQLAlchemy database session.
        template_id: ID of the template to copy.

    Returns:
        TemplateResponse with copied template data.

    Raises:
        TemplateNotFoundError: If template with given ID does not exist.
    """
    template = db.get(Template, template_id)
    if not template:
        raise TemplateNotFoundError(template_id=str(template_id))

    new_template = Template(
        name=f"{template.name} (copy)",
        description=template.description,
        fields=template.fields,
    )
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    return _to_response(new_template)
